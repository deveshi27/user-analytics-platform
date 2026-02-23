from pydantic import BaseModel
from typing import List


# -----------------------------
# /metrics/active-users
# -----------------------------
class ActiveUsersResponse(BaseModel):
    active_users: int
    definition: str


# -----------------------------
# /metrics/events-by-type
# -----------------------------
class EventsByTypeItem(BaseModel):
    event_type: str
    events: int


class EventsByTypeResponse(BaseModel):
    results: List[EventsByTypeItem]


# -----------------------------
# /metrics/activity-windows
# -----------------------------
class ActivityWindowItem(BaseModel):
    window: str
    events: int


class ActivityWindowsResponse(BaseModel):
    results: List[ActivityWindowItem]


# -----------------------------
# /metrics/event-count
# -----------------------------
class EventCountResponse(BaseModel):
    events: int