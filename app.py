#!/usr/bin/env python3
"""
Time and Task Manager - Web Application
A Flask web app to track time spent on customer tasks and projects.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from src.task_manager import TaskManager, Task
from src.models import Customer, Department

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize components
task_manager = TaskManager()


@app.route('/reports/by-department')
def report_by_department():
    tasks = task_manager.get_all_tasks()
    
    # Group tasks by department
    tasks_by_department = {}
    for task in tasks:
        if task.department_id not in tasks_by_department:
            tasks_by_department[task.department_id] = []
        tasks_by_department[task.department_id].append(task)
        
    return render_template('report_by_department.html', tasks_by_department=tasks_by_department, task_manager=task_manager)

@app.route('/reports/by-task')
def report_by_task():
    tasks = task_manager.get_all_tasks()
    
    # Group tasks by description
    tasks_by_description = {}
    for task in tasks:
        if task.description not in tasks_by_description:
            tasks_by_description[task.description] = []
        tasks_by_description[task.description].append(task)
        
    total_all_time = sum(task.hours for task in tasks)
    return render_template('report_by_task.html', tasks_by_description=tasks_by_description, task_manager=task_manager, total_all_time=total_all_time)

@app.route('/reports/by-customer')
def report_by_customer():
    tasks = task_manager.get_all_tasks()
    
    # Group tasks by customer
    tasks_by_customer = {}
    for task in tasks:
        if task.customer_id not in tasks_by_customer:
            tasks_by_customer[task.customer_id] = []
        tasks_by_customer[task.customer_id].append(task)
        
    total_all_time = sum(task.hours for task in tasks)
    return render_template('report_by_customer.html', tasks_by_customer=tasks_by_customer, task_manager=task_manager, total_all_time=total_all_time)

@app.route('/reports/by-project')
def report_by_project():
    tasks = task_manager.get_all_tasks()
    
    # Group tasks by department (acting as project)
    tasks_by_department = {}
    for task in tasks:
        if task.department_id not in tasks_by_department:
            tasks_by_department[task.department_id] = []
        tasks_by_department[task.department_id].append(task)
        
    total_all_time = sum(task.hours for task in tasks)
    return render_template('report_by_project.html', tasks_by_department=tasks_by_department, task_manager=task_manager, total_all_time=total_all_time)

@app.route('/reports/all-entries')
def report_all_entries():
    tasks = task_manager.get_all_tasks()
    tasks.sort(key=lambda t: t.date, reverse=True)
    total_time = sum(task.hours for task in tasks)
    return render_template('report_all_entries.html', tasks=tasks, task_manager=task_manager, total_time=total_time)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            task_manager.create_customer(name)
            flash(f'Customer "{name}" created successfully!', 'success')
        else:
            flash('Customer name cannot be empty.', 'error')
        return redirect(url_for('customers'))
    
    customers = task_manager.get_all_customers()
    return render_template('customers.html', customers=customers, task_manager=task_manager)

@app.route('/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        customer_id = request.form.get('customer_id', '').strip()
        if name and customer_id:
            task_manager.create_department(name, customer_id)
            flash(f'Department "{name}" created successfully!', 'success')
        else:
            flash('Department name and customer are required.', 'error')
        return redirect(url_for('departments'))
    
    customers = task_manager.get_all_customers()
    departments = task_manager.get_all_departments()
    return render_template('departments.html', customers=customers, departments=departments, task_manager=task_manager)

@app.route('/api/departments')
def api_departments():
    customer_id = request.args.get('customer_id')
    if not customer_id:
        return jsonify([])
    departments = task_manager.get_departments_for_customer(customer_id)
    return jsonify([d.to_dict() for d in departments])

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page showing dashboard and task creation form."""
    if request.method == 'POST':
        customer_id = request.form.get('customer_id', '').strip()
        department_id = request.form.get('department_id', '').strip()
        date = request.form.get('date', '').strip()
        hours = request.form.get('hours', '').strip()
        description = request.form.get('description', '').strip()
        
        if not customer_id or not department_id or not date or not hours:
            flash('Customer, department, date, and hours are required.', 'error')
        else:
            try:
                hours_float = float(hours)
                task = task_manager.create_task(
                    customer_id=customer_id,
                    department_id=department_id,
                    date=date,
                    hours=hours_float,
                    description=description
                )
                flash(f'Task created successfully!', 'success')
                return redirect(url_for('index'))
            except ValueError:
                flash('Hours must be a valid number.', 'error')

    tasks = task_manager.get_all_tasks()
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    
    # Stats
    total_tasks = len(tasks)
    total_hours = sum(task.hours for task in tasks)
    total_customers = len(task_manager.get_all_customers())

    return render_template('index.html', 
                         tasks=tasks[:10], 
                         total_tasks=total_tasks,
                         total_hours=total_hours,
                         total_customers=total_customers,
                         task_manager=task_manager)

@app.route('/tasks')
def list_tasks():
    """List all tasks."""
    tasks = task_manager.get_all_tasks()
    tasks.sort(key=lambda t: t.date, reverse=True)
    total_time = sum(task.hours for task in tasks)
    return render_template('report_all_entries.html', tasks=tasks, task_manager=task_manager, total_time=total_time)

@app.route('/tasks/<task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit an existing task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found.', 'error')
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
                flash('Hours must be a valid number.', 'error')
                return render_template('edit_task.html', task=task)

        description = request.form.get('description', '').strip()
        if description: updates['description'] = description
        
        if updates:
            updated_task = task_manager.update_task(task_id, **updates)
            flash(f'Task for {updated_task.customer_id} updated successfully!', 'success')
        
        return redirect(url_for('list_tasks'))
    
    return render_template('edit_task.html', task=task, customers=task_manager.get_all_customers(), departments=task_manager.get_all_departments())

@app.route('/tasks/<task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """Delete a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found.', 'error')
        return redirect(url_for('list_tasks'))
    
    task_customer_id = task.customer_id
    if task_manager.delete_task(task_id):
        flash(f'Task for customer {task_customer_id} deleted successfully!', 'success')
    else:
        flash('Failed to delete task.', 'error')
    
    return redirect(url_for('list_tasks'))

@app.route('/reports')
def reports():
    """Show time reports."""
    return render_template('reports.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
