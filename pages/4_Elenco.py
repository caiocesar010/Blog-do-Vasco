from pathlib import Path

import pandas as pd
import streamlit as st

ARQUIVO = Path(__file__).parent.parent / "data" / "elenco.csv"

# Agrupa as posições do arquivo em blocos maiores para exibir na página
GRUPOS = {
    "Goleiro": "Goleiros",
    "Lateral-direito": "Laterais",
    "Lateral-esquerdo": "Laterais",
    "Zagueiro": "Zagueiros",
    "Volante": "Volantes",
    "Meia": "Meias",
    "Atacante": "Atacantes",
}
ORDEM = ["Goleiros", "Laterais", "Zagueiros", "Volantes", "Meias", "Atacantes"]

st.set_page_config(page_title="Elenco | Raio-X do Vasco", layout="wide")
st.title("Elenco")

if not ARQUIVO.exists():
    st.error("Arquivo data/elenco.csv não encontrado.")
    st.stop()

elenco = pd.read_csv(ARQUIVO)
elenco["grupo"] = elenco["posicao"].map(GRUPOS)
elenco["observacao"] = elenco["observacao"].fillna("")
# Camisa vazia (reforço sem número definido) aparece em branco em vez de <NA>
elenco["numero"] = elenco["numero"].astype("Int64").astype(str).replace("<NA>", "")

st.info(
    "Lista montada a partir de matérias de imprensa (Netvasco e Lance) publicadas entre abril e "
    "setembro de 2026. Não inclui jogadores da base nem possíveis saídas recentes. "
    "Para atualizar, edite o arquivo data/elenco.csv."
)

colunas = st.columns(len(ORDEM) + 1)
colunas[0].metric("Jogadores", len(elenco))
for coluna, grupo in zip(colunas[1:], ORDEM):
    coluna.metric(grupo, int((elenco["grupo"] == grupo).sum()))

escolhidos = st.multiselect("Posições", ORDEM, default=ORDEM)

for grupo in ORDEM:
    if grupo not in escolhidos:
        continue
    bloco = elenco[elenco["grupo"] == grupo]
    st.subheader(grupo)
    st.dataframe(
        bloco[["numero", "nome", "posicao", "observacao"]].rename(
            columns={"numero": "Nº", "nome": "Jogador", "posicao": "Posição", "observacao": "Observação"}
        ),
        hide_index=True,
        width="stretch",
    )
