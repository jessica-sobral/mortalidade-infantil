from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

import analise

PASTA_RESULTADOS = Path("resultados")
LIMITE_BAIXO_PESO = 2500


def salvar(nome_base):
    """Salva o gráfico atual em PNG (300 dpi) e PDF, como na Aula 10, e fecha a figura."""
    PASTA_RESULTADOS.mkdir(exist_ok=True)
    plt.tight_layout()
    plt.savefig(PASTA_RESULTADOS / f"{nome_base}.png", dpi=300, bbox_inches="tight")
    plt.savefig(PASTA_RESULTADOS / f"{nome_base}.pdf", bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo em: resultados/{nome_base}.png (e .pdf)")


def nascimentos_por_mes(df):
    """Devolve (rótulos aaaa-mm, valores) com o nº de nascimentos por mês."""
    contagem = df.groupby(["ano", "mes"]).size()
    rotulos = [f"{ano}-{int(mes):02d}" for ano, mes in contagem.index]
    return rotulos, contagem.values


# ---------- Gráfico de linhas: evolução no tempo ----------
def linha_matplotlib(df):
    plt.rcdefaults()
    rotulos, valores = nascimentos_por_mes(df)
    plt.figure(figsize=(10, 4))
    plt.plot(rotulos, valores, marker="o", linestyle="--", label="Nascimentos")
    plt.title("Evolução mensal dos nascimentos", fontsize=16)
    plt.xlabel("Mês")
    plt.ylabel("Nascimentos")
    plt.xticks(rotulos[::3], rotation=45)
    plt.legend()
    plt.grid(alpha=0.25)
    salvar("aula10_linha_matplotlib")


def linha_seaborn(df):
    sns.set_theme(style="whitegrid")
    rotulos, valores = nascimentos_por_mes(df)
    plt.figure(figsize=(10, 4))
    sns.lineplot(x=rotulos, y=valores, marker="o")
    plt.title("Evolução mensal dos nascimentos", fontsize=16)
    plt.xlabel("Mês")
    plt.ylabel("Nascimentos")
    plt.xticks(rotulos[::3], rotation=45)
    salvar("aula10_linha_seaborn")


# ---------- Gráfico de barras: comparar categorias ----------
def barras_matplotlib(serie, titulo, rotulo, nome_base, horizontal=False):
    plt.rcdefaults()
    categorias = [str(i) for i in serie.index]
    plt.figure(figsize=(9, 4))
    if horizontal:
        plt.barh(categorias, serie.values, color="teal")
        plt.xlabel(rotulo)
    else:
        plt.bar(categorias, serie.values, color="teal")
        plt.ylabel(rotulo)
    plt.title(titulo)
    salvar(nome_base)


def barras_seaborn(serie, titulo, rotulo, nome_base):
    sns.set_theme(style="ticks")
    categorias = [str(i) for i in serie.index]
    plt.figure(figsize=(9, 4))
    sns.barplot(x=categorias, y=serie.values, errorbar=None)
    plt.title(titulo)
    plt.ylabel(rotulo)
    salvar(nome_base)


# ---------- Histograma: distribuição de valores numéricos ----------
def histograma_matplotlib(df):
    plt.rcdefaults()
    plt.figure(figsize=(9, 4))
    plt.hist(df["peso"], bins=30, edgecolor="white")
    plt.axvline(LIMITE_BAIXO_PESO, color="red", linestyle="--", label="Limite de baixo peso (2.500 g)")
    plt.title("Distribuição do peso ao nascer")
    plt.xlabel("Peso (g)")
    plt.ylabel("Frequência")
    plt.legend()
    salvar("aula10_histograma_matplotlib")


def histograma_seaborn(df):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(9, 4))
    sns.histplot(data=df, x="peso", bins=30)
    plt.axvline(LIMITE_BAIXO_PESO, color="red", linestyle="--", label="Limite de baixo peso (2.500 g)")
    plt.title("Distribuição do peso ao nascer")
    plt.xlabel("Peso (g)")
    plt.ylabel("Frequência")
    plt.legend()
    salvar("aula10_histograma_seaborn")


# ---------- Dispersão: relação entre variáveis ----------
def dispersao_matplotlib(df):
    plt.rcdefaults()
    amostra = df.sample(min(len(df), 1000), random_state=1)
    plt.figure(figsize=(9, 4))
    plt.scatter(amostra["idade_mae"], amostra["peso"], alpha=0.4)
    plt.title("Idade da mãe x peso ao nascer (amostra de 1.000)")
    plt.xlabel("Idade da mãe")
    plt.ylabel("Peso (g)")
    salvar("aula10_dispersao_matplotlib")


def dispersao_seaborn(df):
    sns.set_theme(style="whitegrid")
    amostra = df.sample(min(len(df), 1000), random_state=1)
    plt.figure(figsize=(9, 4))
    sns.scatterplot(data=amostra, x="idade_mae", y="peso", alpha=0.4)
    plt.title("Idade da mãe x peso ao nascer (amostra de 1.000)")
    plt.xlabel("Idade da mãe")
    plt.ylabel("Peso (g)")
    salvar("aula10_dispersao_seaborn")


def gerar_todos(sinasc):
    """Gera cada gráfico nas duas versões (Matplotlib e Seaborn) para comparação."""
    parto = analise.distribuicao_percentual(sinasc, "parto")
    escolaridade = analise.distribuicao_percentual(sinasc, "escolaridade")

    linha_matplotlib(sinasc)
    linha_seaborn(sinasc)
    barras_matplotlib(parto, "Nascimentos por tipo de parto", "%", "aula10_barras_matplotlib")
    barras_seaborn(parto, "Nascimentos por tipo de parto", "%", "aula10_barras_seaborn")
    barras_matplotlib(escolaridade, "Escolaridade da mãe", "%", "aula10_barras_horizontais",
                      horizontal=True)
    histograma_matplotlib(sinasc)
    histograma_seaborn(sinasc)
    dispersao_matplotlib(sinasc)
    dispersao_seaborn(sinasc)
    plt.rcdefaults()      # devolve o estilo padrão para os demais gráficos do projeto