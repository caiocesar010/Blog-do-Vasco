# Raio-X do Vasco

Site com estatísticas e história do Vasco da Gama, feito em Python (Pandas + Plotly + Streamlit) e atualizado diariamente, como um diário com números.

> Projeto em construção.

## Estrutura de pastas

```
raio-x-vasco/
├── data/                 # CSVs (histórico do Brasileirão e jogos da temporada)
├── pages/                # páginas do site (Histórico, Rivais, Temporada, Diário)
├── posts/                # um arquivo .md por dia para o Diário
├── explorar_dados.py     # script para conhecer os dados
├── app.py                # página inicial do site (vem depois)
├── requirements.txt
└── README.md
```

## Dados

- Brasileirão 2003–2024: [Brasileirao_Dataset](https://github.com/adaoduque/Brasileirao_Dataset) (crédito ao autor do repositório).
- Temporada atual: `data/jogos_atual.csv`, atualizado manualmente após cada partida.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate           # Windows
source .venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
python explorar_dados.py
```

## Roteiro

- [ ] **Etapa 0:** preparar o ambiente (Python, VS Code, pasta, ambiente virtual)
- [ ] **Etapa 1:** explorar os dados (`explorar_dados.py`)
- [ ] **Etapa 2:** limpar e filtrar só os jogos do Vasco (resultado e pontos por jogo)
- [ ] **Etapa 3:** página Histórico (indicadores e gráficos por temporada)
- [ ] **Etapa 4:** página Rivais (retrospecto por adversário)
- [ ] **Etapa 5:** página Diário (posts em Markdown)
- [ ] **Etapa 6:** página Temporada atual (`jogos_atual.csv`)
- [ ] **Etapa 7:** publicar no Streamlit Cloud e colocar o link aqui
- [ ] **Depois:** automatizar a atualização com GitHub Actions

## Tecnologias

Python, Pandas, Plotly, Streamlit.
