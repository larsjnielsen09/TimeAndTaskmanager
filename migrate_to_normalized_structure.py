#!/usr/bin/env python3
"""
Migration script to convert existing task data from string-based customer/department 
to normalized structure with separate Customer and Department tables.
"""

import json
import os
import sys
from datetime import datetime
import shutil

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from task_manager import TaskManager, Task, CustomerManager, Customer, DepartmentManager, Department

def backup_existing_data():
    """Create backups of existing data files."""
    backup_dir = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = ['data/tasks.json']
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_path = os.path.join(backup_dir, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            print(f"✓ Backed up {file_path} to {backup_path}")
    
    return backup_dir

def migrate_data():
    """Migrate existing task data to normalized structure."""
    print("🔄 Starting data migration to normalized structure...")
    
    # Create backup first
    backup_dir = backup_existing_data()
    print(f"✓ Data backed up to {backup_dir}")
    
    try:
        # Initialize managers
        customer_manager = CustomerManager()
        department_manager = DepartmentManager()
        
        # Load existing tasks directly from JSON to avoid format issues
        tasks_file = 'data/tasks.json'
        if not os.path.exists(tasks_file):
            print("ℹ️  No existing tasks file found. Migration not needed.")
            return
            
        with open(tasks_file, 'r', encoding='utf-8') as f:
            raw_task_data = json.load(f)
        
        print(f"📋 Found {len(raw_task_data)} existing tasks")
        
        if not raw_task_data:
            print("ℹ️  No existing tasks found. Migration not needed.")
            return
        
        # Extract unique customers and departments
        customer_names = set()
        department_by_customer = {}
        
        for task_id, task_data in raw_task_data.items():
            # Check if task needs migration (has old format)
            if 'customer' in task_data and 'customer_id' not in task_data:
                customer_name = task_data.get('customer', 'Unknown')
                department_name = task_data.get('department', 'General')
            else:
                # Task already in new format, skip
                continue
                
            customer_names.add(customer_name)
            
            if customer_name not in department_by_customer:
                department_by_customer[customer_name] = set()
            department_by_customer[customer_name].add(department_name)
        
        print(f"👥 Found {len(customer_names)} unique customers")
        print(f"🏢 Found departments for {len(department_by_customer)} customers")
        
        # Create customers
        customer_map = {}  # customer_name -> customer_id
        for customer_name in customer_names:
            customer = customer_manager.create_customer(name=customer_name)
            customer_map[customer_name] = customer.id
            print(f"✓ Created customer: {customer_name}")
        
        # Create departments
        department_map = {}  # (customer_name, department_name) -> department_id
        for customer_name, departments in department_by_customer.items():
            customer_id = customer_map[customer_name]
            for department_name in departments:
                department = department_manager.create_department(
                    name=department_name,
                    customer_id=customer_id
                )
                department_map[(customer_name, department_name)] = department.id
                print(f"✓ Created department: {department_name} for {customer_name}")
        
        # Convert tasks to new structure
        converted_count = 0
        converted_tasks = {}
        
        for task_id, task_data in raw_task_data.items():
            # Check if task needs conversion
            if 'customer' in task_data and 'customer_id' not in task_data:
                customer_name = task_data.get('customer', 'Unknown')
                department_name = task_data.get('department', 'General')
                
                # Get IDs for the new structure
                customer_id = customer_map.get(customer_name)
                department_id = department_map.get((customer_name, department_name))
                
                if customer_id and department_id:
                    # Create new task data with normalized structure
                    new_task_data = {
                        'id': task_data['id'],
                        'customer_id': customer_id,
                        'department_id': department_id,
                        'date': task_data.get('date', ''),
                        'hours': task_data.get('hours', 0.0),
                        'description': task_data.get('description', ''),
                        'created_at': task_data.get('created_at', ''),
                        'updated_at': task_data.get('updated_at', '')
                    }
                    
                    converted_tasks[task_id] = new_task_data
                    converted_count += 1
                    print(f"✓ Converted task {task_id} for {customer_name}/{department_name}")
                else:
                    print(f"⚠️  Could not find IDs for task {task_id} ({customer_name}/{department_name})")
            else:
                # Task already in new format, keep as-is
                converted_tasks[task_id] = task_data
        
        # Save converted tasks directly to JSON
        os.makedirs(os.path.dirname(tasks_file), exist_ok=True)
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(converted_tasks, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Migration completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Customers created: {len(customer_names)}")
        print(f"   - Departments created: {sum(len(depts) for depts in department_by_customer.values())}")
        print(f"   - Tasks converted: {converted_count}")
        print(f"   - Backup location: {backup_dir}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print(f"💡 You can restore from backup: {backup_dir}")
        raise

def verify_migration():
    """Verify that migration was successful."""
    print("\n🔍 Verifying migration...")
    
    try:
        task_manager = TaskManager()
        customer_manager = CustomerManager()
        department_manager = DepartmentManager()
        
        tasks = task_manager.get_all_tasks()
        customers = customer_manager.get_all_customers()
        departments = department_manager.get_all_departments()
        
        print(f"✓ Found {len(customers)} customers")
        print(f"✓ Found {len(departments)} departments")
        print(f"✓ Found {len(tasks)} tasks")
        
        # Check that all tasks have valid references
        invalid_tasks = 0
        for task in tasks:
            if not hasattr(task, 'customer_id') or not hasattr(task, 'department_id'):
                print(f"⚠️  Task {task.id} still has old structure")
                invalid_tasks += 1
            else:
                customer = customer_manager.get_customer(task.customer_id)
                department = department_manager.get_department(task.department_id)
                if not customer:
                    print(f"⚠️  Task {task.id} references non-existent customer {task.customer_id}")
                    invalid_tasks += 1
                if not department:
                    print(f"⚠️  Task {task.id} references non-existent department {task.department_id}")
                    invalid_tasks += 1
        
        if invalid_tasks == 0:
            print("✅ All tasks have valid references!")
        else:
            print(f"⚠️  Found {invalid_tasks} tasks with invalid references")
        
        return invalid_tasks == 0
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Time and Task Manager - Data Migration Tool")
    print("=" * 50)
    
    # Run migration
    migrate_data()
    
    # Verify migration
    if verify_migration():
        print("\n🎉 Migration completed successfully!")
        print("You can now run the web application with the new normalized structure.")
    else:
        print("\n⚠️  Migration completed but verification found issues.")
        print("Please check the output above and consider running the migration again.")
