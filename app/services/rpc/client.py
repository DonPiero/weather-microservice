import grpc
from datetime import datetime

from app.core.config import settings
from app.services.rpc import weather_pb2, weather_pb2_grpc


def format_weather_entry(entry):
    return (
        f"{entry.city_name.title()} — {entry.timestamp}\n"
        f"Temp: {entry.temperature:.1f} °C\n"
        f"Humidity: {entry.humidity}%\n"
        f"Conditions: {entry.weather_description}\n"
        f"Wind: {entry.wind_speed} m/s\n"
    )


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = weather_pb2_grpc.WeatherServiceStub(channel)

    print("Weather CLI — type 'exit' to quit.")
    print("Commands:")
    print("live <city> → get current weather")
    print("history <city> → get weather history\n")

    while True:
        raw = input("> ").strip()
        if not raw:
            continue
        if raw.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        parts = raw.split(maxsplit=1)
        if len(parts) == 1:
            print("Please provide a city name.")
            continue

        cmd, city = parts[0].lower(), parts[1].strip()

        try:
            if cmd == "live":
                resp = stub.GetWeather(weather_pb2.WeatherRequest(city_name=city), metadata=(
                    ("x-api-key", settings.grpc_api_key),
                    ("user-email", "razvan.petru.leonte@gmail.com"),
                ))
                print(format_weather_entry(resp))

            elif cmd == "history":
                start = input("Start date (YYYY-MM-DD): ").strip()
                end = input("End date (YYYY-MM-DD): ").strip()
                try:
                    datetime.fromisoformat(start)
                    datetime.fromisoformat(end)
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.\n")
                    continue

                resp = stub.GetWeatherHistory(
                    weather_pb2.WeatherHistoryRequest(city_name=city, start_time=start, end_time=end),
                    metadata=(
                        ("x-api-key", settings.grpc_api_key),
                        ("user-email", "razvan.petru.leonte@gmail.com"),
                    )
                )

                if not resp.readings:
                    print(f"No history for {city} in that range.\n")
                    continue

                index = 0
                while index < len(resp.readings):
                    print(format_weather_entry(resp.readings[index]))
                    index += 1
                print("\n")
            else:
                print("Unknown command. Use 'live' or 'history'.\n")

        except grpc.RpcError as e:
            print(f"gRPC Server Error: {e} \n")


if __name__ == "__main__":
    run()
