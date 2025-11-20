from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timezone
from typing import Optional


class WeatherData(BaseModel):
    email: EmailStr
    city_name: str
    temperature: float
    weather_description: str
    humidity: float
    wind_speed: Optional[float] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WeatherHistory(BaseModel):
    email: EmailStr
    city_name: str
    start_time: datetime
    end_time: datetime

