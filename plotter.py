import plotly.express as px

def draw_sunsetdark_line_chart(selected_points_df, x, y, color, hover_name, hover_data, x_label, y_label, color_label):
    competitor_standings_fig = px.line(selected_points_df,
            x=x,
            y=y,
            color=color,
            hover_name=hover_name,
            hover_data={
                hover_data:False
            },
            labels={
                x:x_label,
                y:y_label,
                color:color_label
            },
            color_discrete_sequence=px.colors.sequential.Sunsetdark
            # color_discrete_map={
            #     "hamilton": "black",
            #     "bottas":"blue",
            #     "hhhh":"red"
            # }
    )

    competitor_standings_fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
            dtick = 1,
            showgrid = False
        ),
        yaxis = dict(
            gridcolor='Silver'
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
            t=0,
            b=0
        ),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return competitor_standings_fig


def draw_viridis_line_chart(selected_points_df, x, y, color, hover_name, hover_data, x_label, y_label, color_label):
    competitor_standings_fig = px.line(selected_points_df,
            x=x,
            y=y,
            color=color,
            hover_name=hover_name,
            hover_data={
                hover_data:False
            },
            labels={
                x:x_label,
                y:y_label,
                color:color_label
            },
            color_discrete_sequence=px.colors.sequential.Viridis
            # color_discrete_map={
            #     "hamilton": "black",
            #     "bottas":"blue",
            #     "hhhh":"red"
            # }
    )

    competitor_standings_fig.update_layout(
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1,
            dtick = 1,
            showgrid = False
        ),
        yaxis = dict(
            gridcolor='Silver'
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
            t=0,
            b=0
        ),
        plot_bgcolor='rgba(0,0,0,0)'
    )

    return competitor_standings_fig


def draw_sunsetdark_pie_chart(points_scoring_competitor, values, names):
    competitor_standings_pie = px.pie(points_scoring_competitor,
                values=values,
                names=names,
                color_discrete_sequence=px.colors.sequential.Sunsetdark
            )

    competitor_standings_pie.update_layout(
        showlegend=False,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    return competitor_standings_pie


def draw_viridis_pie_chart(points_scoring_competitor, values, names):
    competitor_standings_pie = px.pie(points_scoring_competitor,
                values=values,
                names=names,
                color_discrete_sequence=px.colors.sequential.Viridis
            )

    competitor_standings_pie.update_layout(
        showlegend=False,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    return competitor_standings_pie


def turn_on_constructor_legends(constructor_standings_fig, constructor_standings_pie):
    constructor_standings_fig.update_layout(
        showlegend=True
    )
    constructor_standings_pie.update_layout(
        showlegend=True
    )
    return constructor_standings_fig, constructor_standings_pie


def turn_on_driver_legends(driver_standings_fig, driver_standings_pie):
    driver_standings_fig.update_layout(
        showlegend=True
    )
    driver_standings_pie.update_layout(
        showlegend=True
    )
    return driver_standings_fig, driver_standings_pie