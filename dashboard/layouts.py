from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
import urllib.request

# =========================================
# LEITURA DOS DADOS
# =========================================

df = pd.read_csv(
    '../data/processed/enem_tratado.csv',
    low_memory=False
)

# =========================================
# GEOJSON BRASIL
# =========================================

url = (
    'https://raw.githubusercontent.com/'
    'codeforamerica/click_that_hood/master/'
    'public/data/brazil-states.geojson'
)

with urllib.request.urlopen(url) as response:
    brasil_geojson = json.load(response)

# =========================================
# SIGLAS DOS ESTADOS
# =========================================

siglas_estados = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goiás': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraíba': 'PB',
    'Paraná': 'PR',
    'Pernambuco': 'PE',
    'Piauí': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'São Paulo': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}

def create_layout(app):

    # =========================================
    # KPIs
    # =========================================

    media_geral = round(
        df['MEDIA_GERAL'].mean(),
        2
    )

    total_alunos = len(df)

    media_2023 = round(
        df[df['ANO'] == 2023]['MEDIA_GERAL'].mean(),
        2
    )

    media_2024 = round(
        df[df['ANO'] == 2024]['MEDIA_GERAL'].mean(),
        2
    )

    # =========================================
    # DADOS DO MAPA
    # =========================================

    mapa_df = (
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .reset_index()
    )

    mapa_df.columns = ['sigla', 'media']

    mapa_df['estado'] = mapa_df['sigla'].map(
        {v: k for k, v in siglas_estados.items()}
    )

    # =========================================
    # MAPA DO BRASIL
    # =========================================

    fig_mapa = px.choropleth(
        mapa_df,
        geojson=brasil_geojson,
        locations='estado',
        featureidkey='properties.name',
        color='media',
        hover_name='estado',
        color_continuous_scale='Blues',
        title='Desempenho Médio por Estado'
    )

    fig_mapa.update_geos(
        fitbounds='locations',
        visible=False
    )

    fig_mapa.update_layout(
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # =========================================
    # GRÁFICO - MÉDIA POR ESTADO
    # =========================================

    fig_estado = px.bar(
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .reset_index(),
        x='SG_UF_PROVA',
        y='MEDIA_GERAL',
        title='Média Geral por Estado'
    )

    # =========================================
    # GRÁFICO - DISTRIBUIÇÃO
    # =========================================

    fig_box = px.box(
        df,
        x='ANO',
        y='MEDIA_GERAL',
        title='Distribuição das Notas'
    )

    # =========================================
    # LAYOUT
    # =========================================

    app.layout = dbc.Container(
        fluid=True,
        children=[

            dbc.Row([

                # =====================================
                # SIDEBAR
                # =====================================

                dbc.Col([

                    html.Div([

                        html.H2(
                            'ENEM Analytics',
                            className='sidebar-title'
                        ),

                        html.P(
                            '''
                            Dashboard de análise comparativa
                            dos microdados do ENEM 2023 e 2024.
                            ''',
                            className='sidebar-text'
                        ),

                        html.Hr(),

                        html.H5('Objetivos'),

                        html.Ul([
                            html.Li('Comparar desempenho'),
                            html.Li('Analisar desigualdade'),
                            html.Li('Explorar padrões'),
                            html.Li('Gerar insights')
                        ])

                    ], className='sidebar')

                ], width=2),

                # =====================================
                # CONTEÚDO PRINCIPAL
                # =====================================

                dbc.Col([

                    html.H1(
                        'Dashboard Educacional ENEM',
                        className='text-center my-4'
                    ),

                    html.P(
                        '''
                        Análise exploratória e comparativa
                        dos dados do ENEM utilizando Python,
                        Pandas, Plotly e Dash.
                        ''',
                        className='text-center'
                    ),

                    # =====================================
                    # KPIs
                    # =====================================

                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                html.Div(
                                    'Média Geral',
                                    className='kpi-title'
                                ),
                                html.Div(
                                    media_geral,
                                    className='kpi-value'
                                )
                            ], className='kpi-card')
                        ], width=3),

                        dbc.Col([
                            html.Div([
                                html.Div(
                                    'Participantes',
                                    className='kpi-title'
                                ),
                                html.Div(
                                    f'{total_alunos:,}',
                                    className='kpi-value'
                                )
                            ], className='kpi-card')
                        ], width=3),

                        dbc.Col([
                            html.Div([
                                html.Div(
                                    'Média 2023',
                                    className='kpi-title'
                                ),
                                html.Div(
                                    media_2023,
                                    className='kpi-value'
                                )
                            ], className='kpi-card')
                        ], width=3),

                        dbc.Col([
                            html.Div([
                                html.Div(
                                    'Média 2024',
                                    className='kpi-title'
                                ),
                                html.Div(
                                    media_2024,
                                    className='kpi-value'
                                )
                            ], className='kpi-card')
                        ], width=3)

                    ]),

                    # =====================================
                    # VISÃO GERAL
                    # =====================================

                    html.H2(
                        'Visão Geral',
                        className='section-title'
                    ),

                    # =====================================
                    # MAPA
                    # =====================================

                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                dcc.Graph(
                                    figure=fig_mapa
                                )
                            ], className='graph-container')
                        ], width=12)

                    ]),

                    # =====================================
                    # GRÁFICOS EXECUTIVOS
                    # =====================================

                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                dcc.Graph(
                                    figure=fig_estado
                                )
                            ], className='graph-container')
                        ], width=6),

                        dbc.Col([
                            html.Div([
                                dcc.Graph(
                                    figure=fig_box
                                )
                            ], className='graph-container')
                        ], width=6)

                    ]),

                    # =====================================
                    # DASHBOARD INTERATIVO
                    # =====================================

                    html.H2(
                        'Exploração Interativa',
                        className='section-title'
                    ),

                    dbc.Row([

                        dbc.Col([

                            dcc.Dropdown(
                                id='filtro-ano',
                                options=[
                                    {
                                        'label': str(i),
                                        'value': i
                                    }
                                    for i in sorted(
                                        df['ANO'].unique()
                                    )
                                ],
                                value=2024,
                                clearable=False
                            )

                        ], width=3),

                        dbc.Col([

                            dcc.Dropdown(
                                id='filtro-estado',
                                options=[
                                    {
                                        'label': i,
                                        'value': i
                                    }
                                    for i in sorted(
                                        df['SG_UF_PROVA']
                                        .dropna()
                                        .unique()
                                    )
                                ],
                                value='SP',
                                clearable=False
                            )

                        ], width=3)

                    ]),

                    html.Br(),

                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                dcc.Graph(id='grafico-renda')
                            ], className='graph-container')
                        ], width=6),

                        dbc.Col([
                            html.Div([
                                dcc.Graph(id='grafico-histograma')
                            ], className='graph-container')
                        ], className='graph-container', width=6)

                    ]),

                    dbc.Row([

                        dbc.Col([
                            html.Div([
                                dcc.Graph(id='grafico-redacao')
                            ], className='graph-container')
                        ], width=6),

                        dbc.Col([
                            html.Div([
                                dcc.Graph(id='grafico-top-estados')
                            ], className='graph-container')
                        ], width=6)

                    ])

                ], width=10)

            ])

        ]
    )