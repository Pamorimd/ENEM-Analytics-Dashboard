from dash import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv(
    '../data/processed/enem_tratado.csv',
    low_memory=False
)

def register_callbacks(app):

    @app.callback(
        Output('grafico-renda', 'figure'),
        Output('grafico-histograma', 'figure'),
        Output('grafico-redacao', 'figure'),
        Output('grafico-top-estados', 'figure'),

        Input('filtro-ano', 'value'),
        Input('filtro-estado', 'value')
    )

    def atualizar_graficos(ano, estado):

        dff = df[
            (df['ANO'] == ano) &
            (df['SG_UF_PROVA'] == estado)
        ]

        # =====================================
        # GRÁFICO 1 - RENDA
        # =====================================

        if 'Q006' in dff.columns:

            fig_renda = px.box(
                dff,
                x='Q006',
                y='MEDIA_GERAL',
                title='Faixa de Renda x Média Geral'
            )

        else:

            fig_renda = px.histogram(
                dff,
                x='MEDIA_GERAL',
                title='Distribuição da Média Geral'
            )

        # =====================================
        # GRÁFICO 2 - HISTOGRAMA
        # =====================================

        fig_hist = px.histogram(
            dff,
            x='MEDIA_GERAL',
            nbins=30,
            title='Distribuição das Notas'
        )

        # =====================================
        # GRÁFICO 3 - REDAÇÃO
        # =====================================

        fig_redacao = px.scatter(
            dff,
            x='NU_NOTA_REDACAO',
            y='MEDIA_GERAL',
            title='Redação x Média Geral'
        )

        # =====================================
        # GRÁFICO 4 - TOP ESTADOS
        # =====================================

        top_estados = (
            df[df['ANO'] == ano]
            .groupby('SG_UF_PROVA')['MEDIA_GERAL']
            .mean()
            .reset_index()
            .sort_values(by='MEDIA_GERAL', ascending=False)
            .head(10)
        )

        fig_top = px.bar(
            top_estados,
            x='SG_UF_PROVA',
            y='MEDIA_GERAL',
            title='Top 10 Estados'
        )

        return (
            fig_renda,
            fig_hist,
            fig_redacao,
            fig_top
        )