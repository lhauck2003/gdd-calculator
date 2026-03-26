import time
from time import strftime
from datetime import datetime, time, timedelta
import requests
from .cache.states import states, states_map

from .urls import (
    NOAA_BASE_API
)

def active_date(weeks=2):
    return strftime("%Y-%m-%d",(datetime.now() - timedelta(weeks=weeks)).timetuple())

def get_state_by_abbr(state_abbr):
    return states_map[state_abbr]

def get_stateid_by_state(state_name: str):
    state_data = states["results"]

    for state in state_data:
        if state_name.strip().lower() in state["name"].strip().lower():
            return state["id"]
    
    return ""

def get_stateid_by_abbr(state_abbr):
    state_name = get_state_by_abbr(state_abbr)
    return get_stateid_by_state(state_name)