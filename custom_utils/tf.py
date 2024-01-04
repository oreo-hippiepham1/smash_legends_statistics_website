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


def get_onehot(df):
    def onehot_abi(df, keep_orig: bool=True):
        # ABILITIES
        unique_abilities = pd.concat([df['abi_1'], df['abi_2']]).unique() # returns list of all abilities
        abi_onehot_encoded = pd.DataFrame(0, index=df.index, columns=unique_abilities) # all 0 entries

        for index, row in df.iterrows():
            abi_onehot_encoded.loc[index, row['abi_1']] = 1 # one hot
            abi_onehot_encoded.loc[index, row['abi_2']] = 1

        if keep_orig:
            abi_onehot_encoded = pd.concat([df, abi_onehot_encoded], axis=1) # combine with original df
            abi_onehot_encoded.drop(['abi_1', 'abi_2', 'charm_1', 'charm_2',], axis=1, inplace=True)

        return abi_onehot_encoded


    def onehot_enchantments(df, keep_orig: bool=True):
        # ENCHANTMENTS
        unique_enchantments = pd.concat([df['charm_1'], df['charm_2']]).unique()
        enchant_onehot_encoded = pd.DataFrame(0, index=df.index, columns=unique_enchantments) # all 0 entries

        for index, row in df.iterrows():
            enchant_onehot_encoded.loc[index, row['charm_1']] = 1
            enchant_onehot_encoded.loc[index, row['charm_2']] = 1

        if keep_orig:
            enchant_onehot_encoded = pd.concat([df, enchant_onehot_encoded], axis=1)
            enchant_onehot_encoded.drop(['charm_1', 'charm_2', 'abi_1', 'abi_2'], axis=1, inplace=True)

        return enchant_onehot_encoded

    abi = onehot_abi(df)
    ench = onehot_enchantments(df, False)
    final = pd.concat([abi, ench], axis=1)

    return final


def data_pipeline_raw(data_path, save_new: bool=False):
    # original data
    orig_data = pd.read_csv(data_path+'orig.csv')

    # remapping
    df = tf_df(orig_data)

    # get onehot version (abi + ench)
    df_onehot = get_onehot(df)

    # save if needed
    if save_new:
        df.to_csv(data_path + 'df.csv', index=False)
        df_onehot.to_csv(data_path + 'df_onehot.csv', index=False)

    return df, df_onehot