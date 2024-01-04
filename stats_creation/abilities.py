from custom_utils.remapping import *
from custom_utils import preprocess, tf

import plotly.express as px
import pandas as pd


DATA_PATH = './data/'
#data = pd.read_csv(DATA_PATH+'df_onehot.csv')

#_, df = tf.data_pipeline_raw(DATA_PATH)
df = pd.read_csv(DATA_PATH + 'df_onehot.csv')

def get_abi_count(df):
    abi_count = df.copy()

    abi_list = ['abi0', 'abi1', 'abi2', 'abi3', 'abi4', 'abi5']
    total_match_count = round(abi_count['match_count'].sum() / 6) # assumes repetition of 6 matches

    # sum up ability picks over SAME matches
    for ability in abi_list:
        abi_count[ability+'_pick'] = abi_count[ability] * abi_count['match_count']
        #abi_count[ability+'_win'] = abi_count[ability] * abi_count['win_count']
    # sum up ability picks over LEGENDS
    abi_count = abi_count.groupby('legend')[[abi+'_pick' for abi in abi_list]].sum().reset_index()

    abi_total = pd.Series(abi_count[[abi+'_pick' for abi in abi_list ]].sum(axis=1)) // 2 # total number of picks for each ability (assumes each match picks 2 abilities)

    for ability in abi_list:
        abi_count[ability+'_pickrate'] = round(abi_count[ability+'_pick'] / abi_total * 100, 2)

    return abi_count

def get_abi(df, legend):
    df = get_abi_count(df)

    df = df.loc[df['legend']==legend, :]
    abi_list = ['abi1', 'abi2', 'abi3', 'abi4', 'abi5']

    return_list = ['legend']
    return_list.extend([abi+'_pickrate' for abi in abi_list])

    return df.loc[:, return_list]
