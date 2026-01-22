from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

@dataclass
class Conflict:
    """Represents a rail network conflict or incident"""
    id: str
    type: str  # e.g., 'schedule_clash', 'resource_contention', 'safety_violation'
    severity: float  # 0.0 to 1.0
    timestamp: datetime
    affected_resources: List[str]  # Train IDs, track segments, etc.
    metadata: Dict[str, Any]  # Additional context-specific data
    
    def __str__(self) -> str:
        return f"Conflict({self.id}, {self.type}, severity={self.severity})"