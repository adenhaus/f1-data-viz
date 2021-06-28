import streamlit as st
import pandas as pd
import plotly.express as px
import ergastpy

st.set_page_config(layout="wide", page_title='F1 Data Visualizer', page_icon='favicon.ico')

def get_attribute(df, source_attr, target_attr, value):
    temp_df = df.loc[df[source_attr] == value]
    temp_df.reset_index(drop=True, inplace=True)
    return temp_df.iloc[0][target_attr]


header = st.beta_container()
standings_section = st.beta_container()
driver_standings_column, constructor_standings_column = st.beta_columns(2)

with header:
    st.title('Formula 1 Data Visualiser')
    st.markdown('Explore detailed F1 data such as how driver and constructor points progressed over a given season, current and historical standings, and more key stats.')
    st.markdown('---')

with st.sidebar:
    st.markdown('## **Standings**')

    year = st.slider('Choose Year', min_value=1950, max_value=2021, value=2020, step=1)
    season_length = len(ergastpy.get_schedule(year))

    with st.beta_expander("Select Drivers"):
        driver_df = ergastpy.get_drivers(year)
        driver_list = driver_df['driverId'].tolist()
        selected_drivers = st.multiselect('Choose Drivers', options=driver_list, default=driver_list)
        non_selected_drivers = list(set(driver_list) - set(selected_drivers))

    with st.beta_expander("Select Constructors"):
        constructor_df = ergastpy.get_constructors(year)
        constructor_list = constructor_df['constructorId'].tolist()
        selected_constructors = st.multiselect('Choose Constructors', options=constructor_list, default=constructor_list)
        non_selected_constructors = list(set(constructor_list) - set(selected_constructors))

    show_legend = st.checkbox('Show graph legends', help='Legends are hidden by default as they cramp the layout somewhat, but you can enable them.')
    st.markdown('---')

with standings_section:
    st.markdown('## **Standings**')
    st.markdown('Compare any combination of drivers or constructors by selecting them in the sidebar on the left to see their points progression over the course of a given season, which you can also choose on the left.')
    st.markdown('***Hint:*** *Hover over a line on a chart to see more details.*')

    with driver_standings_column:
        st.markdown('### **Drivers**')

        all_driver_points_df = pd.read_csv('data/driver_standings/' + str(year) + '.csv')

        for driver in non_selected_drivers:
            all_driver_points_df = all_driver_points_df[all_driver_points_df.driverID != driver]
        
        # chart2 = alt.Chart(all_driver_points_df).mark_line().encode(
        #     alt.X("race", scale=alt.Scale(domain=[1, season_length], nice=False)),
        #     alt.Y("points"),
        #     alt.Color("driverID")
        # ).configure_view(
        #     strokeWidth=0
        # ).configure_axisX(
        #     tickCount=season_length
        # )
        # st.altair_chart(chart2, use_container_width=True)

        driver_standings_fig = px.line(all_driver_points_df,
            x="race",
            y="points",
            color='driverID',
            hover_name="driverID",
            hover_data={
                'driverID':False
            },
            labels={
                'points':'Points',
                'race':'Race',
                'driverID':'Drivers'
            }
            # color_discrete_map={
            #     "hamilton": "black",
            #     "bottas":"blue",
            #     "hhhh":"red"
            # }
        )

        driver_standings_fig.update_layout(
            xaxis = dict(
                tickmode = 'linear',
                tick0 = 1,
                dtick = 1,
                showgrid = False
            ),
            yaxis = dict(
                showgrid = False
            ),
            legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
            ),
            showlegend=False,
            margin=dict(
                l=0,
                r=0,
                t=0
            ),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        if (show_legend):
            driver_standings_fig.update_layout(
                showlegend=True
            )

        st.plotly_chart(driver_standings_fig, use_container_width=True)

    with constructor_standings_column:
        st.markdown('### **Constructors**')

        try:
            all_constructor_points_df = pd.read_csv('data/constructorID_standings/' + str(year) + '.csv')
        except:
            print('No constructor standings data for seasons before 1958')

        for constructor in non_selected_constructors:
            all_constructor_points_df = all_constructor_points_df[all_constructor_points_df.constructorID != constructor]

        try:
            # chart3 = alt.Chart(all_constructor_points_df).mark_line().encode(
            # alt.X("race", scale=alt.Scale(domain=[1, season_length], nice=False)),
            # alt.Y("points"),
            # alt.Color("constructorID", legend=None)
            # ).configure_view(
            #     strokeWidth=0
            # ).configure_axisX(
            #     tickCount=season_length
            # )
            # st.altair_chart(chart3, use_container_width=True)

            constructor_standings_fig = px.line(all_constructor_points_df,
                x="race",
                y="points",
                color='constructorID',
                hover_name="constructorID",
                hover_data={
                    'constructorID':False
                },
                labels={
                    'points':'Points',
                    'race':'Race',
                    'constructorID':'Constructors'
                }
                # color_discrete_map={
                #     "hamilton": "black",
                #     "bottas":"blue",
                #     "hhhh":"red"
                # }
            )

            constructor_standings_fig.update_layout(
                xaxis = dict(
                    tickmode = 'linear',
                    tick0 = 1,
                    dtick = 1,
                    showgrid = False
                ),
                yaxis = dict(
                    showgrid = False
                ), legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                ),
                showlegend=False,
                margin=dict(
                    l=0,
                    r=0,
                    t=0
                ),
                plot_bgcolor='rgba(0,0,0,0)'
            )

            if (show_legend):
                constructor_standings_fig.update_layout(
                showlegend=True
            )

            st.plotly_chart(constructor_standings_fig, use_container_width=True)
        except:
            st.write('*No constructor standings data for seasons before 1958.*')
