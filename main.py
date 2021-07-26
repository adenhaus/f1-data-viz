import streamlit as st
import pandas as pd
import ergastpy
from datetime import datetime
import data_scraper
import plotter
import time

start = time.time()

st.set_page_config(layout="wide", page_title='F1 Data Visualizer', page_icon='favicon.ico')

def get_attribute(df, source_attr, target_attr, value):
    temp_df = df.loc[df[source_attr] == value]
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df.iloc[0][target_attr]

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def make_api_calls(year):
    schedule = ergastpy.get_schedule(year)
    driver_df = ergastpy.get_drivers(year)
    constructor_df = ergastpy.get_constructors(year)
    return schedule, driver_df, constructor_df

header = st.beta_container()
points_progression_section = st.beta_container()
driver_points_progression_column, constructor_points_progression_column = st.beta_columns(2)
standings_section = st.beta_container()
driver_standings_column, constructor_standings_column = st.beta_columns(2)

with header:
    st.title('Formula 1 Data Visualiser')
    st.markdown('Explore detailed F1 data such as how driver and constructor points progressed over a given season, current and historical standings, career snapshots and more key stats.')
    st.markdown('---')

with st.sidebar:
    st.markdown('# **Adjust Parameters**')

    year = st.slider('Choose Year', min_value=1950, max_value=2021, value=2021, step=1)
    schedule, driver_df, constructor_df = make_api_calls(year)

    # Restrict schedule to races which have already taken place
    schedule['date']= pd.to_datetime(schedule['date'])
    schedule = schedule.loc[schedule['date'] < datetime.now()]
    season_length = len(schedule)

    st.markdown('## **Points Progression**')

    with st.beta_expander("Select Drivers"):
        driver_list = driver_df['driverId'].tolist()
        selected_drivers = st.multiselect('Choose Drivers', options=driver_list, default=driver_list)
        non_selected_drivers = list(set(driver_list) - set(selected_drivers))

    with st.beta_expander("Select Constructors"):
        constructor_list = constructor_df['constructorId'].tolist()
        selected_constructors = st.multiselect('Choose Constructors', options=constructor_list, default=constructor_list)
        non_selected_constructors = list(set(constructor_list) - set(selected_constructors))

    show_legend = st.checkbox('Show legends', help='Legends are hidden by default as they cramp the layout somewhat, but you can enable them.')
    st.markdown('---')

    st.markdown('## **Standings**')

    race_list = schedule['raceName'].tolist()
    race_list.reverse()

    race = st.selectbox('Choose Race', options=race_list)

    round_df = schedule.loc[schedule['raceName'] == race]
    round_df.reset_index(drop=True, inplace=True)
    round = int(round_df.iloc[0]['round'])


with points_progression_section:
    st.markdown('## **Points Progression**')
    st.markdown('Compare any combination of drivers or constructors by selecting them in the sidebar on the left to see their points progression over the course of a given season, which you can also choose on the left.')
    st.markdown('***Hint:*** *Hover over a line on a chart to see more details.*')

    with driver_points_progression_column:
        st.markdown('### **Drivers**')

        all_driver_points_df = data_scraper.standings(year, 'driver', season_length, driver_df)
        # all_driver_points_df = pd.read_csv('data/driver_standings/' + str(year) + '.csv')
        selected_driver_points_df = all_driver_points_df.copy()

        for driver in non_selected_drivers:
            selected_driver_points_df = selected_driver_points_df[selected_driver_points_df.driverID != driver]

        driver_standings_fig = plotter.draw_viridis_line_chart(selected_driver_points_df, "race", "points", 'driverID', 'driverID', 'driverID', 'Race', 'Points', 'Drivers')

        points_scoring_drivers = all_driver_points_df[all_driver_points_df.points != 0]
        points_scoring_drivers = points_scoring_drivers[points_scoring_drivers.race == season_length]

        driver_standings_pie = plotter.draw_viridis_pie_chart(points_scoring_drivers, 'points', 'driverID')

        if (show_legend):
            driver_standings_fig, driver_standings_pie = plotter.turn_on_driver_legends(driver_standings_fig, driver_standings_pie)

        st.plotly_chart(driver_standings_fig, use_container_width=True)

        st.plotly_chart(driver_standings_pie, use_container_width=True)

    with constructor_points_progression_column:
        st.markdown('### **Constructors**')

        try:
            all_constructor_points_df = data_scraper.standings(year, 'constructor', season_length, constructor_df)
            # all_constructor_points_df = pd.read_csv('data/constructorID_standings/' + str(year) + '.csv')
            selected_constructor_points_df = all_constructor_points_df.copy()
        except:
            pass

        for constructor in non_selected_constructors:
            selected_constructor_points_df = selected_constructor_points_df[selected_constructor_points_df.constructorID != constructor]

        try:
            constructor_standings_fig = plotter.draw_sunsetdark_line_chart(selected_constructor_points_df, "race", "points", 'constructorID', 'constructorID', 'constructorID', 'Race', 'Points', 'Constructors')
            
            points_scoring_constructor = all_constructor_points_df[all_constructor_points_df.points != 0]
            points_scoring_constructor = points_scoring_constructor[points_scoring_constructor.race == season_length]

            constructor_standings_pie = plotter.draw_sunsetdark_pie_chart(points_scoring_constructor, 'points', 'constructorID')

            if (show_legend):
                constructor_standings_fig, constructor_standings_pie = plotter.turn_on_constructor_legends(constructor_standings_fig, constructor_standings_pie)

            st.plotly_chart(constructor_standings_fig, use_container_width=True)

            st.plotly_chart(constructor_standings_pie, use_container_width=True)
        except:
            st.write('*No constructor standings data available for seasons before 1958.*')

    with standings_section:
        st.markdown('## **Standings**')
        st.markdown('Choose a year and a race from the sidebar on the left to view driver and constructors standings.')
        st.markdown('***Hint:*** *Hover over a table and scroll to see more.*')

        with driver_standings_column:
            st.markdown('### **Drivers Championship**')
            driver_standings_df = all_driver_points_df.loc[all_driver_points_df['race'] == round].copy()
            driver_standings_df.sort_values(by=['points'], inplace=True, ascending=False)
            driver_standings_df.reset_index(drop=True, inplace=True)
            st.dataframe(driver_standings_df)
        
        with constructor_standings_column:
            st.markdown('### **Constructors Championship**')
            try:
                constructor_standings_df = all_constructor_points_df.loc[all_constructor_points_df['race'] == round].copy()
                constructor_standings_df.sort_values(by=['points'], inplace=True, ascending=False)
                constructor_standings_df.reset_index(drop=True, inplace=True)
                st.dataframe(constructor_standings_df)
            except NameError:
                st.write('*No constructor standings data available for seasons before 1958.*')

end = time.time()
print("TOTAL TIME:")
print(end - start)
print()
