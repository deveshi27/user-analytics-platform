from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime


class Event(BaseModel):
    event_id: Optional[str] = Field(
        default=None, description="Unique event identifier"
    )
    user_id: str = Field(..., description="User who generated the event")
    event_type: str = Field(..., description="Type of event (click, view, purchase)")
    source: str = Field(..., description="Event source (web, mobile)")
    event_time: datetime = Field(..., description="Time when event occurred")
    metadata: Dict[str, str] = Field(
        default_factory=dict, description="Additional event attributes"
    )
