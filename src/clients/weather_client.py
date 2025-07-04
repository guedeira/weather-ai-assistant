import requests
from src.config.settings import OPENWEATHER_API_KEY


class WeatherClient:
    def __init__(self):
        self.api_key = OPENWEATHER_API_KEY
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'
    
    def get_weather(self, city):
        '''
        Get current weather data for a city.
        '''
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'pt_br'
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Erro ao buscar clima: {response.status_code}')
            return None
