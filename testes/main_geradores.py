# main.py

"""
main.py

Descrição:
-----------
Este é o script principal responsável por orquestrar a geração de dados sintéticos de empresas, integrando
as funcionalidades do módulo "geradores.py". O objetivo é criar um dataset realista com diversos indicadores
financeiros, operacionais, de marketing, satisfação do cliente e uso de produtos/serviços, com base em parâmetros
definidos pelo usuário.

Funcionalidades:
-----------------
1. Configuração de Parâmetros:
   - Permite definir o número de registros a serem gerados (por meio do argumento --registros).
   - Permite especificar os segmentos de mercado para os quais os dados serão criados (via --segmentos).
   - Permite definir o período de geração dos dados utilizando os argumentos --data_inicio e --data_fim.
   - Possibilita a configuração da probabilidade de aplicação de outliers (via --outliers).
   - Permite definir o nome do arquivo de saída (por exemplo, CSV) para armazenar os dados gerados (via --arquivo_saida).

2. Integração com o Módulo "geradores.py":
   - Importa as funções de geração de dados do módulo "geradores.py".
   - Gera os dados iniciais e, quando apropriado, aplica a autocorrelação com base em registros anteriores,
     simulando a evolução dos indicadores ao longo do tempo.
   - Aplica outliers em determinados campos, conforme a probabilidade configurada, para simular variações
     extremas e anomalias.

3. Execução e Salvamento:
   - Processa os argumentos da linha de comando para configurar todos os parâmetros de geração.
   - Executa a geração dos registros conforme os parâmetros informados.
   - Salva o dataset gerado em um arquivo (por exemplo, CSV) com o nome especificado, facilitando a posterior
     análise ou integração com outros sistemas.

Uso:
-----
Exemplo de execução:
    python main.py --registros 5000 --segmentos "Aviação" "Finanças" "Metalurgia" "Automobilismo" "Hospital" "Saúde" "TI" \
                   --data_inicio 2020-01-01 --data_fim 2024-12-31 --outliers 0.05 --arquivo_saida "dados_segmentados_2020_2024.csv"

Observações:
-------------
- O script está preparado para lidar tanto com segmentos pré-definidos (como "Varejo", "Hotelaria", "TI", "Saúde", etc.)
  quanto com segmentos novos (como "Finanças", "Aviação", "Metalurgia" e "Automobilismo"). Para os segmentos não
  tratados especificamente, as métricas exclusivas ficarão com valores padrão ou `None`.
- O código utiliza bibliotecas padrão (como argparse) para o processamento dos argumentos da linha de comando,
  garantindo flexibilidade e facilidade na configuração.
- Este script serve como uma ferramenta para a criação de datasets sintéticos, auxiliando em testes, simulações
  e análises em projetos de Business Intelligence e Data Analytics.

Desenvolvido para facilitar a geração de dados realistas e apoiar o desenvolvimento e a validação de sistemas
analíticos.
"""

import argparse
from datetime import datetime
from faker import Faker
import numpy as np
import random
from geradores import gerar_data_aleatoria, gerar_dados_empresa, gerar_dados_com_outliers
from util import criar_arquivo_csv

import geradores
print(geradores.__file__)

import util #Adiciona o import
print(util.__file__) #Imprime o caminho.

import sys  #Adicionado
print(sys.path) #Adicionado

def main():
    parser = argparse.ArgumentParser(description="Gera dados fictícios de KPIs empresariais.")
    parser.add_argument("--registros", type=int, default=2000, help="Número de registros (mínimo 2000).")
    parser.add_argument("--segmentos", nargs="+", default=["Educação", "Hotelaria", "Saúde", "TI", "Varejo", "Serviços", "Finanças", "Indústria", "Banco", "Hospital"], help="Segmentos.") #Adicionei mais alguns
    parser.add_argument("--data_inicio", type=lambda s: datetime.strptime(s, '%Y-%m-%d'), default=datetime(2020, 1, 1), help="Data de início (YYYY-MM-DD).")
    parser.add_argument("--data_fim", type=lambda s: datetime.strptime(s, '%Y-%m-%d'), default=datetime.now(), help="Data de fim (YYYY-MM-DD).")
    parser.add_argument("--outliers", type=float, default=0.01, help="Probabilidade de outliers (0.01 = 1%).")
    parser.add_argument("--arquivo_saida", type=str, default="dados_kpis.csv", help="Nome do arquivo CSV de saída.")

    args = parser.parse_args()

    fake = Faker("pt_BR")

    # Cabeçalho ENORME agora!
    cabecalho = [
        "registro_id", "data", "ano", "mes", "dia", "segmento", "empresa", "cidade",
        "numero_clientes", "ticket_medio", "receita", "custo", "lucro",
        "indice_satisfacao", "taxa_ocupacao", "taxa_crescimento",
        "custo_marketing", "investimento_publicidade",
        "previsao_vendas", "previsao_custos",
        "sensibilidade_negocios", "indice_correcao", "programacao_linear",
        "regiao", "estado", "pais", "tipo_cliente", "canal_venda",
        "categoria_produto", "tipo_servico", "plano", "faixa_etaria",
        "genero", "fonte_trafego", "dispositivo", "sistema_operacional",
        "navegador", "quantidade_produtos", "custo_por_cliente",
        "receita_por_cliente", "lucro_por_cliente", "desconto_medio",
        "percentual_desconto", "taxa_conversao", "vendas_por_vendedor",
        "comissao_vendas", "valor_impostos", "frete_medio",
        "pedidos_por_cliente", "LTV", "CAC", "MRR", "ARR",
        "receita_media_diaria", "custo_por_clique", "custo_por_mil_impressoes",
        "taxa_de_clique", "impressoes", "cliques", "leads_gerados",
        "custo_por_lead", "ROAS", "avaliacao_media", "numero_avaliacoes",
        "NPS", "CSAT", "reclamacoes", "tempo_medio_resposta",
        "tempo_medio_entrega", "taxa_devolucao", "nivel_estoque",
        "giro_estoque", "custo_estoque", "numero_fornecedores",
        "taxa_de_defeito", "usuarios_ativos", "tempo_medio_sessao",
        "taxa_retencao", "churn_rate", "funcionalidade_mais_usada",
        "numero_sessoes", "RevPAR", "taxa_evasao",
        "tempo_medio_atendimento", "despesa_administrativa",
        "despesa_com_pessoal", "despesa_fixa", "despesa_variavel",
        "despesa_tributaria", "despesa_financeira"
    ]

    dados = []
    dados_anteriores = None
    for i in range(1, args.registros + 1):
        data_registro = gerar_data_aleatoria(args.data_inicio, args.data_fim)
        segmento = random.choice(args.segmentos)
        dados_empresa = gerar_dados_empresa(fake, segmento, data_registro, dados_anteriores)
        gerar_dados_com_outliers(dados_empresa, args.outliers) # Modificada
        dados.append([i] + dados_empresa)
        dados_anteriores = dados_empresa

    dados.sort(key=lambda x: x[1])

    criar_arquivo_csv(args.arquivo_saida, cabecalho, dados)
    print(f"Arquivo '{args.arquivo_saida}' criado com {args.registros} registros.")

if __name__ == "__main__":
    main()