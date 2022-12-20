from webapp.cache import *
import requests
import json


def get_covid_api_data():
    covid_data = {}
    # Covid key to save in cache
    covid_cache_key = "COVID19_ALL_STATS"
    permanent_covid_cache_key = "COVID19_ALL_STATS_PERMANENT"

    # Fetch Covid cache data
    covid_cache_data = cache.get(covid_cache_key)

    # If cached covid data is not found
    if not covid_cache_data:
        try:
            # Fetch fresh data
            covid_fresh_data = get_covid_web_widget_data()

            # Cache news for half day
            cache.set(covid_cache_key, covid_fresh_data, 1 * 60 * 60 * 6 )
            cache.set(permanent_covid_cache_key, covid_fresh_data, None)

        except Exception as e:
            permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
            covid_fresh_data = permanent_covid_cache_data
    else:
        covid_fresh_data = covid_cache_data

    # if fresh data is available
    if covid_fresh_data:
        covid_data = covid_fresh_data
    return covid_data


def get_covid_web_widget_data():
    permanent_covid_cache_key = "COVID19_ALL_STATS_PERMANENT"
    covid_data = {}

    # Fetching india vaccinated data
    try:
        ind_total_vaccinated_url = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports"
        ind_total_vaccinated_response = requests.request("GET", ind_total_vaccinated_url)
        ind_total_vaccinated_response_data = ind_total_vaccinated_response.json()
        ind_total_vaccinated = ind_total_vaccinated_response_data["topBlock"]["vaccination"]["tot_dose_2"]
        covid_data['ind_total_vaccinated'] = ind_total_vaccinated
    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['ind_total_vaccinated'] = permanent_covid_cache_data['ind_total_vaccinated']

    try:
        # Fetching odisha vaccinated data
        odisa_total_vaccinated_url = "https://api.cowin.gov.in/api/v1/reports/v2/getPublicReports?state_id=26"
        odisa_total_vaccinated_response = requests.request("GET", odisa_total_vaccinated_url)
        odisa_total_vaccinateds_response_data = odisa_total_vaccinated_response.json()
        odisa_total_vaccinated = odisa_total_vaccinateds_response_data["topBlock"]["vaccination"]["tot_dose_2"]
        covid_data['odisa_total_vaccinated'] = odisa_total_vaccinated
    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['odisa_total_vaccinated'] = permanent_covid_cache_data['odisa_total_vaccinated']

    # Fetching india and odisha covid data.
    try:
        ind_odisha_covid_data_url = "https://www.mohfw.gov.in/data/datanew.json"
        ind_odisha_covid_data_response = requests.request("GET", ind_odisha_covid_data_url)
        ind_covid_data = ind_odisha_covid_data_response.json()[-1]
        covid_data['india_active_cases'] = ind_covid_data['active']
        covid_data['india_total_cases'] = ind_covid_data['positive']
        covid_data['india_recovered_cases'] = ind_covid_data['cured']
        covid_data['india_death_cases'] = ind_covid_data['death']

        odisha_covid_cases = list(filter(lambda x: x if 'state_name' in x.keys() and x["state_name"] == "Odisha" else None, ind_odisha_covid_data_response.json()))[0]
        covid_data['odisha_active_cases'] = odisha_covid_cases['active']
        covid_data['odisha_death_cases'] = odisha_covid_cases['death']
        covid_data['odisha_total_cases'] = odisha_covid_cases['positive']
        covid_data['odisha_recovered_cases'] = odisha_covid_cases['cured']

    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['india_active_cases'] = permanent_covid_cache_data['india_active_cases']
        covid_data['india_total_cases'] = permanent_covid_cache_data['india_total_cases']
        covid_data['india_recovered_cases'] = permanent_covid_cache_data['india_recovered_cases']
        covid_data['india_death_cases'] = permanent_covid_cache_data['india_death_cases']
        covid_data['odisha_active_cases'] = permanent_covid_cache_data['odisha_active_cases']
        covid_data['odisha_death_cases'] = permanent_covid_cache_data['odisha_death_cases']
        covid_data['odisha_total_cases'] = permanent_covid_cache_data['odisha_total_cases']
        covid_data['odisha_recovered_cases'] = permanent_covid_cache_data['odisha_recovered_cases']

    # Fetching world covid data.
    try:
        world_covid_data_url = "https://coronavirus-19-api.herokuapp.com/countries/world"
        world_covid_data_response = requests.request("GET", world_covid_data_url)
        world_covid_data = world_covid_data_response.json()
        covid_data['world_active_cases'] = world_covid_data['active']
        covid_data['world_total_cases'] = world_covid_data['cases']
        covid_data['world_recovered_cases'] = world_covid_data['recovered']
        covid_data['world_death_cases'] = world_covid_data['deaths']

    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['world_active_cases'] = permanent_covid_cache_data['world_active_cases']
        covid_data['world_total_cases'] = permanent_covid_cache_data['world_total_cases']
        covid_data['world_recovered_cases'] = permanent_covid_cache_data['world_recovered_cases']
        covid_data['world_death_cases'] = permanent_covid_cache_data['world_death_cases']

    # Fetching world covid data(active cases).
    try:
        world_active_data_url = "https://coronavirus-19-api.herokuapp.com/countries/world"
        world_active_data_response = requests.request("GET", world_active_data_url)
        world_active_covid_data = world_active_data_response.json()
        covid_data['world_active_cases'] = world_active_covid_data['active']
    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['world_active_cases'] = permanent_covid_cache_data['world_active_cases']

    try:
        # Fetching world vaccinated data.
        world_total_vaccinated_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
        world_total_vaccinated_response = requests.request("GET", world_total_vaccinated_url)
        world_total_vaccinated_response_data = world_total_vaccinated_response.json()
        world_vac = list(filter(lambda x: x if 'country' in x.keys() and x["country"] == "World" else None,
                                world_total_vaccinated_response_data))
        world_fully_vaccinated = world_vac[0]['data'][-1]['people_fully_vaccinated']
        covid_data['world_fully_vaccinated'] = world_fully_vaccinated
    except Exception as e:
        permanent_covid_cache_data = cache.get(permanent_covid_cache_key)
        covid_data['world_fully_vaccinated'] = permanent_covid_cache_data['world_fully_vaccinated']
    return covid_data