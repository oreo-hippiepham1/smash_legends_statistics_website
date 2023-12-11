from custom_utils.remapping import *
from custom_utils.tf import tf_df
from custom_utils import preprocess
from viz import win_rate, pick_rate

import plotly.express as px
import pandas as pd



def per_legend_fig(df: pd.DataFrame, map_col: str, tier_col: str,ordered: bool=False, fig_mode: str="winrate"):
    """
    Expects 'df' to be a 2D DataFrame, with columns: 'legend' and 'per-legend-statistics'
    """

    if fig_mode == 'winrate':
        pct = win_rate.win_rate_tier_map(df, map_col, tier_col, ordered)
        y = 'winrate'
    elif fig_mode == 'pickrate':
        pct = pick_rate.pick_rate_tier_map(df, map_col, tier_col, ordered)
        y = 'pickrate'

    # Create Bar plot
    title = f'''{fig_mode} by Legend,
    Map: {map_col},
    Tier: {tier_col} '''
    fig = px.bar(pct, x='legend', y=y, title=title,
                color='legend', color_discrete_map=color_map)
    fig.update_layout(xaxis_title='Legend Name', yaxis_title=fig_mode)
    min_range = 0 if pct[y].min() - 10 <= 0 else pct[y].min() - 10
    fig.update_yaxes(range=[min_range, pct[y].max()+5])

    return fig


