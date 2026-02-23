from fastapi import APIRouter, Depends, HTTPException
from app.core.security import verify_api_key
from app.services.elastic_client import search
from app.core.config import ES_INDEX
from app.schemas.responses import (
    EventsByTypeResponse,
    EventsByTypeItem,
    ActiveUsersResponse,
    ActivityWindowsResponse,
    ActivityWindowItem,
    EventCountResponse
)


router = APIRouter(prefix="/metrics", dependencies=[Depends(verify_api_key)])

@router.get("/active-users",response_model=ActiveUsersResponse)
def active_users():
    query = {
        "size": 0,
        "query": {
            "range": {
                "event_count": {
                    "gt": 0
                }
            }
        },
        "aggs": {
            "active_windows": {
                "value_count": {
                    "field": "window_start.keyword"
                }
            }
        }
    }

    result = search(ES_INDEX, query)

    return ActiveUsersResponse(
        active_users=result["aggregations"]["active_windows"]["value"],
        definition="Active windows with event_count > 0"
    )
@router.get("/events-by-type", response_model=EventsByTypeResponse)
def events_by_type():
    query = {
        "size": 0,
        "aggs": {
            "events_by_type": {
                "terms": {
                    "field": "event_type.keyword"
                },
                "aggs": {
                    "total_events": {
                        "sum": {
                            "field": "event_count"
                        }
                    }
                }
            }
        }
    }

    result = search(ES_INDEX, query)

    items = [
        EventsByTypeItem(
            event_type=bucket["key"],
            events=int(bucket["total_events"]["value"])
        )
        for bucket in result["aggregations"]["events_by_type"]["buckets"]
    ]

    return EventsByTypeResponse(results=items)



@router.get(
    "/activity-windows",
    response_model=ActivityWindowsResponse
)
def activity_windows():
    query = {
        "size": 0,
        "aggs": {
            "activity_windows": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "hour"
                },
                "aggs": {
                    "events": {
                        "sum": {
                            "field": "event_count"
                        }
                    }
                }
            }
        }
    }

    result = search(ES_INDEX, query)

    items = [
        ActivityWindowItem(
            window=bucket["key_as_string"],
            events=int(bucket["events"]["value"])
        )
        for bucket in result["aggregations"]["activity_windows"]["buckets"]
    ]

    return ActivityWindowsResponse(results=items)


@router.get("/event-count",response_model=EventCountResponse)
def event_count():
    query = {"size": 0}
    result = search(ES_INDEX, query)
    return {"events": result["hits"]["total"]["value"]}