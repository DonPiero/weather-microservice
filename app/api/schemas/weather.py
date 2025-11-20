from pydantic import BaseModel
from typing import Optional, List


class LiveWeatherRequest(BaseModel):
    city_name: str


class HistoryWeatherRequest(BaseModel):
    city_name: str
    start_time: str
    end_time: str


class WeatherLiveResponse(BaseModel):
    city_name: str
    temperature: float
    weather_description: str
    humidity: float
    wind_speed: Optional[float]
    timestamp: str


class WeatherHistoryResponse(BaseModel):
    readings: List[WeatherLiveResponse]
