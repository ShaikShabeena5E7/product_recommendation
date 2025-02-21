from pydantic import BaseModel
from typing import List

class UserRequest(BaseModel):
    user_id: int
    browsing_history: List[str]
