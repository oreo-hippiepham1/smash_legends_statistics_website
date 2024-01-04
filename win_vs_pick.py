from custom_utils.remapping import *
from custom_utils.tf import tf_df
from custom_utils import preprocess, mapping
from viz import pick_rate, win_rate

import plotly.express as px
import pandas as pd
from PIL import Image
import os


def win_vs_pick_df(df, map_col, tier_col):
    pickrate_df = pick_rate.pick_rate_tier_map(df, map_col, tier_col)
    winrate_df = win_rate.win_rate_tier_map(df, map_col, tier_col)

    winpickrate = pd.merge(pickrate_df, winrate_df, on='legend', how='inner')
    return winpickrate

def plot_win_vs_pick(df, show_icons: bool=True):
    fig = px.scatter(df, x='pickrate', y='winrate', color='legend',
                 color_discrete_map=color_map, size=[2]*37)

    if show_icons:
        fig = px.scatter(df, x='pickrate', y='winrate',
                        hover_name='legend', hover_data=['legend', 'pickrate', 'winrate'])

        # add images
        for i, row in df.iterrows():
            legend = row['legend']
            abs_path = mapping.avatar_map[legend].lstrip('/')
            fig.add_layout_image(
            dict(
                source=Image.open(abs_path),
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=row["pickrate"],
                y=row["winrate"],
                sizex=3,
                sizey=3,
                #sizing="contain",
                opacity=0.8,
                layer="above"
                )
            )

    average_win_rate = df['winrate'].mean()
    average_pick_rate = df['pickrate'].mean()

    fig.add_shape(
        type="line",
        x0=0,
        y0=average_win_rate,
        x1=100,
        y1=average_win_rate,
        line=dict(color='red', width=2, dash='dash'),
        name="Average Win Rate"
    )

    # Add average pick rate line
    fig.add_shape(
        type="line",
        x0=average_pick_rate,
        y0=0,
        x1=average_pick_rate,
        y1=100,
        line=dict(color='blue', width=2, dash='dash'),
        name="Average Pick Rate"
    )

    # Calculate the range for the plot
    min_pickrate = df['pickrate'].min()
    max_pickrate = df['pickrate'].max()
    min_winrate = df['winrate'].min()
    max_winrate = df['winrate'].max()


    fig.update_layout(xaxis_title='Pickrate (%)', yaxis_title='Winrate (%)', showlegend=True)
    fig.update_yaxes(range=[min_winrate-3, max_winrate+3])
    fig.update_xaxes(range=[min_pickrate-3, max_pickrate+3])

    return fig
