"""
Funções que carregam e resumem os dados do Vasco.

Ficam num arquivo separado para as várias páginas do site usarem o mesmo código.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

ARQUIVO = Path(__file__).parent / "data" / "vasco_jogos.csv"


@st.cache_data  # guarda o resultado na memória para o site não reler o CSV a cada clique
def carregar_jogos() -> pd.DataFrame:
    if not ARQUIVO.exists():
        st.error("Arquivo data/vasco_jogos.csv não encontrado. Rode 'python preparar_dados.py' primeiro.")
        st.stop()
    return pd.read_csv(ARQUIVO, parse_dates=["data"])


def resumo_por_temporada(jogos: pd.DataFrame) -> pd.DataFrame:
    """Uma linha por temporada: jogos, V/E/D, pontos, gols e aproveitamento."""
    tabela = jogos.groupby("temporada").agg(
        jogos=("pontos", "size"),
        pontos=("pontos", "sum"),
        vitorias=("resultado", lambda s: (s == "V").sum()),
        empates=("resultado", lambda s: (s == "E").sum()),
        derrotas=("resultado", lambda s: (s == "D").sum()),
        gols_pro=("gols_pro", "sum"),
        gols_contra=("gols_contra", "sum"),
    ).reset_index()
    tabela["aproveitamento"] = (tabela["pontos"] / (tabela["jogos"] * 3) * 100).round(1)
    # Como texto, o gráfico não deixa "buracos" nos anos em que o Vasco estava na Série B
    tabela["temporada"] = tabela["temporada"].astype(str)
    return tabela
