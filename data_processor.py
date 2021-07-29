from datetime import datetime
import pandas as pd


def get_attribute(df, source_attr, target_attr, value):
    '''Returns a target attribute from a pandas dataframe
    where a source attribute is equal to a certain value.
    '''
    temp_df = df.loc[df[source_attr] == value]
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df.iloc[0][target_attr]


def make_column_past_dates(df, column_name):
    '''Changes a given column in a pandas dataframe to the data datatype
    and removes rows where date is in the future.
    '''
    df[column_name]= pd.to_datetime(df[column_name])
    return df.loc[df[column_name] < datetime.now()]


def get_column_list(df, competitorID):
    '''Turns a given column of a pandas dataframe into a list.'''
    return df[competitorID].tolist()


def get_race_round(df, column_name, race):
    '''Takes a race name and returns the race's number in the season
    order (eg. 1 or 2).
    '''
    round_df = df.loc[df[column_name] == race]
    round_df.reset_index(drop=True, inplace=True)
    return int(round_df.iloc[0]['round'])


def remove_df_rows(df, competitorID, competitors):
    '''Removes all rows of a dataframe where a value in a certain column
    is present in a given list of values.
    '''
    for competitor in competitors:
        df = df[df[competitorID] != competitor]
    return df


def get_points_scoring_competitors(df, season_length):
    '''Return a pandas dataframe of only drivers or constructors who
    scored points by the end of the season.
    '''
    point_scorers = df[df['points'] != 0]
    return point_scorers[point_scorers['race'] == season_length]


def get_standings(df, round):
    '''Return a pandas dataframe of driver or constructor standings after a
    given race in a season.
    '''
    standings_df = df.loc[df['race'] == round].copy()
    standings_df.sort_values(by=['points'], inplace=True, ascending=False)
    standings_df.reset_index(drop=True, inplace=True)
    return standings_df
