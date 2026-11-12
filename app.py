from pathlib import Path

import pandas as pd
import streamlit as st

from dados import carregar_jogos

ARQUIVO_PROXIMOS = Path(__file__).parent / "data" / "proximos_jogos.csv"
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

st.set_page_config(page_title="Raio-X do Vasco", layout="wide")

jogos = carregar_jogos()

st.title("Raio-X do Vasco")
st.write("Números e história do Vasco da Gama no Campeonato Brasileiro, atualizados aos poucos.")

temporada_atual = int(jogos["temporada"].max())
atual = jogos[jogos["temporada"] == temporada_atual]

total = len(atual)
vitorias = int((atual["resultado"] == "V").sum())
empates = int((atual["resultado"] == "E").sum())
derrotas = int((atual["resultado"] == "D").sum())
aproveitamento = atual["pontos"].sum() / (total * 3) * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(f"Jogos no Brasileirão {temporada_atual}", total)
col2.metric("Vitórias", vitorias)
col3.metric("Empates", empates)
col4.metric("Derrotas", derrotas)
col5.metric("Aproveitamento", f"{aproveitamento:.1f}%")


# Próximos jogos: lidos de data/proximos_jogos.csv
st.subheader("Próximos jogos")
if ARQUIVO_PROXIMOS.exists():
    proximos = pd.read_csv(ARQUIVO_PROXIMOS)
    proximos["inicio"] = pd.to_datetime(proximos["data"] + " " + proximos["hora"], format="%d/%m/%Y %H:%M")

    # Horário de Brasília = UTC menos 3 horas (o site publicado roda em UTC)
    agora = pd.Timestamp.now(tz="UTC").tz_localize(None) - pd.Timedelta(hours=3)
    # O jogo continua na lista até 2 horas depois do início
    proximos = proximos[proximos["inicio"] + pd.Timedelta(hours=2) >= agora]
    proximos = proximos.sort_values("inicio").head(5)

    if proximos.empty:
        st.info("Nenhum jogo futuro cadastrado. Atualize o arquivo data/proximos_jogos.csv.")
    else:
        tabela = pd.DataFrame({
            "Data": proximos["inicio"].apply(lambda d: f"{DIAS[d.weekday()]} {d:%d/%m}"),
            "Hora": proximos["inicio"].dt.strftime("%H:%M"),
            "Jogo": proximos["mandante"] + " x " + proximos["visitante"],
            "Competição": proximos["competicao"] + " - " + proximos["rodada"],
            "Estádio": proximos["estadio"],
        })
        st.dataframe(tabela, hide_index=True, width="stretch")
    st.caption("Datas e horários (de Brasília) podem mudar por decisão da CBF ou das emissoras.")
else:
    st.info("Arquivo data/proximos_jogos.csv não encontrado.")

st.subheader("Últimos jogos do time ")
ultimos = jogos.sort_values("data", ascending=False).head(5).copy()
ultimos["data"] = ultimos["data"].dt.strftime("%d/%m/%Y")
st.dataframe(
    ultimos[["data", "local", "adversario", "gols_pro", "gols_contra", "resultado"]].rename(
        columns={"data": "Data", "local": "Local", "adversario": "Adversário",
                 "gols_pro": "Gols do Vasco", "gols_contra": "Gols do adversário",
                 "resultado": "Resultado"}
    ),
    hide_index=True,
    width="stretch",
)

st.caption("Use o menu à esquerda para abrir as outras páginas. Dados: Brasileirão 2003-2026.")
