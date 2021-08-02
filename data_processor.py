from datetime import datetime
import pandas as pd
import numpy as np


def get_attribute(df, source_attr, target_attr, value):
    # Returns a target attribute from a pandas dataframe
    # where a source attribute is equal to a certain value.
    temp_df = df.loc[df[source_attr] == value]
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df.iloc[0][target_attr]


def make_column_past_dates(df, column_name):
    # Changes a given column in a pandas dataframe to the data datatype
    # and removes rows where date is in the future.
    df[column_name]= pd.to_datetime(df[column_name])
    return df.loc[df[column_name] < datetime.now()]


def get_column_list(df, column):
    # Turns a given column of a pandas dataframe into a list.
    return df[column].tolist()


def get_race_round(df, column_name, race):
    # Takes a race name and returns the race's number in the season
    # order (eg. 1 or 2).
    round_df = df.loc[df[column_name] == race]
    round_df.reset_index(drop=True, inplace=True)
    return int(round_df.iloc[0]['round'])


def remove_df_rows(df, competitorID, competitors):
    # Removes all rows of a dataframe where a value in a certain column
    # is present in a given list of values.
    for competitor in competitors:
        df = df[df[competitorID] != competitor]
    return df


def get_points_scoring_competitors(df, season_length):
    # Return a pandas dataframe of only drivers or constructors who
    # scored points by the end of the season.
    point_scorers = df[df['points'] != 0]
    return point_scorers[point_scorers['race'] == season_length]


def get_standings(df, round):
    # Return a pandas dataframe of driver or constructor standings after a
    # given race in a season.
    standings_df = df.loc[df['race'] == round].copy()
    standings_df.sort_values(by=['points'], inplace=True, ascending=False)
    standings_df.reset_index(drop=True, inplace=True)
    return standings_df


def make_constructor_df(response):
    # Builds a pandas DataFrame from the API resonse json.
    constructorStandings = response['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

    for constructor in constructorStandings:
        constructor['constructorID'] = constructor['Constructor']['constructorId']
        constructor['name'] = constructor['Constructor']['name']
        constructor['nationality'] = constructor['Constructor']['nationality']
        del constructor['Constructor']

    return pd.DataFrame(constructorStandings)


def make_driver_df(response):
    # Builds a pandas DataFrame from the API resonse json.
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


def make_driver_champs_df(response):
    # Builds a pandas DataFrame from the API resonse json.
    champs = response['MRData']

    driverID = champs['SeasonTable']['driverId']
    number_wins = champs['total']

    return [driverID, number_wins]


def make_constructor_champs_df(response):
    # Builds a pandas DataFrame from the API resonse json.
    champs = response['MRData']

    constructorID = champs['SeasonTable']['constructorId']
    number_wins = champs['total']

    return [constructorID, number_wins]


def make_all_champs_df(response, table, competitor):
    # Builds a pandas DataFrame from the API resonse json.
    champs = response['MRData'][table][competitor]

    return pd.DataFrame(champs)


def build_points_df(competitor_list, competitor, race_count, races):
    # Builds a dataframe of points scored by every driver/constructor at every race in a
    # given season from DataFrames for each race.
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


def transpose_list(list):
    np_array = np.array(list)
    transpose = np_array.T
    return transpose.tolist()


def list_to_df(list, columns):
    return pd.DataFrame(list, columns=columns)


def df_column_to_int(df, column):
    df[column] = pd.to_numeric(df[column])
    return df
