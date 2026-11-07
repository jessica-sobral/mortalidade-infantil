# Mortalidade infantil e perfil dos nascimentos

Projeto da disciplina SI204 - Algoritmos e Programação de Computadores II.
Análise de dados públicos de saúde sobre nascimentos (SINASC) e óbitos infantis (SIM).

## Perguntas que o projeto procura responder
1.	Qual o perfil dos nascimentos (idade da mãe, escolaridade, tipo de parto, pré-natal)? 
2.	Qual a proporção de baixo peso e de prematuridade?
3.	Como o pré-natal se relaciona com o peso ao nascer?
4.	Qual o perfil e as principais causas dos óbitos infantis?
5.	Como a taxa de mortalidade infantil varia entre anos e municípios?

## Fontes dos dados
- SINASC (nascidos vivos): https://dadosabertos.saude.gov.br/dataset/sistema-de-informacao-sobre-nascidos-vivos-sinasc
- SIM (mortalidade): https://dadosabertos.saude.gov.br/dataset/sim
- Arquivos usados: SINASC_2024.csv e Mortalidade_Geral_2024.csv
- Data do download: 07/11/2026
- Recorte: Estado de São Paulo, 2024, por residência
- Validação: TabNet/DATASUS (https://datasus.saude.gov.br/informacoes-de-saude-tabnet/), em Estatísticas Vitais, Nascidos Vivos e Mortalidade, estado de São Paulo, 2024, por residência.

## Como executar
1.	Crie e ative o ambiente virtual: python -m venv .venv e .venv\Scripts\activate
2.	Instale as dependências: pip install -r requirements.txt
3. Baixe os CSVs do SINASC e do SIM (SP, 2024) nos links de "Fontes dos dados" e coloque em dados/brutos/ (ou rode python gerar_dados_exemplo.py para usar dados fictícios de teste)
4. Confira no início de principal.py: ARQUIVO_SINASC = "SINASC_2024.csv", ARQUIVO_SIM = "Mortalidade_Geral_2024.csv", SEPARADOR = ";" e CODIGO_UF = "35"
5.	Rode: python principal.py

## Estrutura
`coleta.py` (leitura), `limpeza.py` (tratamento), `analise.py` (indicadores), `graficos.py` (gráficos), `principal.py` (menu).

## Decisões de limpeza
- Código 9 ("ignorado") tratado como valor vazio.
- Peso fora de 500 a 6.000 g e idade da mãe fora de 10 a 60 anos foram removidos.
- Óbitos infantis = menores de 1 ano (IDADE < 400 no SIM).
- Taxa de mortalidade infantil = óbitos de menores de 1 ano / nascidos vivos x 1.000.
- 664 registros do SINASC foram removidos pelos limites de peso e idade da mãe (cerca de 0,14%). Por isso o programa tem 470.223 nascidos vivos contra 470.887 no TabNet.
- No SIM, o programa tem 5.283 óbitos de menores de 1 ano contra 5.311 no TabNet (diferença de 28, cerca de 0,5%).
- O arquivo do SIM de SP não tem óbitos fetais (TIPOBITO = 1): todos os registros são do tipo 2.

## Limitações
- Os dados podem apresentar atrasos de registro, principalmente nos anos mais recentes.
- Municípios com poucos nascimentos podem apresentar taxas de mortalidade infantil instáveis.
- Pode existir subnotificação de nascimentos e óbitos nas bases utilizadas.

## Uso de IA
Foi utilizada a ferramenta de IA Claude (Anthropic) como apoio ao estudo e ao desenvolvimento do projeto, conforme permitido pelas regras da disciplina.

**Como a IA foi usada:**
- Esclarecimento de dúvidas acerca de conceitos de Python.
- Acompanhamento dos testes, conferindo se as saídas batiam com o esperado para os dados de exemplo.
- Identificação de possíveis erros no código.
- Sugestão de melhorias na organização e estrutura do projeto.

**O que foi feito pela equipe:**
- Criação e revisão dos códigos, executados e testados por nós, e os resultados foram conferidos na nossa máquina.
- As sugestões de melhoria fornecidas pela IA foram analisadas e adaptadas pela equipe de acordo com as necessidades do projeto.
- As decisões de limpeza e a interpretação dos resultados são de responsabilidade do grupo.
- Divisão de tarefas entre os integrantes, organização do repositório Git e commits individuais.