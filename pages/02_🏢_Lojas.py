# Importação das bibliotecas necessárias
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utilidades import leitura_de_dados  # Importação da função personalizada

# Configuração da página Streamlit
st.set_page_config(
    page_title="Lojas",  # Título da página
    page_icon="🏢",       # Ícone da página
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

# Obtém a lista de lojas únicas e permite ao usuário selecionar uma loja
lojas = df_data['Loja'].unique()
loja = st.sidebar.selectbox('Loja', lojas)

# Filtra os dados para a loja selecionada
df_data_filtered = df_data[df_data['Loja'] == loja]

# Cálculos de faturamento total e médio para todos os dados e a loja selecionada
faturamento_total = df_data['Valor Final'].sum()
quantidade_total = df_data['Quantidade'].sum()
ticket_medio_total = faturamento_total / quantidade_total

faturamento_loja = df_data_filtered['Valor Final'].sum()
quantidade_loja = df_data_filtered['Quantidade'].sum()
ticket_medio_loja = faturamento_loja / quantidade_loja

# Cria um título para a loja selecionada
st.markdown(f"# {loja}")

# Adiciona um divisor
st.divider()

# Divide a tela em duas colunas
col1, col2 = st.columns(2)

# Exibe informações de faturamento e ticket médio para o grupo de lojas
col1.markdown(f"##### Faturamento Grupo R$: {faturamento_total/1000000:.2f} milhões")
col2.markdown(f"##### Ticket Medio R$: {ticket_medio_total:.2f}")

# Divide a tela em mais duas colunas
col3, col4 = st.columns(2)

# Exibe informações de faturamento e ticket médio para a loja selecionada
col3.markdown(f"##### Faturamento Loja R$: {faturamento_loja/1000000:.2f} milhões")
col4.markdown(f"##### Ticket Medio R$: {ticket_medio_loja:.2f}")

# Adiciona outro divisor
st.divider()

# Converte e formata dados temporais para criar um gráfico de linhas
df_data_filtered['Data'] = pd.to_datetime(df_data_filtered['Data'], format='%d/%m/%Y')
df_data_filtered['Mês/Ano'] = df_data_filtered['Data'].dt.to_period('M')
df_data_filtered['Mês/Ano'] = df_data_filtered['Mês/Ano'].dt.strftime('%Y-%m')

# Agrupa dados por mês/ano e calcula o faturamento mensal
df_faturamento_mensal = df_data_filtered.groupby('Mês/Ano')['Valor Final'].sum().reset_index()

# Cria um gráfico de linhas usando Plotly Express
fig = px.line(df_faturamento_mensal, x='Mês/Ano', y='Valor Final', title=f'Faturamento Mensal da Loja {loja}')
fig.update_xaxes(title_text='Mês/Ano')
fig.update_yaxes(title_text='Faturamento')

# Exibe o gráfico no aplicativo
st.plotly_chart(fig)

# Adiciona outro divisor
st.divider()

# Exibe um DataFrame com os detalhes dos dados da loja selecionada
st.dataframe(df_data_filtered)
