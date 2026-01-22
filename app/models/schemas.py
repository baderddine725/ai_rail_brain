from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

class RailEvent(BaseModel):
    """Base unit of memory: Everything is an event """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    modality: str  # 'telemetry', 'operator_text', 'signal_state' [cite: 7, 17]
    content: Dict[str, Any]
    location: str

class Conflict(BaseModel):
    """The formal object driving memory retrieval [cite: 48]"""
    conflict_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # 'headway', 'platform_overlap', 'track_congestion' [cite: 48]
    severity: int
    affected_trains: List[str]
    spatial_footprint: str
    temporal_window: Dict[str, datetime] # t_start, t_end [cite: 19]