import ergastpy
import pandas as pd
from datetime import date

todays_date = date.today()
current_year = int(todays_date.year)

# os.mkdir('data/constructorID_standings')

def get_standings(competitor_list, competitor, race_count, races):
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
        all_points_df.to_csv('data/' + competitor + '_standings/' + str(year) + '.csv', index=False)

    print(str(year) + ' ' + competitor + ' done')

# Get driver standings for each race of each season
for year in range(1991, current_year + 1):
    season_length = len(ergastpy.get_schedule(year))
    driver_df = ergastpy.get_drivers(year)
    driver_list = driver_df['driverId'].tolist()
    constructor_df = ergastpy.get_constructors(year)
    constructor_list = constructor_df['constructorId'].tolist()

    driver_races = {}
    constructor_races = {}
    driver_race_count = 0
    constructor_race_count = 0

    for race in range(0, season_length):
        try:
            driver_standings = ergastpy.driver_standings(year, race)
            driver_races[race] = driver_standings
            driver_race_count += 1
            try:
                constructor_standings = ergastpy.constructor_standings(year, race)
                constructor_races[race] = constructor_standings
                constructor_race_count += 1
            except:
                print('no constructor standings data before 1958')
        except:
            break
    if year == current_year:
        driver_race_count -= 1
        constructor_race_count -= 1

    # get_standings(driver_list, 'driverId', driver_race_count, driver_races)
    get_standings(constructor_list, 'constructorID', constructor_race_count, constructor_races)
