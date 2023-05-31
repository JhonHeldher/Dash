 #======================================================================================================================
from dash import html, dcc, Input, Output, Dash
import dash_bootstrap_components as dbc
from pandas._libs import properties
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json


# Import bootstrap para o SwitchAIO
from dash_bootstrap_templates import ThemeSwitchAIO

# # Criação do app Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


# config principal
main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10},
}

# Declaramos que o tab_card ocupará toda a altura disponível dentro do contêiner em que está inserido.
tab_card = {'height': '100%'}
# Declaramos que showTips define se as dicas de ferramenta serão exibidas.
config_graph={"displayModeBar": False, "showTips": False}

# Os temas usados do bootstrap da Dash
template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY



# Dataframe com mortalidade, natalidade, aumento população e a população do brasil
df_card = pd.read_csv('concatenados/df_card.csv')
# Dataframe por mes
df_melt_mes_mnd = pd.read_csv('concatenados/df_melt_mes_mnd.csv')
# Dataframe por estados
df_mapa = pd.read_csv('concatenados/df_mapa.csv')

# Declaramos state_geo como leitura do arquivo json usando o encoding latin-1  
state_geo = json.load(open("Json/uf.json", "r", encoding='latin-1'))

# Converção de GEOCODIGO de str para int
for feature in state_geo['features']:
    feature['properties']['GEOCODIGO'] = int(feature['properties']['GEOCODIGO'])

# Dicionario para seleção de Mortalidade ou Natalidade
select_columns_mn = {
                "Mortos": "Mortalidade",
                "nascidos": "Natalidade",
                }
# Dicionario para seleção do ano
select_columns_ano = ["todos os anos", "2018", "2019", "2020", "2021", "2022"]


# ↧ layout ↧ ========================================================================================================================================

app.layout = dbc.Container(children=[      
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Col([
                            dbc.Row([
                            
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend(
                                            "Mortalidade e Natalidade",
                                            style={'font-weight': 'bold', 'font-size': '1.3rem', 'height': '1rem', 'margin-left': '20px'}
                                        ),
                                        html.Span("(nos últimos 5 Anos)", style={'font-size': '90%', 'color': 'dimgray', 'margin-left': '20px'})
                                    ], width=12)
                                ]),
                              

                                dbc.Row([# SwitchAIO de troca de tema
                                    dbc.Col(html.Legend("Escolha o Tema", style={'font-size': '0.8rem', 'height': '1.5625rem', 'margin-left': '1.25rem'}), width='auto'),
                                    dbc.Col(ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2])),
                                ], style={"margin-top": "0.75rem"}),
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Div([
                                    
                                            html.Div([
                                                html.P("Selecione o ano:", style={"margin-top": "-0.9375rem",'font-size': '0.8rem'}),
                                                dcc.Dropdown(
                                                    id="year-dropdown",
                                                    options=[{"label": str(year), "value": year} for year in select_columns_ano],
                                                    value="todos os anos",  # Selecionar "todos" como valor inicial
                                                    style={"margin-top": "-0.625rem"},
                                                ),
                                            ]),
                                            
                                            html.Div([
                                                html.P("Selecione o estado:", style={"margin-top": "0.3125rem",'font-size': '0.8rem'}),
                                                dcc.Dropdown(
                                                    id="state-dropdown",
                                                    options=[{"label": "Brasil", "value": "BR"}] +
                                                            [{"label": state, "value": state} for state in df_mapa["localidade"].unique()],
                                                    value="BR",
                                                    style={"margin-top": "-0.625rem"},
                                                ),
                                            ]),
                                            html.Div([
                                                html.P("Selecione entre Mortos e Nascidos:", style={"margin-top": "0.3125rem",'font-size': '0.8rem'}),
                                                dcc.Dropdown( 
                                                    id="location-dropdown_mn",
                                                    options=[{"label": j, "value": i} for i, j in select_columns_mn.items()],
                                                    value="Mortos",
                                                    style={"margin-top": "-0.625rem"},
                                                ),
                                            ]),
                                            
                                        ], id="teste"),
                                    ]),
                                ]),
                            ])
                        ])
                    ])
                ]),
            ], className='g-2 my-auto', style={'height': '350px'}),
            
            dbc.Row([
                dbc.Card([#Card Gráfico Mapa
                    dbc.CardBody([
                        dcc.Graph(id='graph6', className='dbc', config=config_graph)
                    ])
                ], style=tab_card),
            ], className='g-2 my-auto'),
            
        ], sm=12, lg=4),  
        
    # Segunda coluna === ↧ 4 Cards e dois grafico  ↧ === ↥ Filtro e Mapa ↥===================================================================================================================
    
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([#Card de Mortalidade 
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph1', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                        
                        dbc.Col([#Card de Natalidade 
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='graph2', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                    ])
                ], sm=12, lg=6),
                
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([#Card de Aumento populacional 
                                dbc.CardBody([
                                    dcc.Graph(id='graph3', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                        dbc.Col([
                            dbc.Card([#Card de Projeção da População 
                                dbc.CardBody([
                                    dcc.Graph(id='graph4', className='dbc', config=config_graph)
                                ])
                            ], style=tab_card),
                        ], width=6),
                    ])
                ], sm=12, lg=6),
                
            ],  style={'margin-top': '8px'}),
            
            dbc.Row([  
                dbc.Col([  
                    dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(id='graph5', className='dbc', config=config_graph)
                            ])
                        ], style=tab_card),     
                    ]),    
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph7', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card),
                ]), 
            ], className='g-2 my-auto', style={'margin-top': '7px'}),
            
        ], sm=12, lg=8), 
                
    ], className='g-2 my-auto'), 
    
], fluid=True, style={'height': '95vh'})



# ↧ 4 Cards  ↧=========================================================================================================================================
    
def create_indicator(title, value, reference):
    return go.Figure(
        go.Indicator(
            mode='number+delta',
            title={"text": title},
            value=value,
            number={'prefix': ""},
            delta={'relative': True, 'valueformat': '.1%', 'reference': reference}
        )
    )
    
# ↧ 4 Cards  ↧======↥ indicator ↥=========================================


@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def update_graphs(toggle):
    template = template_theme1 if toggle else template_theme2
  
    df_card_m = df_card[['ano', 'Mortes']].copy()
    df_card_m.sort_values(by='Mortes', ascending=False, inplace=True)
    
    figText = go.Figure()
    figText.add_trace(go.Indicator(
        mode='number+delta',
        title = {"text": f"<span style='font-size:180%'>{df_card['ano'].iloc[0]} - Mortalidade</span><br><span style='font-size:130%; color: dimgray'>últimos 5 anos</span><br>"},
        value = df_card_m['Mortes'].iloc[0],
        number = {'prefix': "", 'font': {'size': 35}},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_m['Mortes'].mean(), 'font': {'size': 12}},
        delta_increasing_color = "red" # add this line
    ))

   
    
    df_card_n = df_card[['ano', 'nascidos']].copy()
    df_card_n.sort_values(by='nascidos', ascending=False, inplace=True)

    figTextN = go.Figure()
    figTextN.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:180%'>{df_card_n['ano'].iloc[0]} - Natalidade</span><br><span style='font-size:130%; color: dimgray'>ultimos 5 anos</span><br>"},
        value = df_card_n['nascidos'].iloc[0],
        number = {'prefix': "", 'font': {'size': 35}},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_n['nascidos'].mean(), 'font': {'size': 12}}
    ))
        
    df_card_d = df_card[['ano', 'diferenca']].copy()
    df_card_d.sort_values(by='diferenca', ascending=False, inplace=True)

    figTextD = go.Figure()
    figTextD.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:180%'>{df_card['ano'].iloc[0]} - Top Ano</span><br><span style='font-size:130%; color: dimgray;'>Aumento população</span><br>"},
        value = df_card_d['diferenca'].iloc[0],
        number = {'prefix': "", 'font': {'size': 35}},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card_d['diferenca'].mean(), 'font': {'size': 12}}
    ))
    
    df_card.sort_values(by='valor', ascending=False, inplace=True)

    figProjPop = go.Figure()
    figProjPop.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span style='font-size:180%'>{df_card['ano'].iloc[0]} - População</span><br><span style='font-size:130%; color: dimgray'>em relação 2021</span><br>"},
        value = df_card['valor'].iloc[0],
        number = {'prefix': "", 'font': {'size': 35}},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_card['valor'].mean(), 'font': {'size': 12}}
    ))
    
    figures = [figText, figTextN, figTextD, figProjPop]
    
    for fig in figures:
        fig.update_layout(main_config,  template=template, height=85)
        fig.update_layout({"margin": {"l":0, "r":0, "t":40, "b":0}})

    return figures



# ↧ Grafico de linha Natalidade e Mortalidade ↧ ====================↥ cards Brazil ↥=====================================================================================================================

@app.callback(
    Output('graph5', 'figure'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def graph5(selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == 'todos os anos':  
        filtered_df = df_melt_mes_mnd 
    else:
        selected_year = str(selected_year)  # Converter para string
        filtered_df = df_melt_mes_mnd[df_melt_mes_mnd['data'].astype(str).str.startswith(selected_year)]
  
    figline = go.Figure()

    figline.add_trace(go.Line(x=filtered_df['data'], y=filtered_df['Mortos'], name='Mortos'))
    figline.add_trace(go.Line(x=filtered_df['data'], y=filtered_df['nascidos'], name='Nascidos', line=dict(color='lightblue')))

    figline.update_layout(
        title='Natalidade e Mortalidade',
    )
    figline.update_layout(main_config, template=template, height=260)
    figline.update_layout({"margin": {"l":0, "r":0, "t":30, "b":0}})
    return figline



# ↧ Mapa ↧=============↥ Grafico de linha Natalidade e Mortalidade ↥============================================================================================================================

@app.callback(
    Output('graph6', 'figure'),
    Input('state-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
)
def graph6(selected_state, selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == "todos os anos":  # Verifica se a opção selecionada é "todos os anos"
        filtered_df = df_mapa  # Mantém o dataframe completo
    elif selected_state == "BR":
        filtered_df = df_mapa[df_mapa["ano"] == int(selected_year)]
    else:
        filtered_df = df_mapa[(df_mapa["ano"] == int(selected_year)) & (df_mapa["localidade"] == selected_state)]
    
    figMap = px.choropleth(filtered_df, geojson=state_geo, color="Mortos",
                        locations="localidade (uid)_y",
                        featureidkey='properties.GEOCODIGO',
                        color_continuous_scale="Blues",
                        projection="mercator",
                        labels= {'Mortos':'Mortalidade'},
                        hover_data={'localidade' : True, 'nascidos': True},
                        )
    figMap.update_geos(fitbounds="locations", visible=False)
    figMap.update_geos(showcountries=False, showcoastlines=False, showland=False, showrivers=False)
    figMap.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'))
    
    figMap.update_layout(main_config,  template=template, height=530)
    return figMap



# ↧ Grafico de barra Aumento populacional ↧===============↥ Mapa ↥=========================================================================================================================================

@app.callback(
    Output('graph7', 'figure'),
    Input('year-dropdown', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph7(selected_year, toggle):
    template = template_theme1 if toggle else template_theme2
    
    if selected_year == 'todos os anos':  
        filtered_df = df_melt_mes_mnd 
    else:
        selected_year = str(selected_year)  # Converter para string
        filtered_df = df_melt_mes_mnd[df_melt_mes_mnd['data'].astype(str).str.startswith(selected_year)]
    
    figBarPop = go.Figure(go.Bar(
        x=filtered_df['data'],
        y=filtered_df['diferencia'],
        orientation='v',
        textposition='auto',
        insidetextfont=dict(family='Times', size=12))
    )

    figBarPop.update_layout(
        title='Variação Populacional',
    )


    figBarPop.update_layout(main_config,  template=template, height=450)
    figBarPop.update_layout({"margin": {"l": 0, "r": 0, "t": 30, "b": 0}})
    return figBarPop
# ↥ Grafico de barra Aumento populacional ↥=================================================================================================================================================================

 
if __name__ == "__main__":
 app.run_server(debug=True)

  
  
  
  
  
  
