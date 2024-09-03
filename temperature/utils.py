import requests


def get_location_key(city_name, api_key):
    base_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        'apikey': api_key,
        'q': city_name,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and len(data) > 0:
        return data[0]['Key']


def get_city_temperature(location_key, api_key):
    base_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
    params = {
        'apikey': api_key,
        'details': 'true'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and len(data) > 0:
        temperature = data[0]['Temperature']['Metric']['Value']
        return temperature


api_key = "lUjc5nMDM7fqrMcDcK4ohOIG1JEgUULD"
