"""
Data models for Customer and Department
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from uuid import uuid4

@dataclass
class Customer:
    """Customer data model."""
    id: str
    name: str
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert customer to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        """Create customer from dictionary."""
        return cls(**data)

@dataclass
class Department:
    """Department data model."""
    id: str
    name: str
    customer_id: str
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert department to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Department':
        """Create department from dictionary."""
        return cls(**data)
