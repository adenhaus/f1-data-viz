from datetime import datetime
import pandas as pd

def get_attribute(df, source_attr, target_attr, value):
    temp_df = df.loc[df[source_attr] == value]
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df.iloc[0][target_attr]

def make_column_past_dates(df, column_name):
    df[column_name]= pd.to_datetime(df[column_name])
    return df.loc[df[column_name] < datetime.now()]

def get_competitor_list(df, competitorID):
    return df[competitorID].tolist()

def get_race_list(df, column_name):
    race_list = df[column_name].tolist()
    race_list.reverse()
    return race_list

def get_race_round(df, column_name, race):
    round_df = df.loc[df[column_name] == race]
    round_df.reset_index(drop=True, inplace=True)
    return int(round_df.iloc[0]['round'])

def remove_df_rows(df, competitorID, competitors):
    selected_points_df = df.copy()
    for competitor in competitors:
        selected_points_df = selected_points_df[selected_points_df[competitorID] != competitor]
    return selected_points_df

def get_points_scoring_competitors(df, season_length):
    points_scoring_competitors = df[df['points'] != 0]
    return points_scoring_competitors[points_scoring_competitors['race'] == season_length]

def get_driver_standings(df, round):
    standings_df = df.loc[df['race'] == round].copy()
    standings_df.sort_values(by=['points'], inplace=True, ascending=False)
    standings_df.reset_index(drop=True, inplace=True)
    return standings_df
    