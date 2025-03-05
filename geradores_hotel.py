# geradores_hotel.py

"""
geradores_hotel.py
Autor: Izairton Oliveira de Vasconcelos
Ponta Grossa - Paraná - Brasil

Descrição:
-----------
Este módulo foi desenvolvido para gerar dados fictícios e realistas para um único hotel, 
simulando tanto informações detalhadas de cada cliente quanto métricas diárias agregadas 
essenciais para análises de Revenue Management. Cada linha gerada representa um cliente que 
se hospedou em um determinado dia, e os dados diários são calculados e inseridos em cada registro, 
permitindo que dashboards possam agrupar e analisar os principais indicadores do hotel sem a necessidade 
de realizar cálculos adicionais.

Funcionalidades Principais:
-----------------------------
1. Geração de Datas:
   - Função `gerar_data_aleatoria`: Gera uma data aleatória entre duas datas fornecidas (início e fim).
   - Função `gerar_datas_periodo` (se utilizada internamente): Gera uma lista de todas as datas entre a data de 
     início e a data de fim.

2. Funções Auxiliares:
   - Função `_safe_randint`: Garante que os limites para `random.randint` sejam convertidos para inteiros, 
     invertendo-os se necessário, para evitar erros de tipo.
   - Função `gerar_dados_com_outliers`: Aplica outliers em certas colunas numéricas com uma probabilidade definida, 
     simulando variações extremas nos dados.

3. Geração de Dados para o Hotel (Modo Hotel Único):
   - Função `gerar_dados_hotel_unico`: 
       * Para cada dia do período especificado, gera registros individuais para cada cliente que se hospeda.
       * Cada registro contém informações individuais, tais como:
           - **id_registro**: Identificador sequencial único.
           - **data**, **ano**, **mes**, **dia**: Data do registro.
           - **nome_hotel**: Nome do hotel (valor fixo para o dataset).
           - **total_quartos**: Número total de quartos disponíveis no hotel (valor configurável).
           - **ocupacao_diaria**: Percentual de quartos ocupados no dia, calculado com base na soma dos quartos alugados.
           - **nome_cliente**, **tipo_de_quarto**, **forma_de_pagamento**: Informações do hóspede e da reserva.
           - **quantidade_quartos**, **quantidade_diarias**, **valor_diaria**: Dados da reserva do cliente.
           - **valor_total_diarias**, **valor_outros_consumos**, **total_pago**: Valores financeiros individuais do cliente.
           - **despesa_fixa**, **despesa_variavel**, **despesa_mao_obra_direta**, **despesa_financeira**, **despesa_administrativa**:
             Despesas diárias do hotel, que são geradas uma vez por dia e replicadas para cada registro daquele dia.
       * Após gerar os registros de cada dia, a função calcula métricas diárias agregadas para o hotel:
           - **quartos_ocupados_dia**: Total de quartos alugados no dia.
           - **receita_quartos_dia**: Soma dos valores totais das diárias dos clientes (receita de quartos).
           - **receita_total_dia**: Soma dos valores totais pagos pelos clientes (diárias + outros consumos).
           - **custo_total_dia**: Soma das despesas diárias (fixas, variáveis, mão de obra, financeiras, administrativas).
           - **lucro_operacional_bruto_dia**: Diferença entre receita_total_dia e custo_total_dia.
           - **adr_dia**: Average Daily Rate – receita_quartos_dia dividida por quartos_ocupados_dia.
           - **revpar_dia**: Revenue per Available Room – receita_quartos_dia dividida pelo total de quartos.
           - **trevpar_dia**: Total Revenue per Available Room – receita_total_dia dividida pelo total de quartos.
           - **goppar_dia**: Gross Operating Profit per Available Room – lucro_operacional_bruto_dia dividido pelo total de quartos.
       * As métricas diárias (índices 22 a 30) são adicionadas a cada registro do dia, permitindo análises imediatas em dashboards.

Uso:
-----
- Este módulo é utilizado pelo script principal (main.py) quando o parâmetro `--modo_hotel_unico` é especificado.
- O usuário pode configurar:
   • `nome_hotel`: Nome do hotel.
   • `total_quartos`: Número total de quartos (por exemplo, 100, 150, etc.).
   • `data_inicio` e `data_fim`: Período para o qual os dados serão gerados.
   • `max_clientes_por_dia`: Número máximo de clientes que podem se hospedar em cada dia.
- O CSV gerado conterá todas as informações detalhadas por cliente, juntamente com as métricas diárias agregadas
  que são fundamentais para análises de Revenue Management.

Observações:
-------------
- As bibliotecas **Faker** e **numpy** são utilizadas para gerar dados realistas e aplicar distribuições estatísticas.
- O código é modular e pode ser facilmente extendido para incluir novas métricas ou ajustar os ranges de valores.
- Este módulo foi projetado para suportar simulações de Revenue Management e ajudar na criação de dashboards e
  análises de performance do hotel.

Desenvolvido para facilitar a criação de datasets sintéticos e apoiar a validação e performance de sistemas analíticos,
especialmente para análises de Revenue Management no setor hoteleiro.
"""

import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

def gerar_data_aleatoria(inicio, fim):
    """
    Gera uma data aleatória entre 'inicio' e 'fim'.
    """
    delta = fim - inicio
    dias_delta = delta.days
    return inicio + timedelta(days=random.randint(0, dias_delta))

def _safe_randint(a, b):
    """
    Versão segura de random.randint, que converte a e b para int
    e inverte se a > b, evitando erro de tipo quando são floats.
    """
    a = int(a)
    b = int(b)
    if a > b:
        a, b = b, a
    return random.randint(a, b)

def gerar_dados_com_outliers(dados, probabilidade_outlier=0.01):
    """
    Aplica outliers em certas colunas numéricas, com determinada probabilidade.
    Ajuste a lista 'indices_numericos' conforme as colunas que deseja afetar.
    Este método é geralmente aplicado no modo original.
    """
    if random.random() < probabilidade_outlier:
        indices_numericos = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
        indice_outlier = random.choice(indices_numericos)
        fator_outlier = np.random.uniform(0.5, 2.0)
        if isinstance(dados[indice_outlier], (int, float)):
            valor_modificado = dados[indice_outlier] * fator_outlier
            dados[indice_outlier] = round(valor_modificado, 2)
            if indice_outlier in [7, 8, 9, 10, 11, 12]:
                dados[indice_outlier] = max(1, dados[indice_outlier])
    return dados

# -------------------------------------------------------------
# MODO 1 (ORIGINAL): Gera dados agregados por empresa/segmento
# -------------------------------------------------------------

def _gerar_dados_gerais(fake, segmento):
    """
    Gera dados gerais (região, estado, etc.) usados no Modo 1.
    """
    regiao = fake.estado_nome()
    estado = fake.estado_sigla()
    pais = "Brasil"
    tipo_cliente = random.choice(["B2B", "B2C", "Pessoa Física", "Pessoa Jurídica"])
    canal_venda = random.choice(["Loja física", "Online", "Aplicativo", "Telefone", "Representante"])

    if segmento in ["Varejo", "Indústria"]:
        categoria_produto = random.choice(["Eletrônicos", "Roupas", "Alimentos", "Livros", "Móveis", "Outros"])
    else:
        categoria_produto = None

    if segmento in ["Serviços", "TI", "Consultoria", "Saúde", "Educação", "Banco", "Hospital"]:
        tipo_servico = random.choice(["Consultoria", "Suporte", "Treinamento", "Desenvolvimento", "Outros"])
    else:
        tipo_servico = None

    if segmento in ["TI", "Serviços", "SaaS"]:
        plano = random.choice(["Básico", "Premium", "Gratuito", "Teste"])
    else:
        plano = None

    faixa_etaria = random.choice(["18-25", "26-35", "36-45", "46-55", "55+"])
    genero = random.choice(["Masculino", "Feminino", "Outro"])
    fonte_trafego = random.choice(["Busca orgânica", "Anúncio pago", "Rede social", "Email", "Referência", "Direto"])
    dispositivo = random.choice(["Desktop", "Mobile", "Tablet"])
    sistema_operacional = random.choice(["Windows", "macOS", "Linux", "Android", "iOS"])
    navegador = random.choice(["Chrome", "Firefox", "Safari", "Edge", "Outro"])

    return (
        regiao, estado, pais, tipo_cliente, canal_venda,
        categoria_produto, tipo_servico, plano, faixa_etaria,
        genero, fonte_trafego, dispositivo, sistema_operacional, navegador
    )

def gerar_dados_empresa(fake, segmento, data_registro, dados_anteriores=None):
    """
    Gera dados fictícios para o Modo 1 (dados agregados por empresa/segmento).
    Este método retorna uma lista de valores que representam um registro agregado.
    (Código resumido; mantenha o seu código atual para o modo original.)
    """
    (regiao, estado, pais, tipo_cliente, canal_venda,
     categoria_produto, tipo_servico, plano, faixa_etaria,
     genero, fonte_trafego, dispositivo, sistema_operacional,
     navegador) = _gerar_dados_gerais(fake, segmento)

    if dados_anteriores is None:
        numero_clientes = random.randint(10, 300)
        ticket_medio = round(random.uniform(20, 200), 2)
        receita = round(numero_clientes * ticket_medio, 2)
        custo = round(receita * random.uniform(0.6, 0.95), 2)
        lucro = round(receita - custo, 2)
        indice_satisfacao = round(random.uniform(1, 10), 2)
        taxa_ocupacao = round(random.uniform(40, 100), 2) if segmento == "Hotelaria" else None
        taxa_crescimento = round(random.uniform(-10, 30), 2)
        custo_marketing = round(receita * random.uniform(0.05, 0.2), 2)
    else:
        numero_clientes = max(1, int(dados_anteriores[7] * random.uniform(0.9, 1.1)))
        ticket_medio = round(dados_anteriores[8] * random.uniform(0.95, 1.05), 2)
        receita = round(numero_clientes * ticket_medio, 2)
        custo = round(receita * random.uniform(0.6, 0.95), 2)
        lucro = round(receita - custo, 2)
        indice_satisfacao = round(random.uniform(1, 10), 2)
        taxa_ocupacao = round(random.uniform(40, 100), 2) if segmento == "Hotelaria" else None
        taxa_crescimento = round(dados_anteriores[14] * random.uniform(0.8, 1.2), 2)
        custo_marketing = round(receita * random.uniform(0.05, 0.2), 2)

    # Exemplo de retorno com colunas:
    return [
        data_registro.strftime("%Y-%m-%d"),  # 0 data
        data_registro.year,                  # 1 ano
        data_registro.month,                 # 2 mes
        data_registro.day,                   # 3 dia
        segmento,                            # 4 segmento
        fake.company(),                      # 5 empresa
        fake.city(),                         # 6 cidade
        numero_clientes,                     # 7
        ticket_medio,                        # 8
        receita,                             # 9
        custo,                               # 10
        lucro,                               # 11
        indice_satisfacao,                   # 12
        taxa_ocupacao,                       # 13
        taxa_crescimento,                    # 14
        custo_marketing,                     # 15
        regiao,                              # 16
        estado,                              # 17
        pais,                                # 18
        tipo_cliente,                        # 19
        canal_venda,                         # 20
        categoria_produto,                   # 21
        tipo_servico,                        # 22
        plano,                               # 23
        faixa_etaria,                        # 24
        genero,                              # 25
        fonte_trafego,                       # 26
        dispositivo,                         # 27
        sistema_operacional,                 # 28
        navegador                            # 29
    ]

# -------------------------------------------------------------
# MODO 2 (NOVO): Gera dados para UM hotel, 1 linha por cliente
# -------------------------------------------------------------

def gerar_dados_hotel_unico(fake, nome_hotel="Hotel Fictício", total_quartos=100,
                            data_inicio=None, data_fim=None, max_clientes_por_dia=5):
    """
    Gera um dataset detalhado para um único hotel, onde cada linha representa um cliente.
    
    Cada linha terá as seguintes colunas:
      0. id_registro
      1. data (YYYY-MM-DD)
      2. ano
      3. mes
      4. dia
      5. nome_hotel
      6. total_quartos
      7. ocupacao_diaria (%)  -> Calculado com base na soma dos quartos alugados no dia.
      8. nome_cliente
      9. tipo_de_quarto
      10. forma_de_pagamento
      11. quantidade_quartos (alugados pelo cliente)
      12. quantidade_diarias
      13. valor_diaria
      14. valor_total_diarias (quantidade_quartos × quantidade_diarias × valor_diaria)
      15. valor_outros_consumos
      16. total_pago (valor_total_diarias + valor_outros_consumos)
      17. despesa_fixa (diária do hotel)
      18. despesa_variavel
      19. despesa_mao_obra_direta
      20. despesa_financeira
      21. despesa_administrativa
      22. quartos_ocupados_dia (soma dos quartos alugados no dia)
      23. receita_quartos_dia (soma dos valor_total_diarias dos clientes)
      24. receita_total_dia (soma dos total_pago dos clientes)
      25. custo_total_dia (despesa_fixa + despesa_variavel + despesa_mao_obra_direta + despesa_financeira + despesa_administrativa)
      26. lucro_operacional_bruto_dia (receita_total_dia - custo_total_dia)
      27. adr_dia (receita_quartos_dia / quartos_ocupados_dia)
      28. revpar_dia (receita_quartos_dia / total_quartos)
      29. trevpar_dia (receita_total_dia / total_quartos)
      30. goppar_dia (lucro_operacional_bruto_dia / total_quartos)
    """
    if data_inicio is None or data_fim is None:
        raise ValueError("Informe data_inicio e data_fim para gerar dados do hotel único.")

    # Gera a lista de datas do período
    delta = data_fim - data_inicio
    datas = [data_inicio + timedelta(days=i) for i in range(delta.days + 1)]
    
    linhas = []
    id_registro = 1

    # Opções para tipo de quarto e forma de pagamento
    tipos_quarto = ["Standard", "Duplo", "Suite"]
    formas_pagamento = ["Cartão de Crédito", "Dinheiro", "PIX", "Transferência"]

    for dia_atual in datas:
        # Gera despesas diárias (fixas, variáveis, mão de obra, financeira, administrativa)
        despesa_fixa = round(random.uniform(500, 5000), 2)
        despesa_variavel = round(random.uniform(200, 2000), 2)
        despesa_mao_obra_direta = round(random.uniform(300, 3000), 2)
        despesa_financeira = round(random.uniform(50, 500), 2)
        despesa_administrativa = round(random.uniform(100, 1000), 2)
        custo_total_dia = despesa_fixa + despesa_variavel + despesa_mao_obra_direta + despesa_financeira + despesa_administrativa

        linhas_dia = []
        quartos_ocupados_dia = 0
        receita_quartos_dia = 0.0
        receita_total_dia = 0.0

        quartos_disponiveis = total_quartos
        num_clientes_dia = random.randint(1, max_clientes_por_dia)

        for _ in range(num_clientes_dia):
            if quartos_disponiveis <= 0:
                break

            nome_cliente = fake.name()
            tipo_de_quarto = random.choice(tipos_quarto)
            forma_de_pagamento = random.choice(formas_pagamento)
            qtd_quartos = random.randint(1, 2)
            if qtd_quartos > quartos_disponiveis:
                qtd_quartos = quartos_disponiveis
            quantidade_diarias = random.randint(1, 7)
            valor_diaria = round(random.uniform(50, 300), 2)
            valor_total_diarias = round(qtd_quartos * quantidade_diarias * valor_diaria, 2)
            valor_outros_consumos = round(random.uniform(0, 300), 2)
            total_pago = round(valor_total_diarias + valor_outros_consumos, 2)

            quartos_ocupados_dia += qtd_quartos
            receita_quartos_dia += valor_total_diarias
            receita_total_dia += total_pago
            quartos_disponiveis -= qtd_quartos

            linha = [
                id_registro,                           # 0: id_registro
                dia_atual.strftime("%Y-%m-%d"),         # 1: data
                dia_atual.year,                         # 2: ano
                dia_atual.month,                        # 3: mes
                dia_atual.day,                          # 4: dia
                nome_hotel,                             # 5: nome_hotel
                total_quartos,                          # 6: total_quartos
                0.0,                                    # 7: ocupacao_diaria (placeholder)
                nome_cliente,                           # 8: nome_cliente
                tipo_de_quarto,                         # 9: tipo_de_quarto
                forma_de_pagamento,                     # 10: forma_de_pagamento
                qtd_quartos,                            # 11: quantidade_quartos
                quantidade_diarias,                     # 12: quantidade_diarias
                valor_diaria,                           # 13: valor_diaria
                valor_total_diarias,                    # 14: valor_total_diarias
                valor_outros_consumos,                  # 15: valor_outros_consumos
                total_pago,                             # 16: total_pago
                despesa_fixa,                           # 17: despesa_fixa
                despesa_variavel,                       # 18: despesa_variavel
                despesa_mao_obra_direta,                # 19: despesa_mao_obra_direta
                despesa_financeira,                     # 20: despesa_financeira
                despesa_administrativa                  # 21: despesa_administrativa
            ]
            linhas_dia.append(linha)
            id_registro += 1

        # Cálculos agregados diários:
        # Quartos usados = total_quartos - quartos_disponiveis
        quartos_usados = total_quartos - quartos_disponiveis
        if total_quartos > 0:
            ocupacao_diaria = round((quartos_usados / total_quartos) * 100, 2)
        else:
            ocupacao_diaria = 0.0
        
        # Outras métricas diárias:
        lucro_operacional_bruto_dia = round(receita_total_dia - custo_total_dia, 2)
        adr_dia = round(receita_quartos_dia / quartos_ocupados_dia, 2) if quartos_ocupados_dia > 0 else 0
        revpar_dia = round(receita_quartos_dia / total_quartos, 2)
        trevpar_dia = round(receita_total_dia / total_quartos, 2)
        goppar_dia = round(lucro_operacional_bruto_dia / total_quartos, 2)

        # Atualiza cada registro do dia:
        for linha in linhas_dia:
            linha[7] = ocupacao_diaria  # Atualiza o placeholder da ocupação
            # Acrescenta as 9 novas colunas (índices 22 a 30):
            linha.extend([
                quartos_usados,         # 22: quartos_ocupados_dia
                round(receita_quartos_dia, 2),  # 23: receita_quartos_dia
                round(receita_total_dia, 2),    # 24: receita_total_dia
                round(custo_total_dia, 2),      # 25: custo_total_dia
                lucro_operacional_bruto_dia,    # 26: lucro_operacional_bruto_dia
                adr_dia,                        # 27: adr_dia
                revpar_dia,                     # 28: revpar_dia
                trevpar_dia,                    # 29: trevpar_dia
                goppar_dia                      # 30: goppar_dia
            ])
        linhas.extend(linhas_dia)
    return linhas
