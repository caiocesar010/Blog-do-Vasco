import pandas as pd
import plotly.express as px
import streamlit as st

from dados import carregar_jogos

st.set_page_config(page_title="Rivais | Raio-X do Vasco", layout="wide")
st.title("Retrospecto contra cada adversário")

jogos = carregar_jogos()

# Uma linha por adversário, com o balanço de todos os jogos contra ele
ranking = jogos.groupby("adversario").agg(
    jogos=("pontos", "size"),
    pontos=("pontos", "sum"),
    vitorias=("resultado", lambda s: (s == "V").sum()),
    empates=("resultado", lambda s: (s == "E").sum()),
    derrotas=("resultado", lambda s: (s == "D").sum()),
    gols_pro=("gols_pro", "sum"),
    gols_contra=("gols_contra", "sum"),
).reset_index()
ranking["aproveitamento"] = (ranking["pontos"] / (ranking["jogos"] * 3) * 100).round(1)
ranking = ranking.sort_values("jogos", ascending=False)

# Caixa de seleção: os adversários mais enfrentados aparecem primeiro
adversario = st.selectbox("Escolha o adversário", ranking["adversario"])

linha = ranking[ranking["adversario"] == adversario].iloc[0]
confrontos = jogos[jogos["adversario"] == adversario].sort_values("data", ascending=False)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Jogos", int(linha["jogos"]))
col2.metric("Vitórias", int(linha["vitorias"]))
col3.metric("Empates", int(linha["empates"]))
col4.metric("Derrotas", int(linha["derrotas"]))
col5.metric("Aproveitamento", f"{linha['aproveitamento']:.1f}%")

st.write(f"Gols: **{int(linha['gols_pro'])}** marcados e **{int(linha['gols_contra'])}** sofridos.")

resumo = pd.DataFrame({
    "Resultado": ["Vitórias", "Empates", "Derrotas"],
    "Jogos": [linha["vitorias"], linha["empates"], linha["derrotas"]],
})
fig = px.bar(resumo, x="Resultado", y="Jogos", title=f"Vasco x {adversario}")
st.plotly_chart(fig, width="stretch")


with st.expander("Ver o retrospecto contra todos os adversários"):
    st.dataframe(ranking, hide_index=True, width="stretch")
