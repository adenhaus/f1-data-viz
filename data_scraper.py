import pandas as pd
from datetime import date
import streamlit as st
import aiohttp
import asyncio
import data_processor

todays_date = date.today()
current_year = int(todays_date.year)

driver_standings_url = 'http://ergast.com/api/f1/{}/{}/driverStandings.json?limit=1000'
constructor_standings_url = 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'
   

@st.cache(suppress_st_warning=True)
def get_points(year, competitor_type, season_length, competitor_df):
    """Returns a pandas DataFrame of the points scored by every driver/constructor
    at every race in a given season.

    Args:
        year (int): The season year.
        competitor_type (String): Either "driver" or "constructor".
        season_length (int): Number of races in a season, excluding any that haven't taken place yet.
        competitor_df (pandas.DataFrame): A DataFrame of all drivers/constructors
        that participated in the season.

    Returns:
        pandas.DataFrame: All of the points scored by every driver/constructor
    at every race in a given season.
    """
    competitor_list = competitor_df[competitor_type + 'Id'].tolist()
    races = []

    # Async
    races = asyncio.run(get_races(season_length, competitor_type, year, races))
    race_dict = dict(zip(range(len(races)), races))

    return data_processor.build_points_df(competitor_list, competitor_type + 'ID', season_length, race_dict)


def get_tasks(session, season_length, competitor_type, year):
    """Creates a list of tasks for an async function.

    Args:
        session (aiohttp.ClientSession): The client session.
        season_length (int): Number of races in a season, excluding any that haven't taken place yet.
        competitor_type (String): Either "driver" or "constructor".
        year (int): The season year.

    Returns:
        list: The tasks.
    """
    tasks = []
    for race in range(0, season_length):
        url = build_url(competitor_type, year, race)
        tasks.append(session.get(url, ssl=False))
    return tasks


async def get_races(season_length, competitor_type, year, races):
    """Makes API calls asynchronously to create a list of pandas DataFrames.

    Args:
        season_length (int): Number of races in a season, excluding any that haven't taken place yet.
        competitor_type (String): Either "driver" or "constructor".
        year (int): The season year.
        races (list): An empty list.

    Returns:
        list: A list of pandas DataFrames containing all points scored by each driver or
        constructor at every race in the season.
    """
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, season_length, competitor_type, year)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if (competitor_type == 'driver'):
                standings_df = data_processor.make_driver_df(await response.json())
            else:
                standings_df = data_processor.make_constructor_df(await response.json())
            races.append(standings_df)
        return races


def build_url(competitor_type, year, race):
    """Formats the URL to later be used in an http request.

    Args:
        competitor_type (String): Either "driver" or "constructor.
        year (int): The season.
        race (int): The round.

    Returns:
        String: Formatted URL.
    """
    if (competitor_type == 'driver'):
        return driver_standings_url.format(year, race)
    else:
        return constructor_standings_url.format(year, race)
