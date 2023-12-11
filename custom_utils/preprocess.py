import pandas as pd


def filter_date(df, date_from, date_to) -> pd.DataFrame:
    date_limit = (df['date_from'] == date_from) & (df['date_to']==date_to)
    return df.loc[date_limit, :].copy()


def filter_tier(df, tier_col) -> pd.DataFrame:
    if tier_col == 'all':
        return df.copy()
    
    return df.loc[df['tier']==tier_col, :].copy()


def filter_map(df, map_col) -> pd.DataFrame:
    if map_col == 'all':
        return df.copy()
    
    return df.loc[df['map']==map_col, :].copy()

