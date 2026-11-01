import numpy as np
import pandas as pd
from limpeza import ROTULOS_CONSULTAS


def estatisticas_peso(df):
    pesos = df["peso"].to_numpy()
    return {
        "media": np.mean(pesos),
        "mediana": np.median(pesos),
        "desvio": np.std(pesos),
        "minimo": np.min(pesos),
        "maximo": np.max(pesos),
    }


def percentual_baixo_peso(df):
    return df["baixo_peso"].mean() * 100


def percentual_prematuro(df):
    conhecidos = df[df["gestacao_cod"].notna()]     # ignora gestação ignorada
    if len(conhecidos) == 0:
        return 0.0
    return conhecidos["prematuro"].mean() * 100


def distribuicao_percentual(df, coluna):
    return (df[coluna].value_counts(normalize=True) * 100).round(1)


def peso_medio_por_consultas(df):
    media = df.groupby("consultas_cod")["peso"].mean().round(0)
    media.index = [ROTULOS_CONSULTAS.get(int(c), str(c)) for c in media.index]
    return media


def nascimentos_por_ano(df):
    return df.groupby("ano").size()


def taxa_mortalidade_infantil(obitos, nascidos):
    """Óbitos de menores de 1 ano por 1.000 nascidos vivos."""
    if nascidos == 0:
        return 0.0
    return obitos / nascidos * 1000


def tabela_taxa(sinasc, sim, coluna):
    """Taxa de mortalidade infantil agrupada por 'ano' ou 'municipio'."""
    nascidos = sinasc.groupby(coluna).size()
    obitos = sim.groupby(coluna).size()
    tabela = pd.DataFrame({"nascidos": nascidos, "obitos": obitos}).fillna(0)
    tabela = tabela[tabela["nascidos"] > 0].astype(int)
    tabela["taxa_por_mil"] = (tabela["obitos"] / tabela["nascidos"] * 1000).round(2)
    return tabela


def contar_por_faixa_obito(sim):
    return sim["faixa_obito"].value_counts()


def principais_causas(sim, quantidade=10):
    categorias = sim["causa"].str[:3]       # categoria da CID-10 (3 caracteres)
    return categorias.value_counts().head(quantidade)