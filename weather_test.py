import pytest
import requests
from FlaskCode.Weather import Weather, openWeather

@pytest.fixture
def mock_weather_data():
    data = {
        "weather": [{"description": "sunny", "icon": "01d"}],
        "main": {"temp": 20, "feels_like": 22, "pressure": 1010, "humidity": 50},
        "wind": {"speed": 5, "deg": 180}
    }
    return data

def test_weather_class(mock_weather_data):
    weather = Weather(
        mock_weather_data["weather"][0]["description"],
        mock_weather_data["main"]["temp"],
        mock_weather_data["main"]["feels_like"],
        mock_weather_data["main"]["pressure"],
        mock_weather_data["main"]["humidity"],
        mock_weather_data["wind"]["speed"],
        mock_weather_data["wind"]["deg"],
        f"http://openweathermap.org/img/wn/{mock_weather_data['weather'][0]['icon']}.png"
    )
    
    assert weather.description == "sunny"
    assert weather.temp == 20
    assert weather.feels_like == 22
    assert weather.pressure == 1010
    assert weather.humidity == 50
    assert weather.wind_speed == 5
    assert weather.wind_direction == 180
    assert weather.icon == "http://openweathermap.org/img/wn/01d.png"

def test_open_weather(mock_weather_data, monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data
            
            def json(self):
                return self.json_data
        
        return MockResponse(mock_weather_data)
    
    monkeypatch.setattr(requests, "get", mock_get)
    
    weather = openWeather("testcity")
    
    assert weather.description == "sunny"
    assert weather.temp == 20
    assert weather.feels_like == 22
    assert weather.pressure == 1010
    assert weather.humidity == 50
    assert weather.wind_speed == 5
    assert weather.wind_direction == 180
    assert weather.icon == "http://openweathermap.org/img/wn/01d.png"
