from fastapi import APIRouter, Depends, HTTPException

from app.api.errors import error_500
from app.api.schemas.weather import HistoryWeatherRequest, WeatherLiveResponse, WeatherHistoryResponse
from app.api.deps import get_user_from_token, get_connection_to_grpc
from app.core.config import settings
from app.services.rpc import weather_pb2


router = APIRouter(prefix="/weather", tags=["weather"])

@router.post("/history", response_model=WeatherHistoryResponse)
async def get_history_weather(
    history_weather_parameters: HistoryWeatherRequest,
    current_user=Depends(get_user_from_token),
    stub=Depends(get_connection_to_grpc),
):
    try:
        response = await stub.GetWeatherHistory(
            weather_pb2.WeatherHistoryRequest(
                city_name=history_weather_parameters.city_name,
                start_time=history_weather_parameters.start_time,
                end_time=history_weather_parameters.end_time,
            ),
            metadata=(("x-api-key", settings.grpc_api_key),
                      ("user-email", current_user.email)),
        )
        readings = [
            WeatherLiveResponse(
                city_name=r.city_name,
                temperature=r.temperature,
                weather_description=r.weather_description,
                humidity=r.humidity,
                wind_speed=r.wind_speed,
                timestamp=r.timestamp
            )
            for r in response.readings
        ]
        return WeatherHistoryResponse(readings=readings)

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Error fetching weather history for {history_weather_parameters.city_name}: {e}")