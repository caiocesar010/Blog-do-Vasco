# Raio-X do Vasco

Site com estatísticas e história do Vasco da Gama no Campeonato Brasileiro, feito em Python (Pandas + Plotly + Streamlit) e atualizado por mim a cada rodada.

**Acesse o site:** https://raio-x-vasco.streamlit.app


https://github.com/user-attachments/assets/0d0b2144-25f0-4c1a-858e-92325a659d2b



## O que tem no site

- **Página inicial:** números do Vasco no Brasileirão atual, próximos jogos, classificação completa e últimos resultados.
- **Histórico:** desempenho do Vasco em cada temporada desde 2003 (aproveitamento, vitórias, empates, derrotas, gols, casa x fora).
- **Rivais:** retrospecto contra cada adversário.
- **Elenco:** jogadores do time profissional por posição.
- **Títulos:** principais conquistas do clube, com gráfico por década.

## Estrutura de pastas

```
raio-x-vasco/
├── data/                  # CSVs (histórico, jogos recentes, elenco, títulos, classificação)
├── pages/                 # páginas do site (Histórico, Rivais, Elenco, Títulos)
├── app.py                 # página inicial
├── dados.py               # leitura e resumo dos dados
├── preparar_dados.py      # monta data/vasco_jogos.csv a partir dos jogos
├── explorar_dados.py      # script para conhecer os dados
├── requirements.txt
└── README.md
```

## Dados e créditos

- Brasileirão 2003–2024: [Brasileirao_Dataset](https://github.com/adaoduque/Brasileirao_Dataset) (crédito ao autor do repositório).
- Jogos de 2025 e 2026, elenco e títulos: compilados de imprensa esportiva (Netvasco, Lance e outros) e podem conter pequenas imprecisões.
- Classificação do Brasileirão 2026: [ValorFinal](https://valorfinal.com.br/brasileirao/dados-abertos), licença CC BY 4.0.

## Como rodar no seu computador

```bash
python -m venv .venv
.venv\Scripts\activate.bat       # Windows (cmd)
source .venv/bin/activate        # Mac/Linux
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologias

Python, Pandas, Plotly, Streamlit.
