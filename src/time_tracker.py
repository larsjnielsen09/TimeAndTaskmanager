"""
Time Tracker - Handle time tracking for tasks
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from uuid import uuid4

@dataclass
class TimeEntry:
    """Time entry data model."""
    id: str
    task_id: str
    start_time: str
    end_time: Optional[str]
    description: str
    duration_seconds: int = 0
    
    def to_dict(self) -> Dict:
        """Convert time entry to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TimeEntry':
        """Create time entry from dictionary."""
        return cls(**data)
    
    def get_duration_hours(self) -> float:
        """Get duration in hours."""
        return self.duration_seconds / 3600.0

class TimeTracker:
    """Manages time tracking for tasks."""
    
    def __init__(self, data_file: str = "data/time_entries.json"):
        """Initialize time tracker with data file."""
        self.data_file = data_file
        self.time_entries: Dict[str, TimeEntry] = {}
        self.active_entry: Optional[TimeEntry] = None
        self.load_time_entries()
    
    def load_time_entries(self) -> None:
        """Load time entries from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.time_entries = {
                        entry_id: TimeEntry.from_dict(entry_data)
                        for entry_id, entry_data in data.items()
                    }
                    
                    # Check for active entry (end_time is None)
                    for entry in self.time_entries.values():
                        if entry.end_time is None:
                            self.active_entry = entry
                            break
                            
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading time entries: {e}")
                self.time_entries = {}
    
    def save_time_entries(self) -> None:
        """Save time entries to JSON file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            data = {entry_id: entry.to_dict() for entry_id, entry in self.time_entries.items()}
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def start_timer(self, task_id: str, description: str = "") -> TimeEntry:
        """Start tracking time for a task."""
        if self.active_entry:
            # Stop current timer first
            self.stop_timer()
        
        entry_id = str(uuid4())
        start_time = datetime.now().isoformat()
        
        time_entry = TimeEntry(
            id=entry_id,
            task_id=task_id,
            start_time=start_time,
            end_time=None,
            description=description,
            duration_seconds=0
        )
        
        self.time_entries[entry_id] = time_entry
        self.active_entry = time_entry
        self.save_time_entries()
        return time_entry
    
    def stop_timer(self) -> Optional[TimeEntry]:
        """Stop the currently active timer."""
        if not self.active_entry:
            return None
        
        end_time = datetime.now()
        start_time = datetime.fromisoformat(self.active_entry.start_time)
        duration = end_time - start_time
        
        self.active_entry.end_time = end_time.isoformat()
        self.active_entry.duration_seconds = int(duration.total_seconds())
        
        completed_entry = self.active_entry
        self.active_entry = None
        self.save_time_entries()
        return completed_entry
    
    def get_active_entry(self) -> Optional[TimeEntry]:
        """Get the currently active time entry."""
        return self.active_entry
    
    def get_time_entries_for_task(self, task_id: str) -> List[TimeEntry]:
        """Get all time entries for a specific task."""
        return [entry for entry in self.time_entries.values() if entry.task_id == task_id]
    
    def get_all_time_entries(self) -> List[TimeEntry]:
        """Get all time entries."""
        return list(self.time_entries.values())
    
    def get_total_time_for_task(self, task_id: str) -> float:
        """Get total time spent on a task in hours."""
        entries = self.get_time_entries_for_task(task_id)
        total_seconds = sum(entry.duration_seconds for entry in entries)
        
        # Add time from active entry if it's for this task
        if self.active_entry and self.active_entry.task_id == task_id:
            start_time = datetime.fromisoformat(self.active_entry.start_time)
            current_duration = datetime.now() - start_time
            total_seconds += int(current_duration.total_seconds())
        
        return total_seconds / 3600.0
    
    def delete_time_entry(self, entry_id: str) -> bool:
        """Delete a time entry."""
        if entry_id in self.time_entries:
            entry = self.time_entries[entry_id]
            if entry == self.active_entry:
                self.active_entry = None
            del self.time_entries[entry_id]
            self.save_time_entries()
            return True
        return False
    
    def update_time_entry(self, entry_id: str, **kwargs) -> Optional[TimeEntry]:
        """Update a time entry."""
        if entry_id not in self.time_entries:
            return None
        
        entry = self.time_entries[entry_id]
        
        # Update allowed fields
        allowed_fields = ['description', 'start_time', 'end_time']
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(entry, field):
                setattr(entry, field, value)
        
        # Recalculate duration if times changed
        if 'start_time' in kwargs or 'end_time' in kwargs:
            if entry.end_time:
                start = datetime.fromisoformat(entry.start_time)
                end = datetime.fromisoformat(entry.end_time)
                entry.duration_seconds = int((end - start).total_seconds())
        
        self.save_time_entries()
        return entry
