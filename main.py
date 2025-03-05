"""
main.py

Descrição:
-----------
Este é o script principal que orquestra a geração de dados sintéticos. Ele integra as funcionalidades dos módulos de
geração e pode operar em dois modos distintos:

1. Modo Original:
   - Gera dados agregados para diversos segmentos, onde cada linha representa um registro de uma empresa (ou operação)
     em um determinado dia.
   - Os registros incluem diversos indicadores financeiros, operacionais, de marketing, satisfação do cliente e uso de
     produtos/serviços, com suporte à autocorrelação e aplicação opcional de outliers.
   - Esse modo é ideal para simulações e análises de KPIs empresariais em geral.

2. Modo Hotel Único:
   - Gera dados detalhados para um único hotel, onde cada linha representa um cliente que se hospedou em um determinado dia.
   - Além dos dados individuais (nome do cliente, tipo de quarto, quantidade de quartos, diárias, valor da diária,
     valor total das diárias, outros consumos e total pago), este modo calcula e acrescenta métricas diárias agregadas
     essenciais para análises de Revenue Management, tais como:
       • Quartos Ocupados no Dia
       • Receita de Quartos do Dia
       • Receita Total do Dia
       • Custo Total do Dia
       • Lucro Operacional Bruto do Dia
       • ADR (Average Daily Rate)
       • RevPAR (Revenue per Available Room)
       • TRevPAR (Total Revenue per Available Room)
       • GOPPAR (Gross Operating Profit per Available Room)
   - Essas métricas diárias são calculadas após gerar os registros de cada dia e inseridas em cada linha,
     permitindo que dashboards possam agrupar os dados por data e exibir os KPIs sem necessidade de cálculos adicionais.

Funcionalidades:
-----------------
1. Configuração de Parâmetros:
   - Permite definir o número de registros, segmentos, intervalo de datas, probabilidade de outliers e o nome do arquivo
     de saída, via argumentos de linha de comando (modo original).
   - Parâmetros específicos para o modo hotel único:
       • --modo_hotel_unico: Habilita o modo de dados detalhados para um único hotel.
       • --nome_hotel: Nome do hotel.
       • --total_quartos: Total de quartos disponíveis no hotel (este valor é configurável e não fixo).
       • --max_clientes_por_dia: Número máximo de clientes que podem chegar por dia.
       
2. Integração com os Módulos de Geração:
   - Importa funções de "geradores.py" para o modo original e de "geradores_hotel.py" para o modo hotel único.
   - Gera os dados de acordo com os parâmetros informados, aplicando, quando apropriado, a autocorrelação e outliers.
   - No modo hotel único, são calculadas as métricas diárias agregadas para Revenue Management e inseridas em cada
     registro do dia.

3. Execução e Salvamento:
   - Processa os argumentos da linha de comando.
   - Seleciona o modo de execução conforme o parâmetro --modo_hotel_unico.
   - Salva o dataset gerado em um arquivo CSV com o cabeçalho apropriado para o modo escolhido.

Uso:
-----
Exemplo para Modo Original:
   python main.py --registros 5000 --segmentos "Aviação" "Finanças" "Metalurgia" "Automobilismo" "Hospital" "Saúde" "TI" \
      --data_inicio 2020-01-01 --data_fim 2024-12-31 --outliers 0.05 --arquivo_saida "dados_segmentados_2020_2024.csv"

Exemplo para Modo Hotel Único:
   python main.py --modo_hotel_unico --data_inicio 2020-01-01 --data_fim 2020-01-31 \
      --nome_hotel "Hotel Luxo" --total_quartos 120 --max_clientes_por_dia 5 --outliers 0.02 \
      --arquivo_saida "hotel_luxo_jan2020.csv"

Observações:
-------------
- O script está preparado para lidar tanto com segmentos pré-definidos (como "Varejo", "Hotelaria", "TI", "Saúde", etc.)
  quanto com segmentos novos. Para segmentos sem tratamento específico, as métricas exclusivas permanecerão com valores
  padrão ou `None`.
- No modo hotel único, os dados diários agregados (ex.: ocupacao_diaria, ADR, RevPAR, TRevPAR, GOPPAR) são calculados
  e adicionados a cada registro do dia, permitindo que dashboards de Revenue Management possam agrupar os dados por data
  sem precisar recalcular os indicadores.
- O código utiliza bibliotecas padrão (argparse, csv, random, datetime, numpy, Faker) para flexibilidade e facilidade na
  configuração.
- Este script serve como ferramenta para a criação de datasets sintéticos, auxiliando em testes, simulações, análises de
  KPIs empresariais e Revenue Management.

Desenvolvido para facilitar a geração de dados realistas e apoiar o desenvolvimento e a validação de sistemas analíticos.
"""

import argparse
from datetime import datetime
import random
from faker import Faker

# Importa as funções para o modo original e para o modo hotel único
from geradores import gerar_data_aleatoria, gerar_dados_empresa, gerar_dados_com_outliers
from geradores_hotel import gerar_dados_hotel_unico
from util import criar_arquivo_csv

def main():
    parser = argparse.ArgumentParser(
        description="Gera dados sintéticos de KPIs empresariais ou dados detalhados para um único hotel."
    )
    # Parâmetros para o modo original:
    parser.add_argument("--registros", type=int, default=2000, help="Número de registros para o modo original.")
    parser.add_argument("--segmentos", nargs="+",
                        default=["Educação", "Hotelaria", "Saúde", "TI", "Varejo", "Serviços", "Finanças", "Indústria", "Banco", "Hospital"],
                        help="Segmentos para o modo original.")
    # Parâmetros comuns (datas, outliers, arquivo de saída)
    parser.add_argument("--data_inicio", type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        default="2020-01-01", help="Data de início (YYYY-MM-DD).")
    parser.add_argument("--data_fim", type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
                        default="2020-12-31", help="Data de fim (YYYY-MM-DD).")
    parser.add_argument("--outliers", type=float, default=0.01, help="Probabilidade de outliers (0.01 = 1%).")
    parser.add_argument("--arquivo_saida", type=str, default="dados.csv", help="Nome do arquivo CSV de saída.")
    
    # Parâmetros específicos para o modo hotel único:
    parser.add_argument("--modo_hotel_unico", action="store_true",
                        help="Habilita o modo de dados detalhados para um único hotel.")
    parser.add_argument("--nome_hotel", type=str, default="Hotel Fictício",
                        help="Nome do hotel (modo hotel único).")
    parser.add_argument("--total_quartos", type=int, default=100,
                        help="Total de quartos do hotel (modo hotel único).")
    parser.add_argument("--max_clientes_por_dia", type=int, default=5,
                        help="Máximo de clientes que podem chegar por dia (modo hotel único).")
    
    args = parser.parse_args()
    fake = Faker("pt_BR")

    if args.modo_hotel_unico:
        # Modo Hotel Único: gera dados detalhados para um único hotel, com as métricas diárias agregadas.
        dados = gerar_dados_hotel_unico(
            fake=fake,
            nome_hotel=args.nome_hotel,
            total_quartos=args.total_quartos,
            data_inicio=args.data_inicio,
            data_fim=args.data_fim,
            max_clientes_por_dia=args.max_clientes_por_dia
        )
        cabecalho = [
            "id_registro", "data", "ano", "mes", "dia",
            "nome_hotel", "total_quartos", "ocupacao_diaria",
            "nome_cliente", "tipo_de_quarto", "forma_de_pagamento",
            "quantidade_quartos", "quantidade_diarias", "valor_diaria",
            "valor_total_diarias", "valor_outros_consumos", "total_pago",
            "despesa_fixa", "despesa_variavel", "despesa_mao_obra_direta",
            "despesa_financeira", "despesa_administrativa",
            "quartos_ocupados_dia", "receita_quartos_dia", "receita_total_dia",
            "custo_total_dia", "lucro_operacional_bruto_dia", "adr_dia",
            "revpar_dia", "trevpar_dia", "goppar_dia"
        ]
        criar_arquivo_csv(args.arquivo_saida, cabecalho, dados)
        print(f"Arquivo '{args.arquivo_saida}' criado no modo hotel único com {len(dados)} registros.")
    else:
        # Modo Original: gera dados agregados para diversos segmentos.
        dados = []
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
        dados_anteriores = None
        for i in range(1, args.registros + 1):
            data_registro = gerar_data_aleatoria(args.data_inicio, args.data_fim)
            segmento = random.choice(args.segmentos)
            linha = gerar_dados_empresa(fake, segmento, data_registro, dados_anteriores)
            gerar_dados_com_outliers(linha, args.outliers)
            dados.append([i] + linha)
            dados_anteriores = linha

        dados.sort(key=lambda x: x[1])
        criar_arquivo_csv(args.arquivo_saida, cabecalho, dados)
        print(f"Arquivo '{args.arquivo_saida}' criado no modo original com {args.registros} registros.")

if __name__ == "__main__":
    main()
