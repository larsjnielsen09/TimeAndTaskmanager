"""
Task Manager - Handle CRUD operations for tasks and projects
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from uuid import uuid4

@dataclass
class Task:
    """Task data model."""
    id: str
    title: str
    description: str
    customer: str
    project: str
    status: str  # 'active', 'completed', 'paused'
    created_at: str
    updated_at: str
    estimated_hours: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create task from dictionary."""
        return cls(**data)

class TaskManager:
    """Manages CRUD operations for tasks and projects."""
    
    def __init__(self, data_file: str = "data/tasks.json"):
        """Initialize task manager with data file."""
        self.data_file = data_file
        self.tasks: Dict[str, Task] = {}
        self.load_tasks()
    
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
    
    def create_task(self, title: str, description: str, customer: str, 
                   project: str, estimated_hours: float = 0.0) -> Task:
        """Create a new task."""
        task_id = str(uuid4())
        now = datetime.now().isoformat()
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            customer=customer,
            project=project,
            status='active',
            created_at=now,
            updated_at=now,
            estimated_hours=estimated_hours
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
    
    def get_tasks_by_customer(self, customer: str) -> List[Task]:
        """Get all tasks for a specific customer."""
        return [task for task in self.tasks.values() if task.customer == customer]
    
    def get_tasks_by_project(self, project: str) -> List[Task]:
        """Get all tasks for a specific project."""
        return [task for task in self.tasks.values() if task.project == project]
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update a task."""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        # Update allowed fields
        allowed_fields = ['title', 'description', 'customer', 'project', 'status', 'estimated_hours']
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
    
    def get_customers(self) -> List[str]:
        """Get list of unique customers."""
        return list(set(task.customer for task in self.tasks.values()))
    
    def get_projects(self) -> List[str]:
        """Get list of unique projects."""
        return list(set(task.project for task in self.tasks.values()))
