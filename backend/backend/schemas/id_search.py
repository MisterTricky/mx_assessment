from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class HolidayBase(BaseModel):
    name: str
    description: Optional[str] = None
    date: datetime
    type: Optional[str] = None

class HolidayCreate(HolidayBase):
    pass

class Holiday(HolidayBase):
    id: int
    id_search_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class IDSearchBase(BaseModel):
    id_number: str = Field(..., description="South African ID number")
    date_of_birth: datetime
    gender: str
    citizen: bool
    search_count: int = Field(default=1)

class IDSearchCreate(IDSearchBase):
    pass

class IDSearch(IDSearchBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    holidays: List[Holiday] = []

    class Config:
        from_attributes = True

class IDSearchResponse(BaseModel):
    id_number: str
    date_of_birth: str
    gender: str
    citizen: bool
    search_count: int
    holidays: List[Holiday]
