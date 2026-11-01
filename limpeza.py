import pandas as pd

# ---------- Dicionários e conjuntos de configuração ----------
# Chave = nome da coluna no arquivo oficial; valor = nome que vamos usar.
RENOMEAR_SINASC = {
    "DTNASC": "data_nasc",
    "PESO": "peso",
    "IDADEMAE": "idade_mae",
    "CONSULTAS": "consultas_cod",
    "PARTO": "parto_cod",
    "ESCMAE": "escolaridade_cod",
    "GESTACAO": "gestacao_cod",
    "CODMUNRES": "municipio",
}
RENOMEAR_SIM = {
    "DTOBITO": "data_obito",
    "IDADE": "idade_cod",
    "CAUSABAS": "causa",
    "CODMUNRES": "municipio",
}

# Rótulos dos códigos (confira no dicionário de dados da base que você baixou)
ROTULOS_PARTO = {1: "Vaginal", 2: "Cesáreo"}
ROTULOS_CONSULTAS = {1: "Nenhuma", 2: "1 a 3", 3: "4 a 6", 4: "7 ou mais"}
ROTULOS_ESCOLARIDADE = {1: "Nenhuma", 2: "1 a 3 anos", 3: "4 a 7 anos",
                        4: "8 a 11 anos", 5: "12 anos ou mais"}

PREMATURO = {1, 2, 3, 4}          # códigos de gestação com menos de 37 semanas
COLUNAS_CODIFICADAS = ["consultas_cod", "parto_cod", "escolaridade_cod", "gestacao_cod"]
CODIGO_IGNORADO = 9
LIMITE_BAIXO_PESO = 2500          # gramas
FAIXAS_INFANTIS = {"Neonatal precoce", "Neonatal tardio", "Pós-neonatal"}


# ---------- Funções gerais ----------
def selecionar_e_renomear(df, mapa):
    faltando = set(mapa.keys()) - set(df.columns)
    if faltando:
        print("Colunas não encontradas no arquivo:", sorted(faltando))
        print("Ajuste o dicionário de renomeação (confira o dicionário de dados da base).")
        return None
    return df[list(mapa.keys())].rename(columns=mapa)


def converter_data(df, coluna):
    """Converte datas no formato ddmmaaaa e cria as colunas ano e mes."""
    texto = df[coluna].astype(str).str.zfill(8)
    df[coluna] = pd.to_datetime(texto, format="%d%m%Y", errors="coerce")
    df["ano"] = df[coluna].dt.year
    df["mes"] = df[coluna].dt.month
    return df


# ---------- SINASC (nascimentos) ----------
def tratar_ignorados(df):
    """Troca o código 9 (ignorado) por valor vazio (NaN)."""
    for coluna in COLUNAS_CODIFICADAS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        df[coluna] = df[coluna].where(df[coluna] != CODIGO_IGNORADO)
    return df


def remover_invalidos(df):
    antes = len(df)
    df["peso"] = pd.to_numeric(df["peso"], errors="coerce")
    df["idade_mae"] = pd.to_numeric(df["idade_mae"], errors="coerce")
    df = df.dropna(subset=["peso", "idade_mae", "data_nasc"])
    # Limites escolhidos pelo projeto: documente-os no README
    df = df[(df["peso"] >= 500) & (df["peso"] <= 6000)]
    df = df[(df["idade_mae"] >= 10) & (df["idade_mae"] <= 60)]
    print(f"Registros removidos por valores inválidos: {antes - len(df)}")
    return df.copy()


def classificar_peso(peso):
    if peso < LIMITE_BAIXO_PESO:
        return "Baixo peso"
    return "Peso adequado"


def criar_colunas(df):
    df["faixa_peso"] = df["peso"].apply(classificar_peso)
    df["baixo_peso"] = df["peso"] < LIMITE_BAIXO_PESO
    df["prematuro"] = df["gestacao_cod"].isin(PREMATURO)
    df["parto"] = df["parto_cod"].map(ROTULOS_PARTO)
    df["consultas"] = df["consultas_cod"].map(ROTULOS_CONSULTAS)
    df["escolaridade"] = df["escolaridade_cod"].map(ROTULOS_ESCOLARIDADE)
    return df


def limpar_sinasc(df):
    df = selecionar_e_renomear(df, RENOMEAR_SINASC)
    if df is None:
        return None
    df = converter_data(df, "data_nasc")
    df = remover_invalidos(df)
    df = tratar_ignorados(df)
    df = criar_colunas(df)
    return df


# ---------- SIM (óbitos) ----------
def classificar_idade_obito(codigo):
    """IDADE no SIM: 2xx = dias, 3xx = meses, 4xx = anos."""
    if pd.isna(codigo):
        return "Ignorado"
    if codigo < 207:
        return "Neonatal precoce"      # 0 a 6 dias
    if codigo < 228:
        return "Neonatal tardio"       # 7 a 27 dias
    if codigo < 400:
        return "Pós-neonatal"          # 28 dias a 11 meses
    return "Não infantil"


def limpar_sim(df):
    df = selecionar_e_renomear(df, RENOMEAR_SIM)
    if df is None:
        return None
    df = converter_data(df, "data_obito")
    df["idade_cod"] = pd.to_numeric(df["idade_cod"], errors="coerce")
    df["causa"] = df["causa"].astype(str).str.strip().str.upper()
    df["faixa_obito"] = df["idade_cod"].apply(classificar_idade_obito)
    df = df.dropna(subset=["data_obito"])
    df = df[df["faixa_obito"].isin(FAIXAS_INFANTIS)]     # só óbitos de menores de 1 ano
    return df.copy()