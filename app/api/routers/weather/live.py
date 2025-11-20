from fastapi import APIRouter, Depends, HTTPException

from app.api.errors import error_500
from app.api.schemas.weather import LiveWeatherRequest, WeatherLiveResponse
from app.api.deps import get_user_from_token, get_connection_to_grpc
from app.core.config import settings
from app.services.rpc import weather_pb2


router = APIRouter(prefix="/weather", tags=["weather"])

@router.post("/live", response_model=WeatherLiveResponse)
async def get_live_weather(
    live_weather_parameters: LiveWeatherRequest,
    current_user=Depends(get_user_from_token),
    stub=Depends(get_connection_to_grpc),
):
    try:
        response = await stub.GetWeather(
            weather_pb2.WeatherRequest(city_name=live_weather_parameters.city_name),
            metadata=(("x-api-key", settings.grpc_api_key),
                      ("user-email", current_user.email)),
        )

        return WeatherLiveResponse(
            city_name=response.city_name,
            temperature=response.temperature,
            weather_description=response.weather_description,
            humidity=response.humidity,
            wind_speed=response.wind_speed,
            timestamp=response.timestamp
        )

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Error fetching live weather for {live_weather_parameters.city_name}: {e}")
