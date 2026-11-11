"""
Passo 1 do projeto Raio-X do Vasco: conhecer os dados.

Este script NÃO faz gráficos ainda. Ele só responde:
  - Quantas linhas e colunas o arquivo tem?
  - Quais são os nomes das colunas?
  - Quantos jogos do Vasco existem na base?

Como rodar:
  1. Baixe os CSVs do repositório https://github.com/adaoduque/Brasileirao_Dataset
  2. Coloque o arquivo de partidas dentro da pasta data/
  3. Ajuste ARQUIVO abaixo se o nome for diferente
  4. No terminal: python explorar_dados.py
"""

from pathlib import Path

import pandas as pd

# Nome do arquivo de partidas (confira o nome real na pasta data/)
ARQUIVO = Path("data") / "campeonato-brasileiro-full.csv"
CLUBE = "Vasco"


def carregar(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        raise SystemExit(
            f"Arquivo não encontrado: {caminho}\n"
            "Baixe o CSV do dataset e coloque dentro da pasta data/."
        )
    return pd.read_csv(caminho)


def filtrar_clube(df: pd.DataFrame, clube: str) -> pd.DataFrame:
    """Mantém as linhas em que o nome do clube aparece em qualquer coluna de texto.

    Fazemos assim porque ainda não sabemos o nome exato das colunas
    (mandante, visitante...). Quando soubermos, trocamos por um filtro direto.
    """
    colunas_texto = df.select_dtypes(include="object").columns
    mascara = pd.Series(False, index=df.index)
    for coluna in colunas_texto:
        mascara |= df[coluna].astype(str).str.contains(clube, case=False, na=False)
    return df[mascara]


def main() -> None:
    df = carregar(ARQUIVO)

    print("=== Visão geral ===")
    print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}\n")

    print("=== Colunas e tipos ===")
    print(df.dtypes, "\n")

    print("=== Primeiras 5 linhas ===")
    print(df.head(), "\n")

    vasco = filtrar_clube(df, CLUBE)
    print(f"=== Jogos que citam '{CLUBE}': {len(vasco)} ===")
    print(vasco.head())


if __name__ == "__main__":
    main()
