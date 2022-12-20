from webapp.cache import *
import requests
import json


def fetch_weather_api_data(user):
    # weather key to save in cache
    weather_cache_key = "WEATHER_ODISHA_DATA"

    # fetch weather cache data
    weather_cache_data = cache.get(weather_cache_key)

    # if cached weather data is not found
    if not weather_cache_data:
        try:
            # Fetch fresh data
            weather_fresh_data = get_weather_data(user)

            # Cache weather for 15 minutes
            cache.set(weather_cache_key, weather_fresh_data, 1 * 60 * 15)
        except Exception as e:
            weather_fresh_data = weather_cache_data
    else:
        weather_fresh_data = weather_cache_data

    weather_data = weather_fresh_data

    return weather_data


def get_weather_data(user):
    api_key = "c8a2fcd539d3521ecf9950f0e09a86e2"

    # latitude and longitude of Bhubaneshwar is used by default
    lat = "20.2961"
    lon = "85.8245"

    # ToDo: Uncomment this code later (not required for this release)

    # if user:
    #     if user.lat and user.long:
    #         lat = str(user.lat)
    #         lon = str(user.long)

    # Open weather API URL
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Currently we fetch data using latitude and longitude
    weather_url = base_url + "?lat=" + lat + "&lon=" + lon + "&appid=" + api_key + "&units=metric"
    r = requests.get(weather_url)
    response = None

    # if successful
    if r.status_code == 200:
        response = json.loads(r.text)

    # Not empty check
    if response:

        # get weather info from response
        weather_info = response.get("weather", None)
        short_description = ""
        weather_icon_code = None

        '''
            Since we have implemented custom weather icons,
            and API has their own weather icons, hence we
            use a dictionary to map from their data to our data
        '''
        custom_icons_dict = get_custom_icons_dict()
        custom_web_icons_dict = get_web_custom_icons_dict()

        # Not empty check
        if weather_info:
            # Fetch weather icon code from API response
            weather_icon_code = weather_info[0].get("icon", None)
            weather_icon_code = str(weather_icon_code)

            # Fetch description from API response
            short_description = weather_info[0].get("description", None)

        # Use the custom_icons_dict dictionary to use custom image
        weather_icon_url = "/static/img/" + custom_icons_dict.get(weather_icon_code, None) + ".svg"
        web_weather_icon_url = "/app/static/img/web_weather_icons/" + custom_web_icons_dict.get(weather_icon_code, None) + ".svg"

        # Fetch city name
        city_name = str(response.get("name", ""))

        # Fetch temperature
        temperature = response.get("main", None).get("temp", None)

        return {
            "city_name": city_name,
            "temperature": temperature,
            "icon_url": weather_icon_url,
            "short_description": short_description,
            "web_weather_icon_url": web_weather_icon_url
        }
    else:
        return {}


def get_custom_icons_dict():
    """
        Since we have implemented custom weather icons,
        and API has their own weather icons, hence we
        use a dictionary to map from their data to our data
        NOTE: The value is the image name we use in Weather widget.
    """

    return {
        "01d": "clear_sky",
        "01n": "clear_sky",
        "02d": "few_clouds",
        "02n": "few_clouds",
        "03d": "scattered_clouds",
        "03n": "scattered_clouds",
        "04d": "broken_clouds",
        "04n": "broken_clouds",
        "09d": "shower_rain",
        "09n": "shower_rain",
        "10d": "rain",
        "10n": "rain",
        "11d": "thunderstorm",
        "11n": "thunderstorm",
        "13d": "snow",
        "13n": "snow",
        "50d": "mist",
        "50n": "mist",
    }


def get_web_custom_icons_dict():
    return {
        "01d": "clear_sky_day",
        "01n": "clear_sky_night",
        "02d": "few_clouds_day",
        "02n": "few_clouds_night",
        "03d": "scattered_clouds",
        "03n": "scattered_clouds",
        "04d": "broken_clouds",
        "04n": "broken_clouds",
        "09d": "shower_rain_day",
        "09n": "shower_rain_night",
        "10d": "rain",
        "10n": "rain",
        "11d": "thunderstorm",
        "11n": "thunderstorm",
        "13d": "snow",
        "13n": "snow",
        "50d": "mist",
        "50n": "mist",
    }