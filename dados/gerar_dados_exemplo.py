"""
Gera dados FICTÍCIOS no mesmo formato do SINASC e do SIM.
Serve apenas para testar o projeto antes de usar os dados reais.
Os resultados desses dados NÃO representam a realidade.
"""
import numpy as np
import pandas as pd
from pathlib import Path

PASTA_BRUTOS = Path("dados/brutos")
MUNICIPIOS = [350010, 350020, 350030, 350040, 350050]  # códigos fictícios


def gerar_datas(n, inicio="2021-01-01", dias=1095):
    """Sorteia n datas e devolve no formato ddmmaaaa (como vem do DATASUS)."""
    deslocamento = pd.to_timedelta(np.random.randint(0, dias, n), unit="D")
    datas = pd.to_datetime(inicio) + deslocamento
    return datas.strftime("%d%m%Y")


def gerar_sinasc(n=20000):
    consultas = np.random.choice([1, 2, 3, 4, 9], n, p=[0.03, 0.12, 0.30, 0.54, 0.01])
    # efeito fictício: mais consultas de pré-natal, peso um pouco maior
    base = 3000 + (consultas == 4) * 120 - (consultas == 1) * 250
    peso = np.random.normal(base, 480).round()

    return pd.DataFrame({
        "DTNASC": gerar_datas(n),
        "PESO": np.clip(peso, 700, 5200).astype(int),
        "IDADEMAE": np.clip(np.random.normal(27, 6, n).round(), 12, 48).astype(int),
        "CONSULTAS": consultas,
        "PARTO": np.random.choice([1, 2, 9], n, p=[0.41, 0.58, 0.01]),
        "ESCMAE": np.random.choice([1, 2, 3, 4, 5, 9], n,
                                   p=[0.01, 0.05, 0.20, 0.50, 0.22, 0.02]),
        "GESTACAO": np.random.choice([1, 2, 3, 4, 5, 6, 9], n,
                                     p=[0.002, 0.008, 0.02, 0.09, 0.86, 0.01, 0.01]),
        "CODMUNRES": np.random.choice(MUNICIPIOS, n),
    })


def gerar_sim(n_infantis=220, n_adultos=300):
    # IDADE no padrão do SIM: 2xx = dias, 3xx = meses, 4xx = anos
    tipos = np.random.choice(["precoce", "tardio", "pos"], n_infantis, p=[0.50, 0.17, 0.33])
    idades = []
    for tipo in tipos:
        if tipo == "precoce":
            idades.append(200 + np.random.randint(0, 7))     # 0 a 6 dias
        elif tipo == "tardio":
            idades.append(200 + np.random.randint(7, 28))    # 7 a 27 dias
        else:
            idades.append(300 + np.random.randint(1, 12))    # 1 a 11 meses
    idades = idades + list(np.random.randint(420, 490, n_adultos))  # adultos (anos)

    causas_infantis = ["P07", "P22", "P36", "Q24", "J18", "A41"]
    causas_adultos = ["I21", "C34", "J44", "E11"]
    causas = (list(np.random.choice(causas_infantis, n_infantis))
              + list(np.random.choice(causas_adultos, n_adultos)))

    n = n_infantis + n_adultos
    df = pd.DataFrame({
        "DTOBITO": gerar_datas(n),
        "IDADE": idades,
        "CAUSABAS": causas,
        "CODMUNRES": np.random.choice(MUNICIPIOS, n),
    })
    return df.sample(frac=1, random_state=1).reset_index(drop=True)


def salvar(df, nome):
    PASTA_BRUTOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_BRUTOS / nome
    df.to_csv(caminho, sep=";", index=False, encoding="utf-8")
    print("Arquivo criado:", caminho)


np.random.seed(42)
salvar(gerar_sinasc(), "sinasc_exemplo.csv")
salvar(gerar_sim(), "sim_exemplo.csv")