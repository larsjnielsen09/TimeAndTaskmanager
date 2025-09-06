#!/usr/bin/env python3
"""
Time and Task Manager - Flask Web Application
A web-based version of the time and task manager with full CRUD operations.
"""

import sys
import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager, Task

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this for production

# Initialize managers
task_manager = TaskManager()

@app.route('/')
def dashboard():
    """Main dashboard showing overview of tasks."""
    tasks = task_manager.get_all_tasks()
    
    # Calculate statistics
    total_hours = sum(task.hours for task in tasks)
    customers = task_manager.get_customers()
    departments = task_manager.get_departments()
    
    # Get recent tasks (last 10)
    recent_tasks = sorted(tasks, key=lambda t: t.date, reverse=True)[:10]
    
    return render_template('dashboard.html', 
                         tasks=tasks,
                         total_tasks=len(tasks),
                         total_hours=total_hours,
                         total_customers=len(customers),
                         total_departments=len(departments),
                         recent_tasks=recent_tasks)

@app.route('/tasks')
def list_tasks():
    """List all tasks with filtering options."""
    customer_filter = request.args.get('customer', '')
    department_filter = request.args.get('department', '')
    
    tasks = task_manager.get_all_tasks()
    
    # Apply filters
    if customer_filter:
        tasks = [t for t in tasks if t.customer.lower() == customer_filter.lower()]
    if department_filter:
        tasks = [t for t in tasks if t.department.lower() == department_filter.lower()]
    
    # Sort by date (most recent first)
    tasks.sort(key=lambda t: t.date, reverse=True)
    
    # Get unique customers and departments for filter dropdowns
    all_customers = task_manager.get_customers()
    all_departments = task_manager.get_departments()
    
    return render_template('tasks.html', 
                         tasks=tasks,
                         customers=all_customers,
                         departments=all_departments,
                         current_customer=customer_filter,
                         current_department=department_filter)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    """Create a new task."""
    if request.method == 'POST':
        customer = request.form.get('customer', '').strip()
        department = request.form.get('department', '').strip()
        date = request.form.get('date', '').strip()
        hours = float(request.form.get('hours', 0) or 0)
        description = request.form.get('description', '').strip()
        
        if not customer:
            flash('Customer name is required', 'error')
            return render_template('create_task.html')
        
        if not department:
            flash('Department is required', 'error')
            return render_template('create_task.html')
        
        if not date:
            flash('Date is required', 'error')
            return render_template('create_task.html')
        
        if hours <= 0:
            flash('Hours must be greater than 0', 'error')
            return render_template('create_task.html')
        
        task = task_manager.create_task(
            customer=customer,
            department=department,
            date=date,
            hours=hours,
            description=description
        )
        
        flash(f'Task for {task.customer} created successfully!', 'success')
        return redirect(url_for('list_tasks'))
    
    return render_template('create_task.html')

@app.route('/tasks/<task_id>')
def view_task(task_id):
    """View task details."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    return render_template('view_task.html', task=task)

@app.route('/tasks/<task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    if request.method == 'POST':
        updates = {}
        
        customer = request.form.get('customer', '').strip()
        if customer: updates['customer'] = customer
        
        department = request.form.get('department', '').strip()
        if department: updates['department'] = department
        
        date = request.form.get('date', '').strip()
        if date: updates['date'] = date
        
        hours = request.form.get('hours', '').strip()
        if hours:
            try:
                updates['hours'] = float(hours)
            except ValueError:
                pass
        
        description = request.form.get('description', '').strip()
        if description is not None: updates['description'] = description
        
        if updates:
            updated_task = task_manager.update_task(task_id, **updates)
            flash(f'Task for {updated_task.customer} updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
        
        return redirect(url_for('view_task', task_id=task_id))
    
    return render_template('edit_task.html', task=task)

@app.route('/tasks/<task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    if task_manager.delete_task(task_id):
        flash(f'Task for "{task.customer}" deleted successfully!', 'success')
    else:
        flash('Failed to delete task', 'error')
    
    return redirect(url_for('list_tasks'))


@app.route('/reports')
def reports():
    """Reports overview page."""
    return render_template('reports.html')

@app.route('/reports/customers')
def report_customers():
    """Customer hours report."""
    customers = task_manager.get_customers()
    customer_data = []
    
    for customer in customers:
        tasks = task_manager.get_tasks_by_customer(customer)
        total_hours = sum(task.hours for task in tasks)
        if total_hours > 0:
            customer_data.append({
                'customer': customer,
                'total_hours': total_hours,
                'task_count': len(tasks),
                'percentage': 0
            })
    
    # Sort by hours (descending)
    customer_data.sort(key=lambda x: x['total_hours'], reverse=True)
    
    # Calculate percentages
    total_all_hours = sum(item['total_hours'] for item in customer_data)
    if total_all_hours > 0:
        for item in customer_data:
            item['percentage'] = (item['total_hours'] / total_all_hours) * 100
    
    return render_template('report_customers.html', 
                         customer_data=customer_data,
                         total_hours=total_all_hours)

@app.route('/reports/departments')
def report_departments():
    """Department hours report."""
    departments = task_manager.get_departments()
    department_data = []
    
    for department in departments:
        tasks = task_manager.get_tasks_by_department(department)
        total_hours = sum(task.hours for task in tasks)
        if total_hours > 0:
            department_data.append({
                'department': department,
                'total_hours': total_hours,
                'task_count': len(tasks),
                'percentage': 0
            })
    
    # Sort by hours (descending)
    department_data.sort(key=lambda x: x['total_hours'], reverse=True)
    
    # Calculate percentages
    total_all_hours = sum(item['total_hours'] for item in department_data)
    if total_all_hours > 0:
        for item in department_data:
            item['percentage'] = (item['total_hours'] / total_all_hours) * 100
    
    return render_template('report_departments.html', 
                         department_data=department_data,
                         total_hours=total_all_hours)

@app.template_filter('datetime')
def datetime_filter(value):
    """Format datetime string for display."""
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return value

@app.template_filter('duration')
def duration_filter(seconds):
    """Format duration in seconds to human readable format."""
    if seconds == 0:
        return "0m"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

@app.template_filter('status_badge')
def status_badge_filter(status):
    """Return appropriate CSS class for status badge."""
    status_classes = {
        'active': 'badge-primary',
        'completed': 'badge-success',
        'paused': 'badge-warning'
    }
    return status_classes.get(status, 'badge-secondary')

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host='127.0.0.1', port=5000)
