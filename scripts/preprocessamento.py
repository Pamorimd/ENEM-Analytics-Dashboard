import pandas as pd
import os

# =====================================================
# CONFIGURAÇÃO DE CAMINHOS
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PASTA_2023 = os.path.join(BASE_DIR, 'data', 'enem_2023')
PASTA_2024 = os.path.join(BASE_DIR, 'data', 'enem_2024')
PASTA_PROCESSADOS = os.path.join(BASE_DIR, 'data', 'processed')

os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

# =====================================================
# LEITURA DOS DADOS
# =====================================================

print('====================================')
print('LENDO DADOS 2023...')
print('====================================')

enem_2023 = pd.read_csv(
    os.path.join(PASTA_2023, 'MICRODADOS_ENEM_2023.csv'),
    sep=';',
    encoding='latin1',
    low_memory=False
)

print('====================================')
print('LENDO DADOS 2024...')
print('====================================')

participantes_2024 = pd.read_csv(
    os.path.join(PASTA_2024, 'PARTICIPANTES_2024.csv'),
    sep=';',
    encoding='latin1',
    low_memory=False
)

resultados_2024 = pd.read_csv(
    os.path.join(PASTA_2024, 'RESULTADOS_2024.csv'),
    sep=';',
    encoding='latin1',
    low_memory=False
)

# =====================================================
# SELEÇÃO DE COLUNAS IMPORTANTES
# =====================================================

print('====================================')
print('SELECIONANDO COLUNAS...')
print('====================================')

colunas_2023 = [
    'SG_UF_PROVA',
    'TP_SEXO',
    'Q006',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT',
    'NU_NOTA_REDACAO'
]

enem_2023 = enem_2023[colunas_2023]

colunas_2024_resultados = [
    'SG_UF_PROVA',
    'NU_NOTA_CN',
    'NU_NOTA_CH',
    'NU_NOTA_LC',
    'NU_NOTA_MT',
    'NU_NOTA_REDACAO'
]

resultados_2024 = resultados_2024[colunas_2024_resultados]

# =====================================================
# LIMPEZA DE DADOS
# =====================================================

print('====================================')
print('REMOVENDO VALORES NULOS...')
print('====================================')

enem_2023 = enem_2023.dropna()
resultados_2024 = resultados_2024.dropna()

# =====================================================
# TRANSFORMAÇÃO DE DADOS
# =====================================================

print('====================================')
print('CRIANDO MÉDIA GERAL...')
print('====================================')

enem_2023['MEDIA_GERAL'] = (
    enem_2023['NU_NOTA_CN'] +
    enem_2023['NU_NOTA_CH'] +
    enem_2023['NU_NOTA_LC'] +
    enem_2023['NU_NOTA_MT']
) / 4

resultados_2024['MEDIA_GERAL'] = (
    resultados_2024['NU_NOTA_CN'] +
    resultados_2024['NU_NOTA_CH'] +
    resultados_2024['NU_NOTA_LC'] +
    resultados_2024['NU_NOTA_MT']
) / 4

# =====================================================
# CRIANDO COLUNA ANO
# =====================================================

enem_2023['ANO'] = 2023
resultados_2024['ANO'] = 2024

# =====================================================
# PADRONIZAÇÃO DE FORMATOS
# =====================================================

enem_2023['TP_SEXO'] = enem_2023['TP_SEXO'].replace({
    'M': 'Masculino',
    'F': 'Feminino'
})

# =====================================================
# INTEGRAÇÃO DE DADOS (CONCAT)
# =====================================================

print('====================================')
print('INTEGRANDO DADOS COM CONCAT...')
print('====================================')

df_final = pd.concat([
    enem_2023,
    resultados_2024
])

# =====================================================
# INTEGRAÇÃO DE DADOS (MERGE)
# EXIGÊNCIA DO PROFESSOR
# =====================================================

print('====================================')
print('CRIANDO DATASET COM MERGE...')
print('====================================')

participantes_estado = (
    participantes_2024
    .groupby('SG_UF_PROVA')
    .size()
    .reset_index(name='TOTAL_PARTICIPANTES')
)

notas_estado = (
    resultados_2024
    .groupby('SG_UF_PROVA')['MEDIA_GERAL']
    .mean()
    .reset_index(name='MEDIA_ESTADO')
)

df_merge = participantes_estado.merge(
    notas_estado,
    on='SG_UF_PROVA'
)

# =====================================================
# SALVANDO DATASETS PROCESSADOS
# =====================================================

print('====================================')
print('SALVANDO DADOS...')
print('====================================')

df_final.to_csv(
    os.path.join(PASTA_PROCESSADOS, 'enem_tratado.csv'),
    index=False
)

df_merge.to_csv(
    os.path.join(PASTA_PROCESSADOS, 'enem_estados.csv'),
    index=False
)

print('====================================')
print('PROCESSAMENTO FINALIZADO!')
print('====================================')

print('\nArquivos gerados:')

print('- enem_tratado.csv')
print('- enem_estados.csv')