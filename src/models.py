from pydantic import BaseModel, Field, validator
from typing import Optional
import datetime

class WeatherRecord(BaseModel):
    city: str
    temperature_c: float
    humidity_pct: int = Field(ge=0, le=100)
    timestamp: datetime.datetime
    status: str

    @validator('temperature_c', pre=True)
    def check_valid_temp(cls, v):
        if v is None:
            raise ValueError("Temperature cannot be null")
        if not (-50 <= v <= 60):
            raise ValueError("Temperature out of realistic bounds")
        return v