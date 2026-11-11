from datetime import datetime
from pathlib import Path

import streamlit as st

# A pasta posts/ fica um nível acima da pasta pages/
PASTA_POSTS = Path(__file__).parent.parent / "posts"

st.set_page_config(page_title="Diário | Raio-X do Vasco", layout="wide")
st.title("Diário do Vasco")
st.write("Um texto por dia, com números e curiosidades.")

# O nome de cada arquivo começa com a data (2026-11-11-titulo.md),
# então ordenar pelo nome já deixa os mais recentes primeiro.
arquivos = sorted(PASTA_POSTS.glob("*.md"), reverse=True)

if not arquivos:
    st.info("Ainda não há textos. Crie um arquivo .md dentro da pasta posts/.")
    st.stop()

for arquivo in arquivos:
    # Os 10 primeiros caracteres do nome são a data no formato AAAA-MM-DD
    try:
        data = datetime.strptime(arquivo.stem[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        data = ""

    st.caption(data)
    st.markdown(arquivo.read_text(encoding="utf-8"))
    st.divider()
