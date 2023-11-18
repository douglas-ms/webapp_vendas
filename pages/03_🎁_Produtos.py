import streamlit as st
import pandas as pd
from datetime import datetime
from utilidades import leitura_de_dados

# Configuração da página Streamlit
st.set_page_config(
    page_title="Produtos",  # Título da página
    page_icon="🎁",       # Ícone da página
    layout="wide"         # Layout amplo
)

# Carrega os dados utilizando a função personalizada
leitura_de_dados()

# Carrega DataFrames da sessão
df_vendas = st.session_state['dados']['df_vendas']
df_lojas = st.session_state['dados']['df_lojas']

# Redefine o índice do DataFrame e seleciona colunas específicas
df_data = pd.merge(df_vendas, df_lojas, on='ID Loja', how='left')
df_data = df_data.reset_index()

# Seleciona as colunas relevantes e formata a coluna de data
df_data = df_data[['Data','Produto', 'Quantidade', 'Valor Unitário', 'Valor Final', 'Loja']]
df_data['Data'] = df_data['Data'].dt.strftime('%d/%m/%Y')

st.markdown("# Detalhamento dos Produtos")

produtos = df_data['Produto'].unique()
produto = st.sidebar.selectbox("Produtos", produtos)

st.divider()

# Converte e formata dados temporais para criar um gráfico de linhas
df_data['Data'] = pd.to_datetime(df_data['Data'], format='%d/%m/%Y')
df_data['Mês/Ano'] = df_data['Data'].dt.to_period('M')
df_data['Mês/Ano'] = df_data['Mês/Ano'].dt.strftime('%Y-%m')

df_data = df_data.drop(columns=['Data','Valor Unitário'], axis=1)
df_data_agrupado = df_data.groupby(['Mês/Ano','Loja','Produto'])[['Quantidade','Valor Final']].sum().reset_index()
df_data_agrupado.set_index('Mês/Ano')
df_data_agrupado['Ticket_Medio'] = df_data_agrupado['Valor Final'] / df_data_agrupado['Quantidade']

df_data_agrupado_qtde = df_data.groupby(['Produto'])[['Quantidade','Valor Final']].sum().reset_index()
# produto_mais_vendido = df_data_agrupado.loc(['Quantidade'].idxmax())['Produto']
# produto_maior_quantidade = df_data_agrupado.loc(['Quantidade'].idxmax())['Quantidade']

# Encontre o produto com o maior ticket médio
produto_maior_ticket_medio = df_data_agrupado.loc[df_data_agrupado['Ticket_Medio'].idxmax()]['Produto']
maior_tkt = df_data_agrupado.loc[df_data_agrupado['Ticket_Medio'].idxmax()]['Ticket_Medio']

st.markdown(f"#### Produto com Maior Tkt é o/a: {produto_maior_ticket_medio} no valor de R$: {maior_tkt}")
# st.markdown(f"#### Produto mais vendido é o/a: {produto_mais_vendido} com {produto_maior_quantidade} unidades")

st.divider()

df_data_agrupado =df_data_agrupado[df_data_agrupado['Produto'] == produto]

st.dataframe(df_data_agrupado)