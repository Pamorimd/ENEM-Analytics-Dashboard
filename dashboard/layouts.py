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
# GEOJSON
# =========================================

url = (
    'https://raw.githubusercontent.com/'
    'codeforamerica/click_that_hood/master/'
    'public/data/brazil-states.geojson'
)

with urllib.request.urlopen(url) as response:
    brasil_geojson = json.load(response)

# =========================================
# SIGLAS
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

# =========================================
# LAYOUT
# =========================================

def create_layout(app):

    # =====================================
    # KPIs
    # =====================================

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

    diferenca = round(
        media_2024 - media_2023,
        2
    )

    # =====================================
    # MAPA
    # =====================================

    mapa_df = (
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .reset_index()
    )

    mapa_df.columns = ['sigla', 'media']

    mapa_df['estado'] = mapa_df['sigla'].map(
        {v: k for k, v in siglas_estados.items()}
    )

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
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#1f2937')
    )

    # =====================================
    # MÉDIA POR ESTADO
    # =====================================

    fig_estado = px.bar(
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .reset_index(),
        x='SG_UF_PROVA',
        y='MEDIA_GERAL',
        color='MEDIA_GERAL',
        color_continuous_scale='Blues',
        title='Comparação de Desempenho por Estado'
    )

    fig_estado.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # DISTRIBUIÇÃO
    # =====================================

    fig_box = px.box(
        df,
        x='ANO',
        y='MEDIA_GERAL',
        color='ANO',
        title='Distribuição das Notas por Ano'
    )

    fig_box.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # HISTOGRAMA
    # =====================================

    fig_hist = px.histogram(
        df,
        x='MEDIA_GERAL',
        nbins=30,
        color='ANO',
        barmode='overlay',
        title='Distribuição Geral das Notas'
    )

    fig_hist.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # REDAÇÃO
    # =====================================

    fig_redacao = px.scatter(
        df.sample(5000),
        x='NU_NOTA_REDACAO',
        y='MEDIA_GERAL',
        color='ANO',
        trendline='ols',
        title='Relação entre Redação e Média Geral'
    )

    fig_redacao.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # RENDA
    # =====================================

    fig_renda = px.box(
        df,
        x='Q006',
        y='MEDIA_GERAL',
        color='ANO',
        title='Impacto da Faixa de Renda no Desempenho'
    )

    fig_renda.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # TOP ESTADOS
    # =====================================

    top_estados = (
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_top = px.bar(
        top_estados,
        x='SG_UF_PROVA',
        y='MEDIA_GERAL',
        color='MEDIA_GERAL',
        color_continuous_scale='Tealgrn',
        title='Top 10 Estados com Melhor Desempenho'
    )

    fig_top.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # =====================================
    # ESTADO COM MAIOR MÉDIA
    # =====================================

    ranking_estados = (
        df.groupby('SG_UF_PROVA')['MEDIA_GERAL']
        .mean()
        .sort_values(ascending=False)
    )

    melhor_estado = ranking_estados.index[0]

    media_melhor_estado = round(
        ranking_estados.iloc[0],
        2
    )

    # =====================================
    # LAYOUT PRINCIPAL
    # =====================================

    app.layout = dbc.Container(
        fluid=True,
        className='main-container',
        children=[

            # =================================
            # HEADER
            # =================================

            html.Div([

                dbc.Row([

                    dbc.Col([

                        html.Div([

                            html.H1(
                                'ENEM Analytics',
                                className='hero-title'
                            ),

                            html.P(
                                '''
                                Dashboard interativo para análise
                                comparativa do desempenho educacional
                                brasileiro com base nos microdados
                                do ENEM 2023 e 2024.
                                ''',
                                className='hero-subtitle'
                            ),

                            html.Div([

                                html.Span(
                                    'Análise Exploratória',
                                    className='tag'
                                ),

                                html.Span(
                                    'Visualização de Dados',
                                    className='tag'
                                ),

                                html.Span(
                                    'Dash + Plotly',
                                    className='tag'
                                )

                            ], className='tags-container')

                        ])

                    ], width=8),

                    dbc.Col([

                        html.Div([

                            html.Div([
                                html.H4('2023'),
                                html.H2(f'{media_2023}')
                            ], className='mini-card'),

                            html.Div([
                                html.H4('2024'),
                                html.H2(f'{media_2024}')
                            ], className='mini-card')

                        ], className='hero-side-cards')

                    ], width=4)

                ])

            ], className='hero-section'),

            # =================================
            # DASHBOARD 1
            # =================================

            html.Div([

                html.H2(
                    'Dashboard 1 — Visão Geral',
                    className='section-title'
                ),

                html.P(
                    '''
                    Este painel apresenta os principais indicadores
                    nacionais do ENEM e destaca padrões gerais
                    de desempenho entre estados e anos.
                    ''',
                    className='section-description'
                ),

                # =============================
                # KPIs
                # =============================

                dbc.Row([

                    dbc.Col([
                        html.Div([
                            html.H6('Média Geral'),
                            html.H3(media_geral)
                        ], className='kpi-card')
                    ], width=3),

                    dbc.Col([
                        html.Div([
                            html.H6('Participantes'),
                            html.H3(f'{total_alunos:,}')
                        ], className='kpi-card')
                    ], width=3),

                    dbc.Col([
                        html.Div([

                            html.H6(
                                'Maior Média:',
                                className='kpi-title'
                            ),

                            html.Small(
                                f'{melhor_estado} • {media_melhor_estado}',
                                className='kpi-value'
                            )

                        ], className='kpi-card')
                    ], width=3),

                    dbc.Col([
                        html.Div([
                            html.H6('Variação 2024'),
                            html.H3(f'+{diferenca}')
                        ], className='kpi-card')
                    ], width=3)
                ]),

                html.Br(),

                # =============================
                # INSIGHT EXECUTIVO
                # =============================

                dbc.Alert([
                    html.H5('Insight Principal'),

                    html.P(
                        f'''
                        Os dados indicam estabilidade no desempenho
                        médio nacional entre 2023 e 2024, porém
                        estados do Sul e Sudeste continuam
                        concentrando as maiores médias do exame.
                        '''
                    )

                ], color='primary'),

                # =============================
                # MAPA
                # =============================

                html.Div([
                    dcc.Graph(figure=fig_mapa)
                ], className='graph-container'),

                html.Br(),

                dbc.Row([

                    dbc.Col([
                        html.Div([
                            dcc.Graph(figure=fig_estado)
                        ], className='graph-container')
                    ], width=6),

                    dbc.Col([
                        html.Div([
                            dcc.Graph(figure=fig_box)
                        ], className='graph-container')
                    ], width=6)

                ])

            ]),

            html.Br(),
            html.Hr(),
            html.Br(),

            # =================================
            # DASHBOARD 2
            # =================================

            html.Div([

                html.H2(
                    'Dashboard 2 — Exploração Interativa',
                    className='section-title'
                ),

                html.P(
                    '''
                    Este painel permite explorar relações entre
                    renda, desempenho, redação e distribuição
                    das notas do ENEM.
                    ''',
                    className='section-description'
                ),

                # =============================
                # FILTROS
                # =============================

                dbc.Row([

                    dbc.Col([

                        html.Label('Selecione o Ano'),

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

                        html.Label('Selecione o Estado'),

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

                # =============================
                # INSIGHT
                # =============================

                dbc.Alert([

                    html.H5('Pergunta Analítica'),

                    html.P(
                        '''
                        Existe relação entre nível socioeconômico
                        e desempenho acadêmico no ENEM?
                        Como a redação impacta a média geral?
                        '''
                    )

                ], color='info'),

                # =============================
                # GRÁFICOS
                # =============================

                dbc.Row([

                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='grafico-renda',
                                figure=fig_renda
                            )
                        ], className='graph-container')
                    ], width=6),

                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='grafico-histograma',
                                figure=fig_hist
                            )
                        ], className='graph-container')
                    ], width=6)

                ]),

                html.Br(),

                dbc.Row([

                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='grafico-redacao',
                                figure=fig_redacao
                            )
                        ], className='graph-container')
                    ], width=6),

                    dbc.Col([
                        html.Div([
                            dcc.Graph(
                                id='grafico-top-estados',
                                figure=fig_top
                            )
                        ], className='graph-container')
                    ], width=6)

                ])

            ])

        ]
    )