#!/usr/bin/env python3
"""
Data migration script for Time and Task Manager
Converts old task structure to new structure
"""

import json
import os
import shutil
from datetime import datetime

def backup_data():
    """Create backup of existing data files"""
    data_dir = "data"
    backup_dir = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if os.path.exists(data_dir):
        shutil.copytree(data_dir, backup_dir)
        print(f"✅ Backup created: {backup_dir}")
        return True
    
    print("ℹ️  No existing data directory found")
    return False

def migrate_tasks():
    """Migrate tasks from old structure to new structure"""
    tasks_file = "data/tasks.json"
    
    if not os.path.exists(tasks_file):
        print("ℹ️  No tasks file found, nothing to migrate")
        return
    
    # Load old tasks
    with open(tasks_file, 'r', encoding='utf-8') as f:
        old_tasks = json.load(f)
    
    new_tasks = {}
    
    for task_id, old_task in old_tasks.items():
        # Map old structure to new structure
        new_task = {
            "id": task_id,
            "customer": old_task.get("customer", "Unknown Customer"),
            "department": old_task.get("project", "General"),  # Map project to department
            "date": datetime.now().strftime("%Y-%m-%d"),  # Use today's date as default
            "hours": old_task.get("estimated_hours", 1.0),  # Use estimated hours as actual hours
            "description": old_task.get("title", "") + 
                          (" - " + old_task.get("description", "") if old_task.get("description") else ""),
            "created_at": old_task.get("created_at", datetime.now().isoformat()),
            "updated_at": old_task.get("updated_at", datetime.now().isoformat())
        }
        
        new_tasks[task_id] = new_task
    
    # Save migrated tasks
    with open(tasks_file, 'w', encoding='utf-8') as f:
        json.dump(new_tasks, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Migrated {len(new_tasks)} tasks to new structure")

def main():
    """Main migration function"""
    print("=== Time and Task Manager Data Migration ===")
    print("Converting tasks to new structure: customer, department, date, hours, description")
    print()
    
    # Create backup
    backup_created = backup_data()
    
    if backup_created:
        print("⚠️  This will modify your existing task data!")
        confirm = input("Continue with migration? (y/N): ").strip().lower()
        
        if confirm != 'y':
            print("Migration cancelled")
            return
    
    # Migrate tasks
    migrate_tasks()
    
    print()
    print("✅ Migration completed successfully!")
    print("🗑️  You can delete the time entries file (data/time_entries.json) since we're no longer tracking time")
    print()
    print("The new task structure is:")
    print("- Customer: Client/customer name")
    print("- Department: Department or area of work (mapped from old 'project')")
    print("- Date: Date the work was performed")
    print("- Hours: Number of hours worked")
    print("- Description: Description of work performed (combined old title + description)")

if __name__ == "__main__":
    main()
