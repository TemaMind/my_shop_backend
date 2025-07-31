from pydantic import BaseModel, Field
from typing import Optional

class InfoParams(BaseModel):
    category: Optional[str] = Field(None, description="Filter by category name")
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
