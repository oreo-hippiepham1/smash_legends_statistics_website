from custom_utils.remapping import *
from custom_utils.tf import tf_df
from custom_utils import preprocess

import plotly.express as px
import pandas as pd


#df = tf_df()


def pick_rate_tier_map(df, map_col, tier_col, ordered=False) -> pd.DataFrame:
    def pick_rate(df):
        total_match_count = df['match_count'].sum() # assumes repetition of 6 times (once per each legend in a single match)
        per_legend = df.groupby(['legend'])['match_count'].sum().reset_index()
        per_legend['pickrate'] = per_legend['match_count'] / (total_match_count / 6) * 100

        return per_legend.loc[:, ['legend', 'pickrate']]
    
    df = preprocess.filter_tier(df, tier_col)
    df = preprocess.filter_map(df, map_col)

    if ordered:
        return pick_rate(df).sort_values(by='pickrate', ascending=False)
    return pick_rate(df)







