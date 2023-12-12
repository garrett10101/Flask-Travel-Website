import requests
import os
from dotenv import load_dotenv
import datetime
load_dotenv()

class Weather:
    def __init__(self, date, description, temp, feels_like, pressure, humidity, wind_speed, wind_direction, icon):
        self.date = date
        self.description = description
        self.temp = temp
        self.feels_like = feels_like
        self.pressure = pressure
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.icon = icon

def openWeather(city_name):
    weather_api_key = os.getenv('weather_api_key')

    # Retrieve 5-day forecast data
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Parse forecast data for each of the next 5 days
    forecasts = []
    #set start_date to current datetime
    start_date = datetime.datetime.now()
    #set end_date to 5 days from now
    end_date = start_date + datetime.timedelta(days=5)
    print(start_date)
    print(end_date)
    for forecast_data in data['list']:
        #check if forecast is within the next 5 days
        forecast_date = datetime.datetime.strptime(forecast_data['dt_txt'], '%Y-%m-%d %H:%M:%S')
        print(forecast_date)
        if forecast_date >= start_date or forecast_date <= end_date:
            #check if forecast_date day is the same as the previous forecast_date day, if so skip
            if forecast_date.day == start_date.day:
                continue
                #check if forecast_date time is between 6am and 6pm, if not skip
            if forecast_date.time() < datetime.time(6, 0, 0) or forecast_date.time() > datetime.time(18, 0, 0):
                continue
            #set start_date to current forecast_date
            start_date = forecast_date
            date = forecast_data['dt_txt']
            description = forecast_data['weather'][0]['description']
            temp = forecast_data['main']['temp']
            feels_like = forecast_data['main']['feels_like']
            pressure = forecast_data['main']['pressure']
            humidity = forecast_data['main']['humidity']
            wind_speed = forecast_data['wind']['speed']
            wind_direction = forecast_data['wind']['deg']
            icon = f"http://openweathermap.org/img/wn/{forecast_data['weather'][0]['icon']}.png"

            # Create Weather object for the forecast
            weather = Weather(date, description, temp, feels_like, pressure, humidity, wind_speed, wind_direction, icon)
            forecasts.append(weather)
    return forecasts