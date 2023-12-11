import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input


from viz import create_plots
from custom_utils import mapping, remapping, preprocess, tf
from stats_creation import abilities, enchantments

# App
app = Dash(__name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]) 
# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
# })
server = app.server


DATA_PATH = './data/'
data = pd.read_csv(DATA_PATH+'df.csv')
df = tf.get_df(data)

data_onehot = pd.read_csv(DATA_PATH+'df_onehot.csv')
DF_ONEHOT = tf.get_df_onehot(data_onehot)

maps_list = [k for k in mapping.maps_dict.keys()]
tiers_list = [t for t in mapping.tiers_dict.keys()]


def generate_enchantment_count_table(df: pd.DataFrame):
    return html.Table(
        className='u-full-width',
        children=[
        html.Thead(
            html.Tr([
                html.Th(html.B("")),
                html.Th(html.B("legend")),
                html.Th(html.Img(src=mapping.avatar_map['health'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.avatar_map['attack'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.avatar_map['lightning'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.avatar_map['barrier'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.avatar_map['beam'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.avatar_map['pink'], height='50px', width='50px')),
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Td(
                    html.Img(src=mapping.avatar_map[df.iloc[0]["legend"]], height='50px', width='50px'),  # Add the image source and dimensions
                ),
                html.Td(df.iloc[0]["legend"]),
                html.Td(df.iloc[0]["e_green_pickrate"]),
                html.Td(df.iloc[0]["e_red_pickrate"]),
                html.Td(df.iloc[0]["e_yellow_pickrate"]),
                html.Td(df.iloc[0]["e_gray_pickrate"]),
                html.Td(df.iloc[0]["e_blue_pickrate"]),
                html.Td(df.iloc[0]["e_pink_pickrate"])
            ])
        ])
    ])

def generate_ability_count_table(df: pd.DataFrame):
    cur_legend = df.iloc[0]['legend']

    return html.Table(
        className='u-full-width',
        children=[
        html.Thead(
            html.Tr([
                html.Th(html.B("")),
                html.Th(html.Img(src=mapping.abi_map[cur_legend]['abi1'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.abi_map[cur_legend]['abi2'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.abi_map[cur_legend]['abi3'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.abi_map[cur_legend]['abi4'], height='50px', width='50px')),
                html.Th(html.Img(src=mapping.abi_map[cur_legend]['abi5'], height='50px', width='50px')),
            ])
        ),
        html.Tbody([
            html.Tr([
                html.Th(html.B("")),
                html.Td(df.iloc[0]["abi1_pickrate"]),
                html.Td(df.iloc[0]["abi2_pickrate"]),
                html.Td(df.iloc[0]["abi3_pickrate"]),
                html.Td(df.iloc[0]["abi4_pickrate"]),
                html.Td(df.iloc[0]["abi5_pickrate"]),
            ])
        ])
    ])

my_output_enchantment = html.Div(className='container')
my_output_ability = html.Div(className='container')

app.layout = html.Div(className='docs-example', style={'padding': 20}, children=[
    html.H3(children='Original Data'),

    html.Div([
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    ], style={'width': '100%', 'display': 'inline-block', },),

    # Input: Choosing Maps + Tiers + SortBy
    html.H3(children='Picking Maps, Tiers, Sorted-ness'),
    html.Div([
        html.Div(dcc.Dropdown(options=maps_list, value=maps_list[0], id='dropdown-map'), style={'flex': 2}, className='columns'),
        html.Div(dcc.Dropdown(options=tiers_list, value=tiers_list[0], id='dropdown-tier'), style={'flex': 2}, className='columns'),
        html.Div([
            html.Div(html.Label('Sorted: '), style={'padding': 5,'flex':1}, className='columns'),
            html.Div(dcc.RadioItems(options=['Value', 'Name'], value='Yes', id='sorted-radio'), style={'flex':2}, className='columns'),
        ], style={'padding': 5, 'flex':1}),
    ], style={'display': 'flex', 'justify-content':'space-evenly', 'border':'solid'}, id='dropdown-div', className='container'),

    # Choose Legends
    html.H3(children='Pick-rates for Enchantments and Abilities (map, tier, legend - sensitive)'),
    html.Div([
        dcc.Dropdown(options=list(remapping.color_map.keys()), value='peter', id='dropdown-legend')
    ], className='container', style={'border':'solid'}), 

    # Enchantment Table
    my_output_enchantment, 
    # Ability Table
    my_output_ability,
    
    # Pick Rate
    html.H3(children='Pick-rates for Legends (map, tier - sensitive)'),
    html.Div([
        dcc.Graph(figure={}, id='maptier-pick-pct'),
    ], style={'width': '100%', 'display': 'inline-block'}),

    # Win Rate
    html.H3(children='Win-rates for Legends (map, tier - sensitive)'),
    html.Div([
        dcc.Graph(figure={}, id='maptier-win-pct'),
    ], style={'width': '100%', 'display': 'block'}),
])


@callback(
    Output(my_output_enchantment, component_property='children'),
    Input(component_id='dropdown-map', component_property='value'),
    Input(component_id='dropdown-tier', component_property='value'),
    Input(component_id='dropdown-legend', component_property='value'),
)
def generate_enchantment(map_chosen, tier_chosen, legend):
    map_col = mapping.maps_dict[map_chosen]
    tier_col = mapping.tiers_dict[tier_chosen]

    df_onehot = preprocess.filter_map(DF_ONEHOT, map_col)
    df_onehot = preprocess.filter_tier(df_onehot, tier_col)

    df = enchantments.get_enchant(df_onehot, legend) 
    return generate_enchantment_count_table(df)


@callback(
    Output(my_output_ability, component_property='children'),
    Input(component_id='dropdown-map', component_property='value'),
    Input(component_id='dropdown-tier', component_property='value'),
    Input(component_id='dropdown-legend', component_property='value'),
)
def generate_enchantment(map_chosen, tier_chosen, legend):
    map_col = mapping.maps_dict[map_chosen]
    tier_col = mapping.tiers_dict[tier_chosen]

    df_onehot = preprocess.filter_map(DF_ONEHOT, map_col)
    df_onehot = preprocess.filter_tier(df_onehot, tier_col)

    df = abilities.get_abi(df_onehot, legend) 
    return generate_ability_count_table(df)


@callback(
    Output(component_id='maptier-pick-pct', component_property='figure'),
    Output(component_id='maptier-win-pct', component_property='figure'),
    Input(component_id='dropdown-map', component_property='value'),
    Input(component_id='dropdown-tier', component_property='value'),
    Input(component_id='sorted-radio', component_property='value'),
)
def choose_map_for_fig(map_chosen, tier_chosen, ordered):
    # Filter maps and tiers
    map_col = mapping.maps_dict[map_chosen]
    tier_col = mapping.tiers_dict[tier_chosen]

    # Order by Value or Name
    if ordered == 'Value':
        ordered = True
    else:
        ordered = False

    fig1 = create_plots.per_legend_fig(df, map_col, tier_col, ordered, fig_mode='pickrate', )
    fig2 = create_plots.per_legend_fig(df, map_col, tier_col, ordered, fig_mode='winrate', )
    
    return [fig1, fig2]



if __name__ == '__main__':
    app.run(debug=True)
