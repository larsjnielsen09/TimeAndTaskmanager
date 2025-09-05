"""
CLI Interface - Command line interface for the time and task manager
"""

import sys
from typing import Optional
from datetime import datetime
from task_manager import TaskManager, Task
from time_tracker import TimeTracker, TimeEntry

class CLIInterface:
    """Command line interface for the time and task manager."""
    
    def __init__(self, task_manager: TaskManager, time_tracker: TimeTracker):
        """Initialize CLI with task manager and time tracker."""
        self.task_manager = task_manager
        self.time_tracker = time_tracker
    
    def run(self) -> None:
        """Run the main CLI loop."""
        while True:
            self.show_main_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.create_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.start_timer()
            elif choice == '6':
                self.stop_timer()
            elif choice == '7':
                self.view_time_reports()
            elif choice == '8':
                print("Thank you for using Time and Task Manager!")\
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def show_main_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("TIME AND TASK MANAGER")
        print("="*50)
        
        # Show active timer if any
        active_entry = self.time_tracker.get_active_entry()
        if active_entry:
            task = self.task_manager.get_task(active_entry.task_id)
            task_title = task.title if task else "Unknown Task"
            start_time = datetime.fromisoformat(active_entry.start_time)
            elapsed = datetime.now() - start_time
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            print(f"⏱️  TIMER ACTIVE: {task_title} ({hours}h {minutes}m)")
            print("-"*50)
        
        print("1. Create new task")
        print("2. List all tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Start timer")
        print("6. Stop timer")
        print("7. View time reports")
        print("8. Exit")
    
    def create_task(self) -> None:
        """Create a new task."""
        print("\n--- CREATE NEW TASK ---")
        
        title = input("Task title: ").strip()
        if not title:
            print("Task title is required.")
            return
        
        description = input("Task description: ").strip()
        customer = input("Customer name: ").strip()
        if not customer:
            print("Customer name is required.")
            return
        
        project = input("Project name: ").strip()
        if not project:
            print("Project name is required.")
            return
        
        try:
            estimated_hours = float(input("Estimated hours (optional, default 0): ").strip() or "0")
        except ValueError:
            estimated_hours = 0.0
        
        task = self.task_manager.create_task(
            title=title,
            description=description,
            customer=customer,
            project=project,
            estimated_hours=estimated_hours
        )
        
        print(f"\n✅ Task created successfully!")
        print(f"Task ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Customer: {task.customer}")
        print(f"Project: {task.project}")
    
    def list_tasks(self) -> None:
        """List all tasks."""
        print("\n--- ALL TASKS ---")
        
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks found.")
            return
        
        # Sort tasks by creation date (most recent first)
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        
        for i, task in enumerate(tasks, 1):
            total_time = self.time_tracker.get_total_time_for_task(task.id)
            status_emoji = "✅" if task.status == "completed" else "⏸️" if task.status == "paused" else "🔄"
            
            print(f"\n{i}. {status_emoji} {task.title}")
            print(f"   ID: {task.id}")
            print(f"   Customer: {task.customer}")
            print(f"   Project: {task.project}")
            print(f"   Status: {task.status}")
            print(f"   Time spent: {total_time:.2f}h")
            if task.estimated_hours > 0:
                print(f"   Estimated: {task.estimated_hours:.2f}h")
            if task.description:
                print(f"   Description: {task.description}")
    
    def update_task(self) -> None:
        """Update an existing task."""
        print("\n--- UPDATE TASK ---")
        
        task_id = input("Enter task ID to update: ").strip()
        task = self.task_manager.get_task(task_id)
        
        if not task:
            print("Task not found.")
            return
        
        print(f"\nCurrent task: {task.title}")
        print("Leave fields empty to keep current values.")
        
        title = input(f"Title ({task.title}): ").strip()
        description = input(f"Description ({task.description}): ").strip()
        customer = input(f"Customer ({task.customer}): ").strip()
        project = input(f"Project ({task.project}): ").strip()
        status = input(f"Status ({task.status}) [active/completed/paused]: ").strip()
        
        try:
            est_hours_input = input(f"Estimated hours ({task.estimated_hours}): ").strip()
            estimated_hours = float(est_hours_input) if est_hours_input else None
        except ValueError:
            estimated_hours = None
        
        # Build update dictionary
        updates = {}
        if title: updates['title'] = title
        if description: updates['description'] = description
        if customer: updates['customer'] = customer
        if project: updates['project'] = project
        if status and status in ['active', 'completed', 'paused']: updates['status'] = status
        if estimated_hours is not None: updates['estimated_hours'] = estimated_hours
        
        if updates:
            updated_task = self.task_manager.update_task(task_id, **updates)
            print(f"\n✅ Task updated successfully!")
            print(f"Title: {updated_task.title}")
        else:
            print("No changes made.")
    
    def delete_task(self) -> None:
        """Delete a task."""
        print("\n--- DELETE TASK ---")
        
        task_id = input("Enter task ID to delete: ").strip()
        task = self.task_manager.get_task(task_id)
        
        if not task:
            print("Task not found.")
            return
        
        print(f"\nTask to delete: {task.title}")
        print(f"Customer: {task.customer}")
        print(f"Project: {task.project}")
        
        confirm = input("\nAre you sure you want to delete this task? (y/N): ").strip().lower()
        
        if confirm == 'y':
            if self.task_manager.delete_task(task_id):
                print("✅ Task deleted successfully!")
            else:
                print("❌ Failed to delete task.")
        else:
            print("Task deletion cancelled.")
    
    def start_timer(self) -> None:
        """Start timing a task."""
        print("\n--- START TIMER ---")
        
        # Check if there's already an active timer
        active_entry = self.time_tracker.get_active_entry()
        if active_entry:
            task = self.task_manager.get_task(active_entry.task_id)
            task_title = task.title if task else "Unknown Task"
            print(f"Timer already active for: {task_title}")
            stop_current = input("Stop current timer and start new one? (y/N): ").strip().lower()
            if stop_current != 'y':
                return
        
        # List tasks to choose from
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks available. Please create a task first.")
            return
        
        print("\nAvailable tasks:")
        active_tasks = [task for task in tasks if task.status == 'active']
        
        if not active_tasks:
            print("No active tasks available.")
            return
        
        for i, task in enumerate(active_tasks, 1):
            print(f"{i}. {task.title} - {task.customer}/{task.project}")
        
        try:
            choice = int(input("\nSelect task number: ").strip())
            if 1 <= choice <= len(active_tasks):
                selected_task = active_tasks[choice - 1]
                description = input("Work description (optional): ").strip()
                
                entry = self.time_tracker.start_timer(selected_task.id, description)
                print(f"\n✅ Timer started for: {selected_task.title}")
                print(f"Start time: {datetime.fromisoformat(entry.start_time).strftime('%H:%M:%S')}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def stop_timer(self) -> None:
        """Stop the active timer."""
        print("\n--- STOP TIMER ---")
        
        active_entry = self.time_tracker.get_active_entry()
        if not active_entry:
            print("No active timer to stop.")
            return
        
        task = self.task_manager.get_task(active_entry.task_id)
        task_title = task.title if task else "Unknown Task"
        
        print(f"Stopping timer for: {task_title}")
        
        completed_entry = self.time_tracker.stop_timer()
        if completed_entry:
            duration_hours = completed_entry.get_duration_hours()
            print(f"\n✅ Timer stopped!")
            print(f"Duration: {duration_hours:.2f} hours")
            print(f"Start: {datetime.fromisoformat(completed_entry.start_time).strftime('%H:%M:%S')}")
            print(f"End: {datetime.fromisoformat(completed_entry.end_time).strftime('%H:%M:%S')}")
        else:
            print("❌ Failed to stop timer.")
    
    def view_time_reports(self) -> None:
        """View time reports."""
        print("\n--- TIME REPORTS ---")
        print("1. Report by task")
        print("2. Report by customer")
        print("3. Report by project")
        print("4. All time entries")
        
        choice = input("\nSelect report type (1-4): ").strip()
        
        if choice == '1':
            self.report_by_task()
        elif choice == '2':
            self.report_by_customer()
        elif choice == '3':
            self.report_by_project()
        elif choice == '4':
            self.report_all_entries()
        else:
            print("Invalid choice.")
    
    def report_by_task(self) -> None:
        """Generate report by task."""
        print("\n--- TIME REPORT BY TASK ---")
        
        tasks = self.task_manager.get_all_tasks()
        if not tasks:
            print("No tasks found.")
            return
        
        tasks_with_time = []
        for task in tasks:
            total_time = self.time_tracker.get_total_time_for_task(task.id)
            if total_time > 0:
                tasks_with_time.append((task, total_time))
        
        if not tasks_with_time:
            print("No time entries found.")
            return
        
        # Sort by time spent (descending)
        tasks_with_time.sort(key=lambda x: x[1], reverse=True)
        
        total_all_time = sum(time for _, time in tasks_with_time)
        
        for task, total_time in tasks_with_time:
            print(f"\n📋 {task.title}")
            print(f"   Customer: {task.customer}")
            print(f"   Project: {task.project}")
            print(f"   Time spent: {total_time:.2f}h")
            if task.estimated_hours > 0:
                percentage = (total_time / task.estimated_hours) * 100
                print(f"   Estimated: {task.estimated_hours:.2f}h ({percentage:.1f}%)")
        
        print(f"\n📊 TOTAL TIME: {total_all_time:.2f} hours")
    
    def report_by_customer(self) -> None:
        """Generate report by customer."""
        print("\n--- TIME REPORT BY CUSTOMER ---")
        
        customers = self.task_manager.get_customers()
        if not customers:
            print("No customers found.")
            return
        
        customer_times = {}
        for customer in customers:
            tasks = self.task_manager.get_tasks_by_customer(customer)
            total_time = sum(self.time_tracker.get_total_time_for_task(task.id) for task in tasks)
            if total_time > 0:
                customer_times[customer] = total_time
        
        if not customer_times:
            print("No time entries found.")
            return
        
        # Sort by time spent (descending)
        sorted_customers = sorted(customer_times.items(), key=lambda x: x[1], reverse=True)
        
        total_all_time = sum(customer_times.values())
        
        for customer, total_time in sorted_customers:
            print(f"\n👤 {customer}")
            print(f"   Total time: {total_time:.2f}h")
            percentage = (total_time / total_all_time) * 100
            print(f"   Percentage: {percentage:.1f}%")
        
        print(f"\n📊 TOTAL TIME: {total_all_time:.2f} hours")
    
    def report_by_project(self) -> None:
        """Generate report by project."""
        print("\n--- TIME REPORT BY PROJECT ---")
        
        projects = self.task_manager.get_projects()
        if not projects:
            print("No projects found.")
            return
        
        project_times = {}
        for project in projects:
            tasks = self.task_manager.get_tasks_by_project(project)
            total_time = sum(self.time_tracker.get_total_time_for_task(task.id) for task in tasks)
            if total_time > 0:
                project_times[project] = total_time
        
        if not project_times:
            print("No time entries found.")
            return
        
        # Sort by time spent (descending)
        sorted_projects = sorted(project_times.items(), key=lambda x: x[1], reverse=True)
        
        total_all_time = sum(project_times.values())
        
        for project, total_time in sorted_projects:
            print(f"\n📁 {project}")
            print(f"   Total time: {total_time:.2f}h")
            percentage = (total_time / total_all_time) * 100
            print(f"   Percentage: {percentage:.1f}%")
        
        print(f"\n📊 TOTAL TIME: {total_all_time:.2f} hours")
    
    def report_all_entries(self) -> None:
        """Show all time entries."""
        print("\n--- ALL TIME ENTRIES ---")
        
        entries = self.time_tracker.get_all_time_entries()
        if not entries:
            print("No time entries found.")
            return
        
        # Sort by start time (most recent first)
        entries.sort(key=lambda e: e.start_time, reverse=True)
        
        total_time = 0
        for entry in entries:
            task = self.task_manager.get_task(entry.task_id)
            task_title = task.title if task else "Unknown Task"
            
            duration = entry.get_duration_hours()
            total_time += duration
            
            start_time = datetime.fromisoformat(entry.start_time)
            status = "⏱️ Active" if entry.end_time is None else "✅ Completed"
            
            print(f"\n{status} - {task_title}")
            print(f"   Duration: {duration:.2f}h")
            print(f"   Date: {start_time.strftime('%Y-%m-%d %H:%M')}")
            if entry.description:
                print(f"   Description: {entry.description}")
        
        print(f"\n📊 TOTAL TIME: {total_time:.2f} hours")
