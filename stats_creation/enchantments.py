from custom_utils.remapping import *
from custom_utils import preprocess, tf

import plotly.express as px
import pandas as pd


DATA_PATH = './data/'
# data = pd.read_csv(DATA_PATH+'df_onehot.csv')
# df = tf.get_df_onehot(data)

#_, df = tf.data_pipeline_raw(DATA_PATH)
df = pd.read_csv(DATA_PATH+'df_onehot.csv')

def get_enchant_count(df):
    enc_count = df.copy()

    enc_list = ['e_green', 'e_red', 'e_yellow', 'e_gray', 'e_blue', 'e_pink', 'e_cyan']

    total_match_count = round(enc_count['match_count'].sum() / 6) # assumes repetition of 6 matches

    # sum up ability picks over SAME matches
    for e in enc_list:
        enc_count[e+'_pick'] = enc_count[e] * enc_count['match_count']
    # sum up ability picks over LEGENDS
    enc_count = enc_count.groupby('legend')[[e+'_pick' for e in enc_list]].sum().reset_index()

    enc_total = pd.Series(enc_count[[e+'_pick' for e in enc_list ]].sum(axis=1)) // 2 # total number of picks for each ability (assumes each match picks 2 abilities)

    for e in enc_list:
        enc_count[e+'_pickrate'] = round(enc_count[e+'_pick'] / enc_total * 100, 2)

    return enc_count

def get_enchant(df, legend):
    df = get_enchant_count(df)

    df = df.loc[df['legend']==legend, :]
    enc_list = ['e_green', 'e_red', 'e_yellow', 'e_gray', 'e_blue', 'e_pink', 'e_cyan']

    return_list = ['legend']
    return_list.extend([e+'_pickrate' for e in enc_list])

    return df.loc[:, return_list]
