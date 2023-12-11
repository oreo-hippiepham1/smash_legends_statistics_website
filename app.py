import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input


from viz import create_plots
from custom_utils import mapping, remapping, preprocess, tf
from stats_creation import abilities, enchantments


# App
app = Dash(__name__, external_stylesheets=['styles.css', 'https://codepen.io/chriddyp/pen/bWLwgP.css']) 

DATA_PATH = './data/'
data = pd.read_csv(DATA_PATH+'df.csv')
df = tf.get_df(data)

data_onehot = pd.read_csv(DATA_PATH+'df_onehot.csv')
DF_ONEHOT = tf.get_df_onehot(data_onehot)

maps_list = [k for k in mapping.maps_dict.keys()]
tiers_list = [t for t in mapping.tiers_dict.keys()]


def generate_enchantment_count_table(df: pd.DataFrame):
    return html.Table(
        className='styled-table',
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

my_output = html.Div(className='center')

app.layout = html.Div(style={'padding': 20}, children=[
    html.Div(children='Hello World', id='div'),

    html.Div([
        dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    ], style={'width': '100%', 'display': 'inline-block', }, id='table-div'),

    # Input: Choosing Maps + Tiers + SortBy
    html.Div([
        html.Div(dcc.Dropdown(options=maps_list, value=maps_list[0], id='dropdown-map'), style={'padding':10, 'flex': 2}),
        html.Div(dcc.Dropdown(options=tiers_list, value=tiers_list[0], id='dropdown-tier'), style={'padding': 10,'flex': 2}),
        html.Div([
            html.Div(html.Label('Sorted: '), style={'padding': 5,'flex':1}),
            html.Div(dcc.RadioItems(options=['Value', 'Name'], value='Yes', id='sorted-radio'), style={'padding': 10, 'flex':2}),
        ], style={'padding': 5, 'flex':1}),
    ], style={'width': '100%',  'display': 'flex', 'justify-content':'space-evenly', 'border':'solid'}, id='dropdown-div'),

    # Choose Legends
    html.Div([
        dcc.Dropdown(options=list(remapping.color_map.keys()), value='peter', id='dropdown-legend')
    ], style={'width': '100%', 'display': 'inline-block'}),

    my_output,
    
    # Pick Rate
    html.Div([
        dcc.Graph(figure={}, id='maptier-pick-pct'),
    ], style={'width': '100%', 'display': 'inline-block'}),

    # Win Rate
    html.Div([
        dcc.Graph(figure={}, id='maptier-win-pct'),
    ], style={'width': '100%', 'display': 'inline-block'}),
])


@callback(
    Output(my_output, component_property='children'),
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