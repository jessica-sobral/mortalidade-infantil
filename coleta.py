from pathlib import Path
import pandas as pd

PASTA_BRUTOS = Path("dados/brutos")


def arquivo_existe(caminho):
    return caminho.exists() and caminho.is_file()


def carregar_csv(nome_arquivo, tipos=None, colunas=None, separador=";"):
    """Lê um CSV de dados/brutos. Devolve None se não for possível ler.

    tipos     -> dicionário {coluna: tipo}, ex.: {"DTNASC": str}
    colunas   -> lista de colunas a ler (economiza memória em arquivos grandes)
    separador -> ";" ou ",", conforme o arquivo baixado
    """
    caminho = PASTA_BRUTOS / nome_arquivo

    if not arquivo_existe(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        print("Confira o nome e se o arquivo está na pasta dados/brutos/.")
        return None

    try:
        df = pd.read_csv(caminho, sep=separador, encoding="utf-8",
                         dtype=tipos, usecols=colunas)
    except UnicodeDecodeError:
        print("Codificação diferente de UTF-8. Tentando latin-1...")
        df = pd.read_csv(caminho, sep=separador, encoding="latin-1",
                         dtype=tipos, usecols=colunas)
    except PermissionError:
        print("Sem permissão para ler o arquivo.")
        return None
    except ValueError as erro:
        print("Alguma coluna esperada não existe no arquivo (ou o separador está errado).")
        print("Detalhe:", erro)
        return None

    print(f"{nome_arquivo}: {df.shape[0]} linhas e {df.shape[1]} colunas")
    return df


def filtrar_uf(df, coluna_municipio, codigo_uf):
    """Mantém só os municípios de uma UF (ex.: "35" = São Paulo). None = sem filtro."""
    if codigo_uf is None:
        return df
    inicio = df[coluna_municipio].astype(str).str[:2]
    return df[inicio == codigo_uf].copy()


def resumo_rapido(df):
    """Mostra a estrutura do arquivo para inspeção inicial."""
    print(df.head())
    print("Colunas:", df.columns.tolist())
    print("Valores nulos por coluna:")
    print(df.isnull().sum())