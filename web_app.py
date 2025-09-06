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

from task_manager import TaskManager, Task, CustomerManager, Customer, DepartmentManager, Department

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this for production

# Initialize managers
task_manager = TaskManager()
customer_manager = CustomerManager()
department_manager = DepartmentManager()

@app.route('/')
def dashboard():
    """Main dashboard showing overview of tasks."""
    tasks = task_manager.get_all_tasks()
    
    # Calculate statistics
    total_hours = sum(task.hours for task in tasks)
    customers = customer_manager.get_all_customers()
    departments = department_manager.get_all_departments()
    
    # Get recent tasks (last 10) - sort by creation timestamp for newest added first
    recent_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)[:10]
    
    return render_template('dashboard.html', 
                         tasks=tasks,
                         total_tasks=len(tasks),
                         total_hours=total_hours,
                         total_customers=len(customers),
                         total_departments=len(departments),
                         recent_tasks=recent_tasks,
                         customers=customers,
                         customer_manager=customer_manager,
                         department_manager=department_manager)

@app.route('/tasks')
def list_tasks():
    """List all tasks with filtering options."""
    customer_filter = request.args.get('customer', '')
    department_filter = request.args.get('department', '')
    
    tasks = task_manager.get_all_tasks()
    
    # Apply filters
    if customer_filter:
        tasks = [t for t in tasks if t.customer_id == customer_filter]
    if department_filter:
        tasks = [t for t in tasks if t.department_id == department_filter]
    
    # Sort by date (most recent first)
    tasks.sort(key=lambda t: t.date, reverse=True)
    
    # Get customers and departments for filter dropdowns and task display
    all_customers = customer_manager.get_all_customers()
    all_departments = department_manager.get_all_departments()
    
    return render_template('tasks.html', 
                         tasks=tasks,
                         customers=all_customers,
                         departments=all_departments,
                         customer_manager=customer_manager,
                         department_manager=department_manager,
                         current_customer=customer_filter,
                         current_department=department_filter)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    """Create a new task."""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', '').strip()
        department_id = request.form.get('department_id', '').strip()
        date = request.form.get('date', '').strip()
        hours = float(request.form.get('hours', 0) or 0)
        description = request.form.get('description', '').strip()
        
        if not customer_id:
            flash('Customer selection is required', 'error')
            customers = customer_manager.get_all_customers()
            return render_template('create_task.html', customers=customers)
        
        if not department_id:
            flash('Department selection is required', 'error')
            customers = customer_manager.get_all_customers()
            return render_template('create_task.html', customers=customers)
        
        if not date:
            flash('Date is required', 'error')
            customers = customer_manager.get_all_customers()
            return render_template('create_task.html', customers=customers)
        
        if hours <= 0:
            flash('Hours must be greater than 0', 'error')
            customers = customer_manager.get_all_customers()
            return render_template('create_task.html', customers=customers)
        
        task = task_manager.create_task(
            customer_id=customer_id,
            department_id=department_id,
            date=date,
            hours=hours,
            description=description
        )
        
        # Get customer name for flash message
        customer = customer_manager.get_customer(customer_id)
        flash(f'Task for {customer.name if customer else "customer"} created successfully!', 'success')
        return redirect(url_for('list_tasks'))
    
    # GET request - load form
    customers = customer_manager.get_all_customers()
    return render_template('create_task.html', customers=customers)

@app.route('/tasks/<task_id>')
def view_task(task_id):
    """View task details."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    # Get customer and department details
    customer = customer_manager.get_customer(task.customer_id)
    department = department_manager.get_department(task.department_id)
    
    return render_template('view_task.html', 
                         task=task, 
                         customer=customer, 
                         department=department)

@app.route('/tasks/<task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    if request.method == 'POST':
        updates = {}
        
        customer_id = request.form.get('customer_id', '').strip()
        if customer_id: updates['customer_id'] = customer_id
        
        department_id = request.form.get('department_id', '').strip()
        if department_id: updates['department_id'] = department_id
        
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
            # Get customer name for flash message
            customer = customer_manager.get_customer(updated_task.customer_id)
            flash(f'Task for {customer.name if customer else "customer"} updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
        
        return redirect(url_for('view_task', task_id=task_id))
    
    # GET request - load form
    customers = customer_manager.get_all_customers()
    customer = customer_manager.get_customer(task.customer_id)
    department = department_manager.get_department(task.department_id)
    return render_template('edit_task.html', 
                         task=task, 
                         customers=customers, 
                         customer=customer, 
                         department=department)

@app.route('/tasks/<task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    if task_manager.delete_task(task_id):
        # Get customer name for flash message
        customer = customer_manager.get_customer(task.customer_id)
        flash(f'Task for "{customer.name if customer else "customer"}" deleted successfully!', 'success')
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
    customers = customer_manager.get_all_customers()
    customer_data = []
    
    for customer in customers:
        tasks = task_manager.get_tasks_by_customer(customer.id)
        total_hours = sum(task.hours for task in tasks)
        if total_hours > 0:
            customer_data.append({
                'customer': customer.name,
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
    departments = department_manager.get_all_departments()
    department_data = []
    
    for department in departments:
        tasks = task_manager.get_tasks_by_department(department.id)
        total_hours = sum(task.hours for task in tasks)
        if total_hours > 0:
            # Get customer name for this department
            customer = customer_manager.get_customer(department.customer_id)
            department_data.append({
                'department': department.name,
                'customer': customer.name if customer else 'Unknown',
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

# Customer Management Routes
@app.route('/customers')
def list_customers():
    """List all customers."""
    customers = customer_manager.get_all_customers()
    customers.sort(key=lambda c: c.name)
    return render_template('customers.html', customers=customers)

@app.route('/customers/create', methods=['GET', 'POST'])
def create_customer():
    """Create a new customer."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        
        if not name:
            flash('Customer name is required', 'error')
            return render_template('create_customer.html')
        
        customer = customer_manager.create_customer(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        
        # Handle departments
        departments = []
        dept_index = 1
        while True:
            dept_name = request.form.get(f'department_{dept_index}_name', '').strip()
            if not dept_name:
                break
            dept_description = request.form.get(f'department_{dept_index}_description', '').strip()
            
            department = department_manager.create_department(
                name=dept_name,
                customer_id=customer.id,
                description=dept_description
            )
            departments.append(department)
            dept_index += 1
        
        if departments:
            flash(f'Customer "{customer.name}" created with {len(departments)} department(s)!', 'success')
        else:
            flash(f'Customer "{customer.name}" created successfully!', 'success')
        
        return redirect(url_for('view_customer', customer_id=customer.id))
    
    return render_template('create_customer.html')

@app.route('/customers/<customer_id>')
def view_customer(customer_id):
    """View customer details."""
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('list_customers'))
    
    # Get departments for this customer
    departments = department_manager.get_departments_by_customer(customer_id)
    # Get tasks for this customer
    tasks = task_manager.get_tasks_by_customer(customer_id)
    
    return render_template('view_customer.html', 
                         customer=customer, 
                         departments=departments,
                         tasks=tasks)

@app.route('/customers/<customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    """Edit a customer."""
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('list_customers'))
    
    if request.method == 'POST':
        updates = {}
        
        name = request.form.get('name', '').strip()
        if name: updates['name'] = name
        
        email = request.form.get('email', '').strip()
        if email is not None: updates['email'] = email
        
        phone = request.form.get('phone', '').strip()
        if phone is not None: updates['phone'] = phone
        
        address = request.form.get('address', '').strip()
        if address is not None: updates['address'] = address
        
        if updates:
            updated_customer = customer_manager.update_customer(customer_id, **updates)
            flash(f'Customer "{updated_customer.name}" updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
        
        return redirect(url_for('view_customer', customer_id=customer_id))
    
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/<customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    """Delete a customer."""
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('list_customers'))
    
    # Check if customer has tasks or departments
    tasks = task_manager.get_tasks_by_customer(customer_id)
    departments = department_manager.get_departments_by_customer(customer_id)
    
    if tasks or departments:
        flash(f'Cannot delete customer "{customer.name}" - customer has existing tasks or departments', 'error')
        return redirect(url_for('view_customer', customer_id=customer_id))
    
    if customer_manager.delete_customer(customer_id):
        flash(f'Customer "{customer.name}" deleted successfully!', 'success')
    else:
        flash('Failed to delete customer', 'error')
    
    return redirect(url_for('list_customers'))

# Department Management Routes
@app.route('/customers/<customer_id>/departments/create', methods=['GET', 'POST'])
def create_department(customer_id):
    """Create a new department for a customer."""
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        flash('Customer not found', 'error')
        return redirect(url_for('list_customers'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Department name is required', 'error')
            return render_template('create_department.html', customer=customer)
        
        department = department_manager.create_department(
            name=name,
            customer_id=customer_id,
            description=description
        )
        
        flash(f'Department "{department.name}" created successfully!', 'success')
        return redirect(url_for('view_customer', customer_id=customer_id))
    
    return render_template('create_department.html', customer=customer)

@app.route('/departments/<department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    """Edit a department."""
    department = department_manager.get_department(department_id)
    if not department:
        flash('Department not found', 'error')
        return redirect(url_for('list_customers'))
    
    customer = customer_manager.get_customer(department.customer_id)
    
    if request.method == 'POST':
        updates = {}
        
        name = request.form.get('name', '').strip()
        if name: updates['name'] = name
        
        description = request.form.get('description', '').strip()
        if description is not None: updates['description'] = description
        
        if updates:
            updated_department = department_manager.update_department(department_id, **updates)
            flash(f'Department "{updated_department.name}" updated successfully!', 'success')
        else:
            flash('No changes made', 'info')
        
        return redirect(url_for('view_customer', customer_id=department.customer_id))
    
    return render_template('edit_department.html', department=department, customer=customer)

@app.route('/departments/<department_id>/delete', methods=['POST'])
def delete_department(department_id):
    """Delete a department."""
    department = department_manager.get_department(department_id)
    if not department:
        flash('Department not found', 'error')
        return redirect(url_for('list_customers'))
    
    # Check if department has tasks
    tasks = task_manager.get_tasks_by_department(department_id)
    
    if tasks:
        flash(f'Cannot delete department "{department.name}" - department has existing tasks', 'error')
        return redirect(url_for('view_customer', customer_id=department.customer_id))
    
    customer_id = department.customer_id
    if department_manager.delete_department(department_id):
        flash(f'Department "{department.name}" deleted successfully!', 'success')
    else:
        flash('Failed to delete department', 'error')
    
    return redirect(url_for('view_customer', customer_id=customer_id))

# API route for getting departments by customer (for AJAX calls)
@app.route('/api/customers/<customer_id>/departments')
def get_customer_departments(customer_id):
    """Get departments for a specific customer (for AJAX calls)."""
    departments = department_manager.get_departments_by_customer(customer_id)
    return jsonify([{'id': dept.id, 'name': dept.name} for dept in departments])

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
