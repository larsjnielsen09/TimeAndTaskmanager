"""
Task Manager - Handle CRUD operations for tasks and projects
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from uuid import uuid4
from .models import Customer, Department

@dataclass
class Task:
    """Task data model."""
    id: str
    customer_id: str
    department_id: str
    date: str
    hours: float
    description: str
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary."""
        return cls(**data)

class TaskManager:
    """Manages CRUD operations for tasks and projects."""
    
    def __init__(self, data_file: str = "data/tasks.json", 
                 customers_file: str = "data/customers.json",
                 departments_file: str = "data/departments.json"):
        """Initialize task manager with data files."""
        self.data_file = data_file
        self.customers_file = customers_file
        self.departments_file = departments_file
        self.tasks: Dict[str, Task] = {}
        self.customers: Dict[str, Customer] = {}
        self.departments: Dict[str, Department] = {}
        self.load_tasks()
        self.load_customers()
        self.load_departments()
    
    def load_tasks(self) -> None:
        """Load tasks from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = {
                        task_id: Task.from_dict(task_data)
                        for task_id, task_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = {}
    
    def save_tasks(self) -> None:
        """Save tasks to JSON file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            data = {task_id: task.to_dict() for task_id, task in self.tasks.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_task(self, customer_id: str, department_id: str, 
                   date: str, hours: float, description: str = "") -> Task:
        """Create a new task."""
        task_id = str(uuid4())
        now = datetime.now().isoformat()
        
        task = Task(
            id=task_id,
            customer_id=customer_id,
            department_id=department_id,
            date=date,
            hours=hours,
            description=description,
            created_at=now,
            updated_at=None
        )
        
        self.tasks[task_id] = task
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return list(self.tasks.values())
    
    def get_tasks_by_customer(self, customer_id: str) -> List[Task]:
        """Get all tasks for a specific customer."""
        return [task for task in self.tasks.values() if task.customer_id == customer_id]
    
    def get_tasks_by_project(self, department_id: str) -> List[Task]:
        """Get all tasks for a specific project/department."""
        return [task for task in self.tasks.values() if task.department_id == department_id]
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update a task."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        # Update allowed fields
        allowed_fields = ['customer_id', 'department_id', 'date', 'hours', 'description']
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(task, field):
                setattr(task, field, value)
        
        task.updated_at = datetime.now().isoformat()
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_tasks()
            return True
        return False
    
    
    def get_projects(self) -> List[str]:
        """Get list of unique projects (departments)."""
        return list(set(task.department_id for task in self.tasks.values()))
    
    # Customer management methods
    def load_customers(self) -> None:
        """Load customers from JSON file."""
        if os.path.exists(self.customers_file):
            try:
                with open(self.customers_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.customers = {
                        customer_id: Customer.from_dict(customer_data)
                        for customer_id, customer_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading customers: {e}")
                self.customers = {}
    
    def save_customers(self) -> None:
        """Save customers to JSON file."""
        os.makedirs(os.path.dirname(self.customers_file), exist_ok=True)
        with open(self.customers_file, 'w', encoding='utf-8') as f:
            data = {customer_id: customer.to_dict() for customer_id, customer in self.customers.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_customer(self, name: str) -> Customer:
        """Create a new customer."""
        customer_id = str(uuid4())
        now = datetime.now().isoformat()
        
        customer = Customer(
            id=customer_id,
            name=name,
            created_at=now,
            updated_at=None
        )
        
        self.customers[customer_id] = customer
        self.save_customers()
        return customer
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        return list(self.customers.values())
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        return self.customers.get(customer_id)
    
    # Department management methods
    def load_departments(self) -> None:
        """Load departments from JSON file."""
        if os.path.exists(self.departments_file):
            try:
                with open(self.departments_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.departments = {
                        department_id: Department.from_dict(department_data)
                        for department_id, department_data in data.items()
                    }
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading departments: {e}")
                self.departments = {}
    
    def save_departments(self) -> None:
        """Save departments to JSON file."""
        os.makedirs(os.path.dirname(self.departments_file), exist_ok=True)
        with open(self.departments_file, 'w', encoding='utf-8') as f:
            data = {department_id: department.to_dict() for department_id, department in self.departments.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_department(self, name: str, customer_id: str) -> Department:
        """Create a new department."""
        department_id = str(uuid4())
        now = datetime.now().isoformat()
        
        department = Department(
            id=department_id,
            name=name,
            customer_id=customer_id,
            created_at=now,
            updated_at=None
        )
        
        self.departments[department_id] = department
        self.save_departments()
        return department
    
    def get_all_departments(self) -> List[Department]:
        """Get all departments."""
        return list(self.departments.values())
    
    def get_department(self, department_id: str) -> Optional[Department]:
        """Get a department by ID."""
        return self.departments.get(department_id)
    
    def get_departments_for_customer(self, customer_id: str) -> List[Department]:
        """Get all departments for a specific customer."""
        return [dept for dept in self.departments.values() if dept.customer_id == customer_id]
