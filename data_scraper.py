from datetime import date
import streamlit as st
import aiohttp
import asyncio
import data_processor
import requests

todays_date = date.today()
current_year = int(todays_date.year)

driver_standings_url = 'http://ergast.com/api/f1/{}/{}/driverStandings.json?limit=1000'
constructor_standings_url = 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'
driver_champs = 'http://ergast.com/api/f1/driverStandings/1/drivers.json?limit=1000'
constructor_champs = 'http://ergast.com/api/f1/constructorStandings/1/constructors.json?limit=1000'
driver_champ_wins = 'http://ergast.com/api/f1/drivers/{}/driverStandings/1/seasons.json?limit=1000'
constructor_champ_wins = 'http://ergast.com/api/f1/constructors/{}/constructorStandings/1/seasons.json?limit=1000'


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_champ_winners(competitor_type):
    if (competitor_type == 'driver'):
        response = requests.get(driver_champs)
        champs_df = data_processor.make_all_champs_df(response.json(), 'DriverTable', 'Drivers')
    else:
        response = requests.get(constructor_champs)
        champs_df = data_processor.make_all_champs_df(response.json(), 'ConstructorTable', 'Constructors')
    
    champs_list = data_processor.get_column_list(champs_df, competitor_type + "Id")
    champs = []

    champs = asyncio.run(get_champs(champs_list, competitor_type, champs))
    
    return data_processor.list_to_df(champs, [competitor_type + 'ID', 'number_wins'])
   

@st.cache(suppress_st_warning=True)
def get_points(year, competitor_type, season_length, competitor_df):
    # Returns a pandas DataFrame of the points scored by every driver/constructor
    # at every race in a given season.
    competitor_list = competitor_df[competitor_type + 'Id'].tolist()
    races = []

    # Async
    races = asyncio.run(get_races(season_length, competitor_type, year, races))
    race_dict = dict(zip(range(len(races)), races))

    return data_processor.build_points_df(competitor_list, competitor_type + 'ID', season_length, race_dict)


def get_race_tasks(session, season_length, competitor_type, year):
    # Creates a list of tasks for an async function.
    tasks = []
    for race in range(0, season_length):
        url = build_race_url(competitor_type, year, race)
        tasks.append(session.get(url, ssl=False))
    return tasks


async def get_races(season_length, competitor_type, year, races):
    # Makes API calls asynchronously to create a list of pandas DataFrames.
    async with aiohttp.ClientSession() as session:
        tasks = get_race_tasks(session, season_length, competitor_type, year)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if (competitor_type == 'driver'):
                standings_df = data_processor.make_driver_df(await response.json())
            else:
                standings_df = data_processor.make_constructor_df(await response.json())
            races.append(standings_df)
        return races


async def get_champs(champs, competitor_type, empty_champs):
    # Makes API calls asynchronously to create a list of pandas DataFrames.
    async with aiohttp.ClientSession() as session:
        tasks = get_champs_tasks(session, competitor_type, champs)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if (competitor_type == 'driver'):
                champs_df = data_processor.make_driver_champs_df(await response.json())
            else:
                champs_df = data_processor.make_constructor_champs_df(await response.json())
            empty_champs.append(champs_df)
        return empty_champs


def get_champs_tasks(session, competitor_type, champs):
    # Creates a list of tasks for an async function.
    tasks = []
    for champ in champs:
        url = build_champs_url(competitor_type, champ)
        tasks.append(session.get(url, ssl=False))
    return tasks


def build_race_url(competitor_type, year, race):
    # Formats a URL to later be used in an http request.
    if (competitor_type == 'driver'):
        return driver_standings_url.format(year, race)
    else:
        return constructor_standings_url.format(year, race)
    

def build_champs_url(competitor_type, competitor):
    # Formats a URL to later be used in an http request.
    if (competitor_type == 'driver'):
        return driver_champ_wins.format(competitor)
    else:
        return constructor_champ_wins.format(competitor)
