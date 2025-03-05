# util.py

"""
util.py

Descrição:
-----------
Este módulo contém funções utilitárias que facilitam a manipulação, criação e exportação de arquivos CSV 
para os datasets gerados pelo sistema. A principal função deste módulo é garantir que os dados sintéticos, 
sejam eles provenientes do modo original (dados agregados para diversos segmentos) ou do modo hotel único 
(dados detalhados para um único hotel com métricas diárias para Revenue Management), sejam salvos de forma 
estruturada, consistente e compatível com diversas ferramentas de análise e Business Intelligence.

Funcionalidades:
-----------------
- criar_arquivo_csv(nome_arquivo, cabecalho, dados):
  - **Descrição:** Recebe o nome do arquivo de destino, uma lista de cabeçalhos (nomes das colunas) e os dados 
    (geralmente uma lista de listas, onde cada sublista representa uma linha do dataset) e cria um arquivo CSV 
    com estes dados.
  - **Detalhes Técnicos:**
    - Abre o arquivo em modo de escrita ("w") com codificação UTF-8.
    - Utiliza o parâmetro `newline=""` para garantir a correta formatação das quebras de linha, o que é 
      importante para a compatibilidade do CSV em diferentes sistemas operacionais.
    - Se o arquivo já existir, ele será sobrescrito.

Uso:
-----
Este módulo pode ser importado por outros scripts, como o "main.py", para salvar os datasets gerados 
dinamicamente. A função `criar_arquivo_csv` é essencial para a exportação dos dados, permitindo uma integração 
fácil com ferramentas de análise, dashboards e outros sistemas.

Observações:
-------------
- Utiliza a biblioteca padrão `csv` do Python para a escrita dos arquivos CSV.
- Foi desenvolvido para suportar a geração e exportação de datasets sintéticos, tanto para dados agregados 
  de múltiplos segmentos quanto para dados detalhados de um único hotel, facilitando a análise de KPIs e 
  Revenue Management.
- Este módulo ajuda a manter a consistência e a integridade dos dados exportados, simplificando o fluxo de 
  trabalho em projetos de Business Intelligence e Data Analytics.

Desenvolvido para facilitar a criação, exportação e integração de datasets sintéticos com diversas ferramentas 
de análise.
"""

import csv

def criar_arquivo_csv(nome_arquivo, cabecalho, dados):
    """
    Cria um arquivo CSV com os dados fornecidos.
    - nome_arquivo: nome (ou caminho) do arquivo CSV.
    - cabecalho: lista com os nomes das colunas.
    - dados: lista de listas, onde cada sublista representa uma linha.
    """
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(cabecalho)
        writer.writerows(dados)