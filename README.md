# Mortalidade infantil e perfil dos nascimentos

Projeto da disciplina SI204 - Algoritmos e Programação de Computadores II.
Análise de dados públicos de saúde sobre nascimentos (SINASC) e óbitos infantis (SIM).

## Perguntas que o projeto procura responder
1.	Qual o perfil dos nascimentos (idade da mãe, escolaridade, tipo de parto, pré-natal)? 
2.	Qual a proporção de baixo peso e de prematuridade?
3.	Como o pré-natal se relaciona com o peso ao nascer?
4.	Qual o perfil e as principais causas dos óbitos infantis?
5.	Como a taxa de mortalidade infantil varia entre anos e municípios?

## Fontes dos dados (completar após etapas 9 e 10)
- SINASC e SIM: [OpenDataSUS / TabNet - cole o endereço da página]
- Data do download: [dd/mm/aaaa]
- Recorte: [estado e ano(s)]

## Como executar
1.	Crie e ative o ambiente virtual: python -m venv .venv e .venv\Scripts\activate
2.	Instale as dependências: pip install -r requirements.txt
3.	Crie as pastas dados/brutos e dados/tratados e coloque os CSVs em dados/brutos/ (ou rode python gerar_dados_exemplo.py para usar dados fictícios de teste)
4.	Ajuste os nomes dos arquivos no início de principal.py
5.	Rode: python principal.py

## Estrutura
`coleta.py` (leitura), `limpeza.py` (tratamento), `analise.py` (indicadores), `graficos.py` (gráficos), `principal.py` (menu).

## Decisões de limpeza
- Código 9 ("ignorado") tratado como valor vazio.
- Peso fora de 500 a 6.000 g e idade da mãe fora de 10 a 60 anos foram removidos.
- Óbitos infantis = menores de 1 ano (IDADE < 400 no SIM).
- Taxa de mortalidade infantil = óbitos de menores de 1 ano / nascidos vivos x 1.000.

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
- Divisão de tarefas entre os integrantes, organização do repositório Git e commits individuais;