from pathlib import Path
import matplotlib.pyplot as plt

PASTA_RESULTADOS = Path("resultados")


def salvar_figura(fig, nome_arquivo):
    PASTA_RESULTADOS.mkdir(exist_ok=True)
    caminho = PASTA_RESULTADOS / nome_arquivo
    fig.savefig(caminho, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Gráfico salvo em:", caminho)


def histograma_peso(df):
    fig, ax = plt.subplots()
    ax.hist(df["peso"], bins=30, edgecolor="black")
    ax.axvline(2500, color="red", linestyle="--", label="Limite de baixo peso (2.500 g)")
    ax.set_title("Distribuição do peso ao nascer")
    ax.set_xlabel("Peso (g)")
    ax.set_ylabel("Nascimentos")
    ax.legend()
    salvar_figura(fig, "histograma_peso.png")


def barras(serie, titulo, rotulo_y, nome_arquivo):
    fig, ax = plt.subplots()
    ax.bar([str(i) for i in serie.index], serie.values)
    ax.set_title(titulo)
    ax.set_ylabel(rotulo_y)
    ax.tick_params(axis="x", labelrotation=30)
    salvar_figura(fig, nome_arquivo)


def linha(serie, titulo, rotulo_y, nome_arquivo):
    fig, ax = plt.subplots()
    ax.plot([str(i) for i in serie.index], serie.values, marker="o")
    ax.set_title(titulo)
    ax.set_ylabel(rotulo_y)
    salvar_figura(fig, nome_arquivo)


def dispersao_idade_peso(df):
    amostra = df.sample(min(len(df), 1000), random_state=1)
    fig, ax = plt.subplots()
    ax.scatter(amostra["idade_mae"], amostra["peso"], alpha=0.4)
    ax.set_title("Idade da mãe x peso ao nascer (amostra de 1.000)")
    ax.set_xlabel("Idade da mãe")
    ax.set_ylabel("Peso (g)")
    salvar_figura(fig, "dispersao_idade_peso.png")