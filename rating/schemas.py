from typing import List, Optional
from pydantic import BaseModel


class RatingBase(BaseModel):
    user_id:int
    owner_id:int
    rating:int