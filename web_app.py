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
from time_tracker import TimeTracker, TimeEntry

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this for production

# Initialize managers
task_manager = TaskManager()
time_tracker = TimeTracker()

@app.route('/')
def dashboard():
    """Main dashboard showing overview of tasks and active timer."""
    tasks = task_manager.get_all_tasks()
    active_entry = time_tracker.get_active_entry()
    
    # Get statistics
    active_tasks = [t for t in tasks if t.status == 'active']
    completed_tasks = [t for t in tasks if t.status == 'completed']
    total_time_today = 0
    
    # Calculate today's time
    today = datetime.now().date()
    all_entries = time_tracker.get_all_time_entries()
    for entry in all_entries:
        entry_date = datetime.fromisoformat(entry.start_time).date()
        if entry_date == today and entry.end_time:
            total_time_today += entry.get_duration_hours()
    
    # Add active timer time if it's from today
    if active_entry:
        start_time = datetime.fromisoformat(active_entry.start_time)
        if start_time.date() == today:
            current_duration = datetime.now() - start_time
            total_time_today += current_duration.total_seconds() / 3600.0
    
    return render_template('dashboard.html', 
                         tasks=tasks,
                         active_tasks=active_tasks,
                         completed_tasks=completed_tasks,
                         active_entry=active_entry,
                         task_manager=task_manager,
                         total_time_today=total_time_today)

@app.route('/tasks')
def list_tasks():
    """List all tasks with filtering options."""
    customer_filter = request.args.get('customer', '')
    project_filter = request.args.get('project', '')
    status_filter = request.args.get('status', '')
    
    tasks = task_manager.get_all_tasks()
    
    # Apply filters
    if customer_filter:
        tasks = [t for t in tasks if t.customer.lower() == customer_filter.lower()]
    if project_filter:
        tasks = [t for t in tasks if t.project.lower() == project_filter.lower()]
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]
    
    # Sort by creation date (most recent first)
    tasks.sort(key=lambda t: t.created_at, reverse=True)
    
    # Get unique customers and projects for filter dropdowns
    all_customers = task_manager.get_customers()
    all_projects = task_manager.get_projects()
    
    return render_template('tasks.html', 
                         tasks=tasks,
                         time_tracker=time_tracker,
                         customers=all_customers,
                         projects=all_projects,
                         current_customer=customer_filter,
                         current_project=project_filter,
                         current_status=status_filter)

@app.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    """Create a new task."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        customer = request.form.get('customer', '').strip()
        project = request.form.get('project', '').strip()
        estimated_hours = float(request.form.get('estimated_hours', 0) or 0)
        
        if not title:
            flash('Task title is required', 'error')
            return render_template('create_task.html')
        
        if not customer:
            flash('Customer name is required', 'error')
            return render_template('create_task.html')
        
        if not project:
            flash('Project name is required', 'error')
            return render_template('create_task.html')
        
        task = task_manager.create_task(
            title=title,
            description=description,
            customer=customer,
            project=project,
            estimated_hours=estimated_hours
        )
        
        flash(f'Task "{task.title}" created successfully!', 'success')
        return redirect(url_for('list_tasks'))
    
    return render_template('create_task.html')

@app.route('/tasks/<task_id>')
def view_task(task_id):
    """View task details."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    # Get time entries for this task
    time_entries = time_tracker.get_time_entries_for_task(task_id)
    time_entries.sort(key=lambda e: e.start_time, reverse=True)
    
    total_time = time_tracker.get_total_time_for_task(task_id)
    
    return render_template('view_task.html', 
                         task=task, 
                         time_entries=time_entries,
                         total_time=total_time)

@app.route('/tasks/<task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task."""
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('list_tasks'))
    
    if request.method == 'POST':
        updates = {}
        
        title = request.form.get('title', '').strip()
        if title: updates['title'] = title
        
        description = request.form.get('description', '').strip()
        if description is not None: updates['description'] = description
        
        customer = request.form.get('customer', '').strip()
        if customer: updates['customer'] = customer
        
        project = request.form.get('project', '').strip()
        if project: updates['project'] = project
        
        status = request.form.get('status', '').strip()
        if status and status in ['active', 'completed', 'paused']:
            updates['status'] = status
        
        estimated_hours = request.form.get('estimated_hours', '').strip()
        if estimated_hours:
            try:
                updates['estimated_hours'] = float(estimated_hours)
            except ValueError:
                pass
        
        if updates:
            updated_task = task_manager.update_task(task_id, **updates)
            flash(f'Task "{updated_task.title}" updated successfully!', 'success')
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
        flash(f'Task "{task.title}" deleted successfully!', 'success')
    else:
        flash('Failed to delete task', 'error')
    
    return redirect(url_for('list_tasks'))

@app.route('/timer')
def timer_page():
    """Timer management page."""
    active_entry = time_tracker.get_active_entry()
    active_tasks = [t for t in task_manager.get_all_tasks() if t.status == 'active']
    
    return render_template('timer.html', 
                         active_entry=active_entry,
                         active_tasks=active_tasks,
                         task_manager=task_manager,
                         time_tracker=time_tracker)

@app.route('/timer/start', methods=['POST'])
def start_timer():
    """Start timer for a task."""
    task_id = request.form.get('task_id')
    description = request.form.get('description', '').strip()
    
    if not task_id:
        flash('Please select a task', 'error')
        return redirect(url_for('timer_page'))
    
    task = task_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('timer_page'))
    
    # Check if there's already an active timer
    active_entry = time_tracker.get_active_entry()
    if active_entry:
        # Stop the current timer
        time_tracker.stop_timer()
    
    # Start new timer
    entry = time_tracker.start_timer(task_id, description)
    flash(f'Timer started for "{task.title}"', 'success')
    
    return redirect(url_for('timer_page'))

@app.route('/timer/stop', methods=['POST'])
def stop_timer():
    """Stop the active timer."""
    active_entry = time_tracker.get_active_entry()
    if not active_entry:
        flash('No active timer to stop', 'error')
        return redirect(url_for('timer_page'))
    
    completed_entry = time_tracker.stop_timer()
    if completed_entry:
        duration_hours = completed_entry.get_duration_hours()
        task = task_manager.get_task(completed_entry.task_id)
        task_title = task.title if task else "Unknown Task"
        flash(f'Timer stopped! Duration: {duration_hours:.2f} hours for "{task_title}"', 'success')
    else:
        flash('Failed to stop timer', 'error')
    
    return redirect(url_for('timer_page'))

@app.route('/api/timer/status')
def timer_status():
    """API endpoint to get current timer status."""
    active_entry = time_tracker.get_active_entry()
    if not active_entry:
        return jsonify({'active': False})
    
    task = task_manager.get_task(active_entry.task_id)
    start_time = datetime.fromisoformat(active_entry.start_time)
    elapsed_seconds = int((datetime.now() - start_time).total_seconds())
    
    return jsonify({
        'active': True,
        'task_title': task.title if task else "Unknown Task",
        'start_time': active_entry.start_time,
        'elapsed_seconds': elapsed_seconds,
        'description': active_entry.description
    })

@app.route('/reports')
def reports():
    """Reports overview page."""
    return render_template('reports.html')

@app.route('/reports/tasks')
def report_tasks():
    """Task time report."""
    tasks = task_manager.get_all_tasks()
    tasks_with_time = []
    
    for task in tasks:
        total_time = time_tracker.get_total_time_for_task(task.id)
        if total_time > 0:
            tasks_with_time.append({
                'task': task,
                'total_time': total_time,
                'percentage': 0  # Will be calculated below
            })
    
    # Sort by time spent (descending)
    tasks_with_time.sort(key=lambda x: x['total_time'], reverse=True)
    
    # Calculate percentages
    total_all_time = sum(item['total_time'] for item in tasks_with_time)
    if total_all_time > 0:
        for item in tasks_with_time:
            item['percentage'] = (item['total_time'] / total_all_time) * 100
    
    return render_template('report_tasks.html', 
                         tasks_with_time=tasks_with_time,
                         total_time=total_all_time)

@app.route('/reports/customers')
def report_customers():
    """Customer time report."""
    customers = task_manager.get_customers()
    customer_data = []
    
    for customer in customers:
        tasks = task_manager.get_tasks_by_customer(customer)
        total_time = sum(time_tracker.get_total_time_for_task(task.id) for task in tasks)
        if total_time > 0:
            customer_data.append({
                'customer': customer,
                'total_time': total_time,
                'task_count': len(tasks),
                'percentage': 0
            })
    
    # Sort by time spent (descending)
    customer_data.sort(key=lambda x: x['total_time'], reverse=True)
    
    # Calculate percentages
    total_all_time = sum(item['total_time'] for item in customer_data)
    if total_all_time > 0:
        for item in customer_data:
            item['percentage'] = (item['total_time'] / total_all_time) * 100
    
    return render_template('report_customers.html', 
                         customer_data=customer_data,
                         total_time=total_all_time)

@app.route('/reports/projects')
def report_projects():
    """Project time report."""
    projects = task_manager.get_projects()
    project_data = []
    
    for project in projects:
        tasks = task_manager.get_tasks_by_project(project)
        total_time = sum(time_tracker.get_total_time_for_task(task.id) for task in tasks)
        if total_time > 0:
            project_data.append({
                'project': project,
                'total_time': total_time,
                'task_count': len(tasks),
                'percentage': 0
            })
    
    # Sort by time spent (descending)
    project_data.sort(key=lambda x: x['total_time'], reverse=True)
    
    # Calculate percentages
    total_all_time = sum(item['total_time'] for item in project_data)
    if total_all_time > 0:
        for item in project_data:
            item['percentage'] = (item['total_time'] / total_all_time) * 100
    
    return render_template('report_projects.html', 
                         project_data=project_data,
                         total_time=total_all_time)

@app.route('/reports/entries')
def report_entries():
    """All time entries report."""
    entries = time_tracker.get_all_time_entries()
    
    # Sort by start time (most recent first)
    entries.sort(key=lambda e: e.start_time, reverse=True)
    
    # Add task information to entries
    entries_with_tasks = []
    total_time = 0
    
    for entry in entries:
        task = task_manager.get_task(entry.task_id)
        duration = entry.get_duration_hours() if entry.end_time else 0
        total_time += duration
        
        entries_with_tasks.append({
            'entry': entry,
            'task': task,
            'duration': duration
        })
    
    return render_template('report_entries.html', 
                         entries_with_tasks=entries_with_tasks,
                         total_time=total_time)

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
