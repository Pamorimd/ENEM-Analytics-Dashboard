# 🎓 ENEM Analytics Dashboard

Dashboard interativo desenvolvido em Python utilizando Dash, Plotly e Pandas para análise exploratória dos microdados do ENEM 2023 e 2024.

---

# 📌 Objetivo

O projeto tem como objetivo realizar uma análise comparativa e exploratória dos dados do ENEM, identificando:

- padrões de desempenho
- desigualdades regionais
- relação entre renda e notas
- distribuição das notas
- comportamento dos participantes

Além da análise estatística, o projeto busca comunicar insights através de dashboards interativos e visualmente organizados.

---

# 🚀 Tecnologias Utilizadas

- Python
- Pandas
- Plotly
- Dash
- Dash Bootstrap Components
- GeoJSON
- HTML/CSS

---

# 📂 Estrutura do Projeto

```bash
Dashboard - Analise de Dados Educacionais/
│
├── dashboard/
│   ├── assets/
│   │   └── style.css
│   ├── app.py
│   ├── callbacks.py
│   ├── layouts.py
│   └── utils.py
│
├── data/
│   ├── enem_2023/
│   ├── enem_2024/
│   └── processed/
│
├── scripts/
│   ├── pipeline_dados.py
│   └── preprocessamento.py
│
├── requirements.txt
└── README.md
```

---

# 📊 Funcionalidades

## Dashboard Executivo
- KPIs principais
- média geral do ENEM
- comparação entre 2023 e 2024
- distribuição das notas
- ranking por estado
- mapa interativo do Brasil

## Dashboard Interativo
- filtros dinâmicos
- análise por estado
- comparação entre variáveis
- distribuição estatística
- análise da redação
- exploração visual dos dados

---

# 🧠 Pipeline de Ciência de Dados

## 1. Aquisição de Dados
Leitura dos microdados do ENEM utilizando Pandas.

## 2. Integração de Dados
Integração de múltiplos arquivos utilizando:
- concat
- merge

## 3. Limpeza e Tratamento
- remoção de valores nulos
- padronização
- preparação para análise

## 4. Transformação
- criação de métricas
- cálculo da média geral
- agregações estatísticas

## 5. Análise Exploratória
Identificação de:
- tendências
- padrões regionais
- relações entre variáveis
- insights relevantes

---

# 🌎 Principais Insights

- Estados do Sudeste apresentaram médias superiores à média nacional.
- Existe relação entre nível socioeconômico e desempenho.
- A redação possui forte impacto na média geral.
- Houve diferenças significativas entre 2023 e 2024.

---

# ▶️ Como Executar

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
```

---

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 3. Executar preprocessamento

```bash
cd scripts
python3 preprocessamento.py
```

---

## 4. Executar dashboard

```bash
cd dashboard
python3 app.py
```

---

## 5. Abrir no navegador

```text
http://127.0.0.1:8051/
```

---

# 📈 Visualizações Disponíveis

- Choropleth Map
- Boxplot
- Histogramas
- Gráficos de barras
- Scatterplots
- Rankings
- KPIs

---

# 📚 Fonte dos Dados

Microdados oficiais do ENEM:

- INEP
- Portal Brasileiro de Dados Abertos

---

# 👨‍💻 Autor

Projeto desenvolvido para a disciplina de Estudos Avançados de Banco de Dados.

---

# ⭐ Considerações

Este projeto busca unir:
- análise de dados
- visualização interativa
- storytelling com dados
- comunicação visual

seguindo boas práticas de Data Science e Dashboard Design.