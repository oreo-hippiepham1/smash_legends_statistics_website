from custom_utils.remapping import *
from custom_utils.tf import tf_df
from custom_utils import preprocess
from viz import pick_rate

import plotly.express as px
import pandas as pd

#df = tf_df()

# CALCULATE WIN %
def win_pct_legend(df, legend):
    temp = df.loc[df['legend']==legend, ['legend', 'match_count', 'win_count']]
    return round((temp.sum()['win_count'] / temp.sum()['match_count']) * 100, 2)


def win_rate_tier_map(df, map_col, tier_col, ordered=False) -> pd.DataFrame:
    def win_rate(df):
        df['winrate'] = (df['win_count'] / df['match_count']) * 100
        wpct = df.groupby('legend')['winrate'].mean().reset_index()
        return wpct
    
    df = preprocess.filter_tier(df, tier_col)
    df = preprocess.filter_map(df, map_col)

    # df['winrate'] = (df['win_count'] / df['match_count']) * 100
    # wpct = df.groupby('legend')['winrate'].mean().reset_index()
    if ordered:
        return win_rate(df).sort_values(by='winrate', ascending=False)
    return win_rate(df)




