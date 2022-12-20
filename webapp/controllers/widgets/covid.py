from webapp.cache import *
import requests
import json


def fetch_covid_api_data():
    covid_data = {}
    # Covid key to save in cache
    covid_cache_key = "COVID19_ODISHA_STATS"

    # Fetch Covid cache data
    covid_cache_data = cache.get(covid_cache_key)

    # If cached covid data is not found
    if not covid_cache_data:
        try:
            # Fetch fresh data
            covid_fresh_data = get_india_covid_stats_data()

            # Cache news for half day
            cache.set(covid_cache_key, covid_fresh_data, 1 * 60 * 60 * 12)
        except Exception as e:
            covid_fresh_data = covid_cache_data
    else:
        covid_fresh_data = covid_cache_data

    # if fresh data is available
    if covid_fresh_data:
        for entry in covid_fresh_data:
            # Fetch state info for each entry
            state = entry.get("state", None)

            # We need only Odisha statistics
            if state == "Odisha":
                covid_data["total"] = str(entry.get("confirmed", 0))
                active = int(entry.get("active", 0))
                covid_data["active"] = active
                delta = int(entry.get("deltaconfirmed", 0))
                covid_data["delta"] = delta

    return covid_data


def get_india_covid_stats_data():
    """
        Method fetches Covid stats from Covid19India website
        in JSON format and returns data state-wise.
    """
    url = 'https://api.covid19india.org/data.json'

    r = requests.get(url)
    response = json.loads(r.text)

    # fetch state-wise data
    state_wise_data = response['statewise']
    return state_wise_data
