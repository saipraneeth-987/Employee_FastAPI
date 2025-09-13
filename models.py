# models.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date, datetime
from dateutil import parser

class Employee(BaseModel):
    employee_id: str = Field(..., example="E123")
    name: str = Field(..., example="John Doe")
    department: str = Field(..., example="Engineering")
    salary: float = Field(..., example=75000)
    joining_date: date = Field(..., example="2023-01-15")
    skills: List[str] = Field(..., example=["Python", "MongoDB", "APIs"])

    @validator("skills", pre=True)
    def ensure_list_of_strings(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @validator("joining_date", pre=True)
    def ensure_datetime(cls, v):
        if isinstance(v, str):  # parse string
            v = parser.parse(v).date()
        if isinstance(v, datetime):  # already datetime
            return v
        if isinstance(v, date):  # convert to datetime
            return datetime.combine(v, datetime.min.time())
        return v

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None

    @validator("skills", pre=True)
    def ensure_list_of_strings(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @validator("joining_date", pre=True)
    def ensure_datetime(cls, v):
        if isinstance(v, str):
            v = parser.parse(v).date()
        if isinstance(v, datetime):
            return v
        if isinstance(v, date):
            return datetime.combine(v, datetime.min.time())
        return v
