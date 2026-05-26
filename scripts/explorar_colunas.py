import pandas as pd

# =====================================
# ARQUIVOS
# =====================================

arquivo_2023 = '../data/enem_2023/MICRODADOS_ENEM_2023.csv'

arquivo_2024_participantes = '../data/enem_2024/PARTICIPANTES_2024.csv'

arquivo_2024_resultados = '../data/enem_2024/RESULTADOS_2024.csv'

# =====================================
# FUNÇÃO
# =====================================

def explorar_arquivo(nome, caminho):

    print('\n' + '=' * 60)
    print(f'ARQUIVO: {nome}')
    print('=' * 60)

    df = pd.read_csv(
        caminho,
        nrows=5,
        sep=';',
        encoding='latin1',
        low_memory=False
    )

    print('\nTOTAL DE COLUNAS:')
    print(len(df.columns))

    print('\nCOLUNAS:')
    print(df.columns.tolist())

    print('\nTIPOS:')
    print(df.dtypes)

    print('\nAMOSTRA:')
    print(df.head())


# =====================================
# EXECUÇÃO
# =====================================

explorar_arquivo(
    'ENEM 2023',
    arquivo_2023
)

explorar_arquivo(
    'PARTICIPANTES 2024',
    arquivo_2024_participantes
)

explorar_arquivo(
    'RESULTADOS 2024',
    arquivo_2024_resultados
)

# =====================================
# COMPARAÇÃO DE COLUNAS
# =====================================

df_2023 = pd.read_csv(
    arquivo_2023,
    nrows=1,
    sep=';',
    encoding='latin1'
)

df_2024_part = pd.read_csv(
    arquivo_2024_participantes,
    nrows=1,
    sep=';',
    encoding='latin1'
)

df_2024_res = pd.read_csv(
    arquivo_2024_resultados,
    nrows=1,
    sep=';',
    encoding='latin1'
)

colunas_2023 = set(df_2023.columns)

colunas_2024 = set(
    list(df_2024_part.columns)
    + list(df_2024_res.columns)
)

# =====================================
# COLUNAS EM COMUM
# =====================================

comum = colunas_2023.intersection(colunas_2024)

print('\n' + '=' * 60)
print('COLUNAS EM COMUM')
print('=' * 60)

for coluna in sorted(comum):
    print(coluna)

# =====================================
# APENAS 2023
# =====================================

somente_2023 = colunas_2023 - colunas_2024

print('\n' + '=' * 60)
print('COLUNAS APENAS EM 2023')
print('=' * 60)

for coluna in sorted(somente_2023):
    print(coluna)

# =====================================
# APENAS 2024
# =====================================

somente_2024 = colunas_2024 - colunas_2023

print('\n' + '=' * 60)
print('COLUNAS APENAS EM 2024')
print('=' * 60)

for coluna in sorted(somente_2024):
    print(coluna)