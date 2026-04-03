from pydantic import BaseModel
from typing import Optional, Dict, List

class Observation(BaseModel):
    ticket_id: str
    message: str
    customer_tier: str
    history: List[str]
    status: str

class Action(BaseModel):
    action_type: str  # classify | respond | route | close
    category: Optional[str] = None
    priority: Optional[str] = None
    response: Optional[str] = None
    route_to: Optional[str] = None

class Reward(BaseModel):
    score: float
    breakdown: Dict[str, float]
    done: bool