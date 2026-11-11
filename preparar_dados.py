"""
Etapa 2 do projeto Raio-X do Vasco: preparar os dados.

O que este script faz:
  1. Lê o arquivo de partidas do Brasileirão (todos os clubes)
  2. Fica só com os jogos em que o Vasco foi mandante ou visitante
  3. Cria colunas novas que vamos usar nos gráficos:
       ano, temporada, local (Casa/Fora), adversario, gols_pro, gols_contra,
       resultado (V/E/D) e pontos
  4. Salva tudo em data/vasco_jogos.csv

Como rodar (na pasta raio-x-vasco, com o (.venv) ativo):
  python preparar_dados.py
"""

import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

ARQUIVO_ENTRADA = Path("data") / "campeonato-brasileiro-full.csv"
ARQUIVO_NOVOS = Path("data") / "jogos_novos.csv"
ARQUIVO_SAIDA = Path("data") / "vasco_jogos.csv"
CLUBE = "Vasco"


def carregar(caminho: Path) -> pd.DataFrame:
    if not caminho.exists():
        raise SystemExit(f"Arquivo não encontrado: {caminho}")
    return pd.read_csv(caminho)


def _simplificar(nome: str) -> str:
    """'Atlético-MG' vira 'atleticomg': sem acento, minúsculo e só letras e números."""
    sem_acento = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return "".join(c for c in sem_acento.lower() if c.isalnum())


def padronizar_nomes(novos: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """Troca os nomes dos jogos novos pelos nomes da base histórica quando é claramente o mesmo time.

    Exemplo: 'Botafogo' vira 'Botafogo-RJ' se a base histórica usa esse nome.
    """
    historicos = {}
    for nome in set(df["mandante"].str.strip()) | set(df["visitante"].str.strip()):
        historicos[_simplificar(nome)] = nome

    trocas = {}

    def converter(nome: str) -> str:
        nome = nome.strip()
        chave = _simplificar(nome)
        if chave in historicos:
            novo = historicos[chave]
        else:
            # só troca se existir UM único nome parecido (um contido no outro)
            parecidos = [h for k, h in historicos.items() if chave in k or k in chave]
            novo = parecidos[0] if len(parecidos) == 1 else nome
        if novo != nome:
            trocas[nome] = novo
        return novo

    novos["mandante"] = novos["mandante"].map(converter)
    novos["visitante"] = novos["visitante"].map(converter)
    if trocas:
        print("Nomes ajustados para o padrão da base histórica:", trocas, "\n")
    return novos


def adicionar_jogos_novos(df: pd.DataFrame) -> pd.DataFrame:
    """Junta à base histórica os jogos de 2025 em diante, que você digita em data/jogos_novos.csv."""
    if not ARQUIVO_NOVOS.exists():
        return df
    # sep=None deixa o Pandas descobrir sozinho se o separador é vírgula ou ponto e vírgula
    novos = pd.read_csv(ARQUIVO_NOVOS, sep=None, engine="python")
    if novos.empty:
        return df

    novos = padronizar_nomes(novos, df)

    # Avisa se aparecer um nome de time que não existe na base histórica (pode ser erro de grafia)
    conhecidos = set(df["mandante"].str.strip()) | set(df["visitante"].str.strip())
    usados = set(novos["mandante"].str.strip()) | set(novos["visitante"].str.strip())
    desconhecidos = sorted(usados - conhecidos)
    if desconhecidos:
        print("ATENÇÃO: nomes que não existem na base histórica (confira a grafia):", desconhecidos, "\n")

    print(f"Jogos novos adicionados: {len(novos)}\n")
    return pd.concat([df, novos], ignore_index=True)


def filtrar_vasco(df: pd.DataFrame) -> pd.DataFrame:
    """Mantém só os jogos em que o Vasco aparece como mandante OU visitante."""
    # .str.strip() tira espaços sobrando, para evitar "Vasco " != "Vasco"
    foi_mandante = df["mandante"].str.strip() == CLUBE
    foi_visitante = df["visitante"].str.strip() == CLUBE
    # o símbolo | significa "ou" quando comparamos colunas
    return df[foi_mandante | foi_visitante].copy()


def adicionar_colunas(jogos: pd.DataFrame) -> pd.DataFrame:
    # A coluna "data" vem como texto ("29/03/2003"). Convertemos para data de verdade.
    jogos["data"] = pd.to_datetime(jogos["data"], format="%d/%m/%Y")
    jogos["ano"] = jogos["data"].dt.year

    # Temporada nem sempre é igual ao ano do jogo: o Brasileirão de 2020 atrasou por
    # causa da pandemia e terminou em fevereiro de 2021. Esses jogos pertencem à
    # temporada 2020, então corrigimos aqui.
    jogos["temporada"] = jogos["ano"]
    terminou_em_2021 = (jogos["ano"] == 2021) & (jogos["data"] < pd.Timestamp("2021-03-01"))
    jogos.loc[terminou_em_2021, "temporada"] = 2020

    # O Vasco jogou em casa quando era o mandante
    jogos["local"] = np.where(jogos["mandante"].str.strip() == CLUBE, "Casa", "Fora")

    # Gols a favor, gols contra e adversário dependem de onde o Vasco jogou
    em_casa = jogos["local"] == "Casa"
    jogos["gols_pro"] = np.where(em_casa, jogos["mandante_Placar"], jogos["visitante_Placar"])
    jogos["gols_contra"] = np.where(em_casa, jogos["visitante_Placar"], jogos["mandante_Placar"])
    jogos["adversario"] = np.where(em_casa, jogos["visitante"], jogos["mandante"])

    # Resultado a partir do placar: V = vitória, E = empate, D = derrota
    jogos["resultado"] = np.select(
        [jogos["gols_pro"] > jogos["gols_contra"], jogos["gols_pro"] == jogos["gols_contra"]],
        ["V", "E"],
        default="D",
    )

    # Pontos: vitória vale 3, empate vale 1, derrota vale 0
    jogos["pontos"] = jogos["resultado"].map({"V": 3, "E": 1, "D": 0})

    colunas = ["data", "ano", "temporada", "rodata", "local", "adversario", "gols_pro", "gols_contra",
               "resultado", "pontos", "arena"]
    return jogos[colunas].sort_values("data").reset_index(drop=True)


def main() -> None:
    df = adicionar_jogos_novos(carregar(ARQUIVO_ENTRADA))
    jogos = adicionar_colunas(filtrar_vasco(df))

    jogos.to_csv(ARQUIVO_SAIDA, index=False)
    print(f"Arquivo salvo em {ARQUIVO_SAIDA} com {len(jogos)} jogos do {CLUBE}.\n")

    print("=== Primeiras linhas ===")
    print(jogos.head(), "\n")

    print("=== Resultados no total ===")
    print(jogos["resultado"].value_counts(), "\n")

    print("=== Jogos, pontos e aproveitamento por temporada ===")
    por_temporada = jogos.groupby("temporada").agg(jogos=("pontos", "size"), pontos=("pontos", "sum"))
    por_temporada["aproveitamento_%"] = (por_temporada["pontos"] / (por_temporada["jogos"] * 3) * 100).round(1)
    print(por_temporada.to_string())


if __name__ == "__main__":
    main()
