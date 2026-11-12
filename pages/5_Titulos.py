from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ARQUIVO = Path(__file__).parent.parent / "data" / "titulos.csv"
CATEGORIAS = ["Internacional", "Nacional", "Interestadual", "Estadual"]

st.set_page_config(page_title="Títulos | Raio-X do Vasco", layout="wide")
st.title("Títulos")

if not ARQUIVO.exists():
    st.error("Arquivo data/titulos.csv não encontrado.")
    st.stop()

tabela = pd.read_csv(ARQUIVO)

# Cada linha tem os anos separados por ponto e vírgula. Aqui viram uma linha por conquista.
tabela["ano"] = tabela["anos"].str.split(";")
conquistas = tabela.explode("ano")
conquistas["ano"] = conquistas["ano"].astype(int)
conquistas["decada"] = (conquistas["ano"] // 10 * 10).astype(str) + "s"

st.write("Principais títulos oficiais do Vasco da Gama.")

colunas = st.columns(len(CATEGORIAS) + 1)
colunas[0].metric("Total", len(conquistas))
for coluna, categoria in zip(colunas[1:], CATEGORIAS):
    coluna.metric(categoria, int((conquistas["categoria"] == categoria).sum()))

# Resumo por competição
st.subheader("Por competição")
resumo = (
    conquistas.groupby(["categoria", "competicao"])
    .agg(titulos=("ano", "size"), primeiro=("ano", "min"), ultimo=("ano", "max"))
    .reset_index()
    .sort_values(["categoria", "titulos"], ascending=[True, False])
)
resumo["categoria"] = pd.Categorical(resumo["categoria"], CATEGORIAS, ordered=True)
resumo = resumo.sort_values(["categoria", "titulos"], ascending=[True, False])
st.dataframe(
    resumo.rename(columns={"categoria": "Categoria", "competicao": "Competição", "titulos": "Títulos",
                           "primeiro": "Primeiro", "ultimo": "Mais recente"}),
    hide_index=True,
    width="stretch",
)

# Gráfico: títulos por década
por_decada = conquistas.groupby(["decada", "categoria"]).size().reset_index(name="titulos")
fig = px.bar(por_decada, x="decada", y="titulos", color="categoria",
             title="Títulos por década",
             labels={"decada": "Década", "titulos": "Títulos", "categoria": "Categoria"},
             category_orders={"categoria": CATEGORIAS})
fig.update_xaxes(type="category")
st.plotly_chart(fig, width="stretch")

# Linha do tempo com todas as conquistas
st.subheader("Todas as conquistas")
escolhidas = st.multiselect("Categorias", CATEGORIAS, default=CATEGORIAS)
lista = conquistas[conquistas["categoria"].isin(escolhidas)].sort_values("ano", ascending=False)
st.dataframe(
    lista[["ano", "competicao", "categoria"]].rename(
        columns={"ano": "Ano", "competicao": "Competição", "categoria": "Categoria"}
    ),
    hide_index=True,
    width="stretch",
)

st.caption(
    "Fontes: Netvasco (lista atualizada em 24/12/2024) e Lance. A lista traz os principais títulos "
    "e não inclui torneios menores nem taças de turno. Em 2025 o Vasco foi vice da Copa do Brasil. "
    "Se houver conquista nova, adicione o ano em data/titulos.csv."
)
