import streamlit as st
import ergastpy
import data_scraper
import data_processor
import plotter
import time

start = time.time()

st.set_page_config(layout="wide", page_title='F1 Data Visualizer', page_icon='favicon.ico')


def get_non_selected_competitors(df, competitorID, competitor):
    # Presents a Streamlit Multiselectbox to the user to determine which options
    # to include. Those excluded are returned.
    competitor_list = data_processor.get_column_list(df, competitorID)
    selected_competitors = st.multiselect('Choose ' + competitor, options=competitor_list, default=competitor_list)
    return list(set(competitor_list) - set(selected_competitors))


# Get season schedule, drivers and constructors
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def make_api_calls(year):
    # Makes initial calls to Ergast API to retrieve data that will is necessary
    # to begin the visualizations.
    schedule = ergastpy.get_schedule(year)
    driver_df = ergastpy.get_drivers(year)
    constructor_df = ergastpy.get_constructors(year)
    return schedule, driver_df, constructor_df


# Set up sections of web page
header = st.beta_container()
points_progression_section = st.beta_container()
driver_points_progression_column, constructor_points_progression_column = st.beta_columns(2)
standings_section = st.beta_container()
driver_standings_column, constructor_standings_column = st.beta_columns(2)
champs_ranking_section = st.beta_container()

with header:
    st.title('Formula 1 Data Visualiser')
    st.markdown('An [open-source](https://github.com/adenhaus/f1-data-viz) project by [**Aden Haussmann**](https://www.linkedin.com/in/aden-haussmann/).')
    st.markdown('Explore detailed F1 data such as how driver and constructor points progressed over a given season, current and historical standings, career snapshots and more key stats.')
    st.markdown('*Control the input parameters of tables and visualizations below by using the tools with matching headings in the sidebar to the left.*')
    st.markdown('***Hint:*** *Hover over lines, bars or other aspects of a chart to see more details.*')

with st.sidebar:
    st.markdown('# **Adjust Parameters**')

    year = st.slider('Choose Year', min_value=1950, max_value=2021, value=2021, step=1)
    schedule, driver_df, constructor_df = make_api_calls(year)

    # Restrict schedule to races which have already taken place
    schedule = data_processor.make_column_past_dates(schedule, 'date')
    season_length = len(schedule)

    st.markdown('---')
    st.markdown('## **Points Progression**')

    with st.beta_expander("Select Drivers"):
        non_selected_drivers = get_non_selected_competitors(driver_df, 'driverId', 'Drivers')

    with st.beta_expander("Select Constructors"):
        non_selected_constructors = get_non_selected_competitors(constructor_df, 'constructorId', 'Constructors')

    show_legend = st.checkbox('Show legends', help='Legends are hidden by default as they cramp the layout somewhat, but you can enable them.')
    st.markdown('---')

    st.markdown('## **Standings**')

    # Choose race
    race_list = data_processor.get_column_list(schedule, 'raceName')
    race_list.reverse()
    race = st.selectbox('Choose Race', options=race_list)
    round = data_processor.get_race_round(schedule, 'raceName', race)


with points_progression_section:
    st.markdown('---')
    st.markdown('## **Points Progression**')
    st.markdown('Compare any combination of drivers or constructors by selecting them in the sidebar on the left to see their points progression over the course of a given season, which you can also choose on the left.')

    with driver_points_progression_column:
        st.markdown('### **Drivers**')

        # Get dataframe with all drivers' points for each race in the season
        all_driver_points_df = data_scraper.get_points(year, 'driver', season_length, driver_df)
        selected_driver_points_df = all_driver_points_df.copy()

        # Remove drivers who weren't selected
        selected_driver_points_df = data_processor.remove_df_rows(selected_driver_points_df, 'driverID', non_selected_drivers)

        driver_standings_fig = plotter.draw_viridis_line_chart(selected_driver_points_df, "race", "points", 'driverID', 'driverID', 'driverID', 'Race', 'Points', 'Drivers')
        points_scoring_drivers = data_processor.get_points_scoring_competitors(all_driver_points_df, season_length)
        driver_standings_pie = plotter.draw_viridis_pie_chart(points_scoring_drivers, 'points', 'driverID')

        if (show_legend):
            driver_standings_fig, driver_standings_pie = plotter.turn_on_driver_legends(driver_standings_fig, driver_standings_pie)

        st.plotly_chart(driver_standings_fig, use_container_width=True)
        st.plotly_chart(driver_standings_pie, use_container_width=True)

    with constructor_points_progression_column:
        st.markdown('### **Constructors**')

        # Try except block necessary because constructor standings data is not available before 1958
        try:
            # Get dataframe with all drivers' points for each race in the season
            all_constructor_points_df = data_scraper.get_points(year, 'constructor', season_length, constructor_df)
            selected_constructor_points_df = all_constructor_points_df.copy()
            # Remove constructors who didn't score any points
            selected_constructor_points_df = data_processor.remove_df_rows(selected_constructor_points_df, 'constructorID', non_selected_constructors)
        except IndexError:
            pass

        try:
            constructor_standings_fig = plotter.draw_sunsetdark_line_chart(selected_constructor_points_df, "race", "points", 'constructorID', 'constructorID', 'constructorID', 'Race', 'Points', 'Constructors')
            points_scoring_constructors = data_processor.get_points_scoring_competitors(all_constructor_points_df, season_length)
            constructor_standings_pie = plotter.draw_sunsetdark_pie_chart(points_scoring_constructors, 'points', 'constructorID')

            if (show_legend):
                constructor_standings_fig, constructor_standings_pie = plotter.turn_on_constructor_legends(constructor_standings_fig, constructor_standings_pie)

            st.plotly_chart(constructor_standings_fig, use_container_width=True)
            st.plotly_chart(constructor_standings_pie, use_container_width=True)
        except NameError:
            st.write('*No constructor standings data available for seasons before 1958.*')

with standings_section:
    st.markdown('---')
    st.markdown('## **Standings**')
    st.markdown('Choose a year and a race from the sidebar on the left to view driver and constructors standings.')

    with driver_standings_column:
        st.markdown('### **Drivers Championship**')
        driver_standings_df = data_processor.get_standings(all_driver_points_df, round)
        st.dataframe(driver_standings_df)

    with constructor_standings_column:
        st.markdown('### **Constructors Championship**')
        # Try except block necessary because constructor standings data is not available before 1958
        try:
            constructor_standings_df = data_processor.get_standings(all_constructor_points_df, round)
            st.dataframe(constructor_standings_df)
        except NameError:
            st.write('*No constructor standings data available for seasons before 1958.*')

with champs_ranking_section:
    st.markdown('---')
    st.markdown('## **All-Time Rankings**')
    st.markdown('Drivers and constructors ranked their total respective Championship victoroies.')

    driver_champs_df = data_scraper.get_champ_winners('driver')
    driver_champs_df = data_processor.df_column_to_int(driver_champs_df, 'number_wins')
    driver_champs_fig = plotter.draw_viridis_bar_chart(driver_champs_df, 'driverID', 'number_wins', 'Driver', 'Championships Won', 'driverID')
    st.plotly_chart(driver_champs_fig, use_container_width=True)

    constructor_champs_df = data_scraper.get_champ_winners('constructor')
    constructor_champs_df = data_processor.df_column_to_int(constructor_champs_df, 'number_wins')
    constructor_champs_fig = plotter.draw_sunsetdark_bar_chart(constructor_champs_df, 'constructorID', 'number_wins', 'Constructor', 'Championships Won', 'constructorID')
    st.plotly_chart(constructor_champs_fig, use_container_width=True)

end = time.time()
print("TOTAL TIME:")
print(end - start)
print()
