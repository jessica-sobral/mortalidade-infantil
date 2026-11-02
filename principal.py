from pathlib import Path

import analise
import coleta
import graficos
import limpeza

# ---------- Configuração do projeto (trocar pelos nomes dos arquivos reais) --------
ARQUIVO_SINASC = "sinasc_exemplo.csv"
ARQUIVO_SIM = "sim_exemplo.csv"
SEPARADOR = ";"     # use "," se o CSV for separado por vírgula
CODIGO_UF = None    # None = sem filtro; "35" = só São Paulo (2 primeiros dígitos do município)
PASTA_TRATADOS = Path("dados/tratados")
PASTA_RESULTADOS = Path("resultados")

dados = {"sinasc": None, "sim": None}   # guarda os dados já limpos


def dados_carregados():
    if dados["sinasc"] is None or dados["sim"] is None:
        print("Carregue os dados primeiro (opção 1).")
        return False
    return True


def carregar_dados():
    bruto_sinasc = coleta.carregar_csv(ARQUIVO_SINASC, {"DTNASC": str},
                                       list(limpeza.RENOMEAR_SINASC.keys()), SEPARADOR)
    bruto_sim = coleta.carregar_csv(ARQUIVO_SIM, {"DTOBITO": str},
                                    list(limpeza.RENOMEAR_SIM.keys()), SEPARADOR)
    if bruto_sinasc is None or bruto_sim is None:
        return
    bruto_sinasc = coleta.filtrar_uf(bruto_sinasc, "CODMUNRES", CODIGO_UF)
    bruto_sim = coleta.filtrar_uf(bruto_sim, "CODMUNRES", CODIGO_UF)
    if len(bruto_sinasc) == 0 or len(bruto_sim) == 0:
        print("Nenhum registro encontrado. Confira o CODIGO_UF e os arquivos.")
        return
    dados["sinasc"] = limpeza.limpar_sinasc(bruto_sinasc)
    dados["sim"] = limpeza.limpar_sim(bruto_sim)
    if dados_carregados():
        print(f"Nascidos vivos após limpeza: {len(dados['sinasc'])}")
        print(f"Óbitos infantis após limpeza: {len(dados['sim'])}")


def mostrar_perfil_nascimentos():
    if not dados_carregados():
        return
    sinasc = dados["sinasc"]
    est = analise.estatisticas_peso(sinasc)
    print("\n--- Peso ao nascer (g) ---")
    print(f"Média: {est['media']:.0f} | Mediana: {est['mediana']:.0f} | "
          f"Desvio: {est['desvio']:.0f} | Mín: {est['minimo']} | Máx: {est['maximo']}")
    print(f"Baixo peso (< 2.500 g): {analise.percentual_baixo_peso(sinasc):.1f}%")
    print(f"Prematuros (< 37 semanas): {analise.percentual_prematuro(sinasc):.1f}%")
    print("\n--- Tipo de parto (%) ---")
    print(analise.distribuicao_percentual(sinasc, "parto").to_string())
    print("\n--- Escolaridade da mãe (%) ---")
    print(analise.distribuicao_percentual(sinasc, "escolaridade").to_string())
    print("\n--- Peso médio (g) por consultas de pré-natal ---")
    print(analise.peso_medio_por_consultas(sinasc).to_string())


def mostrar_mortalidade():
    if not dados_carregados():
        return
    sinasc, sim = dados["sinasc"], dados["sim"]
    taxa = analise.taxa_mortalidade_infantil(len(sim), len(sinasc))
    print(f"\nTaxa de mortalidade infantil geral: {taxa:.2f} por 1.000 nascidos vivos")
    print("\n--- Taxa por ano ---")
    print(analise.tabela_taxa(sinasc, sim, "ano"))
    print("\n--- Taxa por município ---")
    print(analise.tabela_taxa(sinasc, sim, "municipio"))
    print("\n--- Óbitos por faixa de idade ---")
    print(analise.contar_por_faixa_obito(sim))
    print("\n--- Principais causas (categoria CID-10) ---")
    print(analise.principais_causas(sim))


def gerar_graficos():
    if not dados_carregados():
        return
    sinasc, sim = dados["sinasc"], dados["sim"]
    graficos.histograma_peso(sinasc)
    graficos.barras(analise.distribuicao_percentual(sinasc, "parto"),
                    "Nascimentos por tipo de parto", "%", "barras_parto.png")
    graficos.barras(analise.distribuicao_percentual(sinasc, "escolaridade"),
                    "Escolaridade da mãe", "%", "barras_escolaridade.png")
    graficos.barras(analise.peso_medio_por_consultas(sinasc),
                    "Peso médio por consultas de pré-natal", "Peso médio (g)",
                    "peso_por_consultas.png")
    graficos.linha(analise.nascimentos_por_ano(sinasc),
                   "Nascimentos por ano", "Nascimentos", "linha_nascimentos.png")
    graficos.linha(analise.tabela_taxa(sinasc, sim, "ano")["taxa_por_mil"],
                   "Taxa de mortalidade infantil por ano",
                   "Óbitos por 1.000 nascidos vivos",
                   "linha_taxa_mortalidade.png")
    graficos.barras(analise.contar_por_faixa_obito(sim),
                    "Óbitos infantis por faixa de idade", "Óbitos",
                    "barras_faixa_obito.png")
    graficos.dispersao_idade_peso(sinasc)


def salvar_relatorio():
    if not dados_carregados():
        return
    sinasc, sim = dados["sinasc"], dados["sim"]
    PASTA_TRATADOS.mkdir(parents=True, exist_ok=True)
    PASTA_RESULTADOS.mkdir(exist_ok=True)
    sinasc.to_csv(PASTA_TRATADOS / "sinasc_tratado.csv", sep=";", index=False, encoding="utf-8")
    sim.to_csv(PASTA_TRATADOS / "sim_tratado.csv", sep=";", index=False, encoding="utf-8")
    taxa = analise.taxa_mortalidade_infantil(len(sim), len(sinasc))
    est = analise.estatisticas_peso(sinasc)
    linhas = [
        "RELATÓRIO - MORTALIDADE INFANTIL E PERFIL DOS NASCIMENTOS", "",
        f"Nascidos vivos analisados: {len(sinasc)}",
        f"Óbitos infantis analisados: {len(sim)}",
        f"Taxa de mortalidade infantil: {taxa:.2f} por 1.000 nascidos vivos",
        f"Peso médio ao nascer: {est['media']:.0f} g",
        f"Baixo peso: {analise.percentual_baixo_peso(sinasc):.1f}%",
        f"Prematuros: {analise.percentual_prematuro(sinasc):.1f}%",
        "",
        "Taxa por ano:",
        analise.tabela_taxa(sinasc, sim, "ano").to_string(),
        "",
        "Taxa por município:",
        analise.tabela_taxa(sinasc, sim, "municipio").to_string(),
        "",
        "ATENÇÃO: confira se os dados são reais ou de exemplo antes de concluir algo.",
    ]
    caminho = PASTA_RESULTADOS / "relatorio.txt"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas))
    print("Relatório salvo em:", caminho)
    print("Tabelas tratadas salvas em:", PASTA_TRATADOS)


def menu():
    while True:
        print("\n===== MORTALIDADE INFANTIL E PERFIL DOS NASCIMENTOS =====")
        print("1 - Carregar e limpar dados")
        print("2 - Perfil dos nascimentos")
        print("3 - Mortalidade infantil")
        print("4 - Gerar gráficos")
        print("5 - Salvar relatório e tabelas tratadas")
        print("0 - Sair")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            carregar_dados()
        elif opcao == "2":
            mostrar_perfil_nascimentos()
        elif opcao == "3":
            mostrar_mortalidade()
        elif opcao == "4":
            gerar_graficos()
        elif opcao == "5":
            salvar_relatorio()
        elif opcao == "0":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


menu()