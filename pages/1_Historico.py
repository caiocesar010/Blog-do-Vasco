import plotly.express as px
import streamlit as st

from dados import carregar_jogos, resumo_por_temporada

st.set_page_config(page_title="Histórico | Raio-X do Vasco", layout="wide")
st.title("Histórico no Brasileirão")

jogos = carregar_jogos()

# Filtro de temporadas na barra lateral
menor, maior = int(jogos["temporada"].min()), int(jogos["temporada"].max())
inicio, fim = st.sidebar.slider("Temporadas", menor, maior, (menor, maior))
jogos = jogos[(jogos["temporada"] >= inicio) & (jogos["temporada"] <= fim)]

tabela = resumo_por_temporada(jogos)

# Indicadores do período escolhido
col1, col2, col3, col4 = st.columns(4)
col1.metric("Jogos", int(tabela["jogos"].sum()))
col2.metric("Vitórias", int(tabela["vitorias"].sum()))
col3.metric("Pontos", int(tabela["pontos"].sum()))
col4.metric("Aproveitamento", f"{tabela['pontos'].sum() / (tabela['jogos'].sum() * 3) * 100:.1f}%")

st.caption("O Vasco não aparece em 2009, 2014, 2016 e 2022 porque jogou a Série B, que não está nos dados.")

# Gráfico 1: aproveitamento por temporada
fig1 = px.bar(tabela, x="temporada", y="aproveitamento",
              title="Aproveitamento por temporada (%)",
              labels={"temporada": "Temporada", "aproveitamento": "Aproveitamento (%)"})
fig1.update_xaxes(type="category")  # trata os anos como rótulos, sem buracos
st.plotly_chart(fig1, width="stretch")

# Gráfico 2: vitórias, empates e derrotas empilhados
fig2 = px.bar(tabela, x="temporada", y=["vitorias", "empates", "derrotas"],
              title="Vitórias, empates e derrotas por temporada",
              labels={"temporada": "Temporada", "value": "Jogos", "variable": "Resultado"})
fig2.update_xaxes(type="category")  # trata os anos como rótulos, sem buracos
st.plotly_chart(fig2, width="stretch")

# Gráfico 3: gols marcados e sofridos
fig3 = px.line(tabela, x="temporada", y=["gols_pro", "gols_contra"], markers=True,
               title="Gols marcados e sofridos por temporada",
               labels={"temporada": "Temporada", "value": "Gols", "variable": ""})
fig3.update_xaxes(type="category")  # trata os anos como rótulos, sem buracos
st.plotly_chart(fig3, width="stretch")

# Gráfico 4: casa x fora
por_local = jogos.groupby("local").agg(jogos=("pontos", "size"), pontos=("pontos", "sum")).reset_index()
por_local["aproveitamento"] = (por_local["pontos"] / (por_local["jogos"] * 3) * 100).round(1)
fig4 = px.bar(por_local, x="local", y="aproveitamento", title="Aproveitamento em casa x fora (%)",
              labels={"local": "Local", "aproveitamento": "Aproveitamento (%)"})
st.plotly_chart(fig4, width="stretch")

with st.expander("Ver tabela completa por temporada"):
    st.dataframe(tabela, hide_index=True, width="stretch")
