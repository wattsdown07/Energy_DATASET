import requests
import datetime

api_key = "YOUR_OWM_API_KEY"
lat = 36.8    # Latitude for Tunis, Tunisia (example)
lon = 10.18   # Longitude for Tunis, Tunisia (example)

url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric"
response = requests.get(url)
weather_data = response.json()

print("Hourly Weather Data for Energy Optimization:")
for hour in weather_data.get('hourly', []):
    timestamp = datetime.datetime.fromtimestamp(hour['dt'])
    temp = hour.get('temp')
    humidity = hour.get('humidity')
    uvi = hour.get('uvi')
    wind_speed = hour.get('wind_speed')
    wind_deg = hour.get('wind_deg')
    clouds = hour.get('clouds')
    pressure = hour.get('pressure')
    rain = hour.get('rain', {}).get('1h', 0)  # mm rainfall in last hour, may be absent
    snow = hour.get('snow', {}).get('1h', 0)  # mm snowfall in last hour, may be absent

    print(f"Time: {timestamp} | Temp: {temp}°C | Humidity: {humidity}% | UV: {uvi} | Wind: {wind_speed} m/s @ {wind_deg}° |"
          f" Clouds: {clouds}% | Pressure: {pressure} hPa | Rain: {rain} mm | Snow: {snow} mm")