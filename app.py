import streamlit as st

from dados import carregar_jogos

st.set_page_config(page_title="Raio-X do Vasco", layout="wide")

jogos = carregar_jogos()

st.title("Raio-X do Vasco")
st.write("Números e história do Vasco da Gama no Campeonato Brasileiro, atualizados aos poucos.")

total = len(jogos)
vitorias = (jogos["resultado"] == "V").sum()
aproveitamento = jogos["pontos"].sum() / (total * 3) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Jogos na base", total)
col2.metric("Vitórias", int(vitorias))
col3.metric("Aproveitamento geral", f"{aproveitamento:.1f}%")

st.subheader("Últimos jogos da base")
ultimos = jogos.sort_values("data", ascending=False).head(5).copy()
ultimos["data"] = ultimos["data"].dt.strftime("%d/%m/%Y")
st.dataframe(
    ultimos[["data", "local", "adversario", "gols_pro", "gols_contra", "resultado"]],
    hide_index=True,
    width="stretch",
)

st.caption("Use o menu à esquerda para abrir as outras páginas. Dados: Brasileirão 2003-2024.")
