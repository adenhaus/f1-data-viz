import pandas as pd
from datetime import date
import streamlit as st
import aiohttp
import asyncio

todays_date = date.today()
current_year = int(todays_date.year)

driver_standings_url = 'http://ergast.com/api/f1/{}/{}/driverStandings.json?limit=1000'
constructor_standings_url = 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'

# os.mkdir('data/constructorID_standings')

def get_standings(competitor_list, competitor, race_count, races, year):
    all_points_df = pd.DataFrame(columns=['points', 'race', competitor])

    for i in range(0, len(competitor_list)):
        for race in range(0, race_count):
            current_standings = races[race]
            current_points_df = current_standings.loc[current_standings[competitor] == competitor_list[i]]
            current_points_df.reset_index(drop=True, inplace=True)
            try:
                current_points = current_points_df.iloc[0]['points']
                new_row = {'points':float(current_points), 'race':int(race), competitor:competitor_list[i]}
            except:
                new_row = {'points':0, 'race':int(race), competitor:competitor_list[i]}
            all_points_df = all_points_df.append(new_row, ignore_index=True)
            all_points_df.loc[(all_points_df.race == 0), 'race'] = race_count

    all_points_df.sort_values(by=['race'], inplace=True)
    return all_points_df
    # all_points_df.to_csv('data/' + competitor + '_standings/' + str(year) + '.csv', index=False)
    # print(str(year) + ' ' + competitor + ' done')


@st.cache(suppress_st_warning=True)
def standings(year, competitor_type, season_length, competitor_df):
    competitor_list = competitor_df[competitor_type + 'Id'].tolist()
    races = []
    race_count = 0

    # THIS TRY BLOCK IS FOR CURRENT YEAR BECAUSE ALL RACES IN SCHEDULE HAVEN'T PASSED YET
    # for race in range(0, season_length):
    #     try:
    #         standings = get_competitor_standings(competitor_type, year, race)
    #         races[race] = standings
    #         race_count += 1
    #     except:
    #         break

    # ASYNC
    races = asyncio.run(get_races(season_length, competitor_type, year, races))
    race_dict = dict(zip(range(len(races)), races))

    if year == current_year:
        race_count -= 1

    # WILL CAUSE INDEX ERROR FOR CURRENT SEASON (season_length)
    return get_standings(competitor_list, competitor_type + 'ID', season_length, race_dict, year)


def get_tasks(session, season_length, competitor_type, year):
    tasks = []
    for race in range(0, season_length):
        url = build_url(competitor_type, year, race)
        tasks.append(session.get(url, ssl=False))
    return tasks


async def get_races(season_length, competitor_type, year, races):
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session, season_length, competitor_type, year)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(type(response))
            if (competitor_type == 'driver'):
                standings_df = make_driver_df(await response.json())
            else:
                standings_df = make_constructor_df(await response.json())
            races.append(standings_df)
        return races


def make_driver_df(response):
    driverStandings = response['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    for driver in driverStandings:
        driver['driverID'] = driver['Driver']['driverId']
        driver['driver'] = driver['Driver']['givenName'] + ' ' + driver['Driver']['familyName']
        driver['nationality'] = driver['Driver']['nationality']
        driver['constructorID'] = driver['Constructors'][0]['constructorId']
        driver['constructor'] = driver['Constructors'][0]['name']
        del driver['Driver']
        del driver['Constructors']

    return pd.DataFrame(driverStandings)


def make_constructor_df(response):
    constructorStandings = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

    for constructor in constructorStandings:
        constructor['constructorID'] = constructor['Constructor']['constructorId']
        constructor['name'] = constructor['Constructor']['name']
        constructor['nationality'] = constructor['Constructor']['nationality']
        del constructor['Constructor']

    return pd.DataFrame(constructorStandings)


def build_url(competitor_type, year, race):
    if (competitor_type == 'driver'):
        return 'http://ergast.com/api/f1/{}/{}/driverStandings.json?limit=1000'.format(year, race)
    else:
        return 'http://ergast.com/api/f1/{}/{}/constructorStandings.json?limit=1000'.format(year, race)
