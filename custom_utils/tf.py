from custom_utils.remapping import *

import plotly.express as px
import pandas as pd

# RE-MAPPING NAMES
def remapping(code_name, mapping):
    return mapping[code_name]

def tf_df(data):
    df = data.copy(deep=True)
    df['legend'] = df['legend'].apply(remapping, args=(l_mapping, ))
    df['charm_1'] = df['charm_1'].apply(remapping, args=(c_mapping, ))
    df['charm_2'] = df['charm_2'].apply(remapping, args=(c_mapping, ))
    df['abi_1'] = df['abi_1'].apply(remapping, args=(abi_map, ))
    df['abi_2'] = df['abi_2'].apply(remapping, args=(abi_map, ))
    df['charm_1'] = df['charm_1'].apply(remapping, args=(e_map, ))
    df['charm_2'] = df['charm_2'].apply(remapping, args=(e_map, ))
    df['map'] = df['map'].apply(remapping, args=(m_mapping, ))
    df['tier'] = df['tier'].apply(remapping, args=(t_mapping, ))

    return df


def get_df(df):
    return tf_df(df)

def get_df_onehot(df):
    df['tier'] = df['tier'].apply(remapping, args=(t_mapping, ))
    return df
