# geradores.py

"""
geradores.py
Autor: Izairton Oliveira de Vasconcelos
Ponta Grossa - Paraná - Brasil

Descrição:
-----------
Este módulo foi desenvolvido para gerar dados fictícios e realistas de empresas, simulando diversas métricas
financeiras, operacionais, de marketing, satisfação do cliente e uso de produtos/serviços. Ele permite a geração
inicial dos dados e também a autocorrelação com dados previamente gerados, simulando a evolução de uma empresa
ao longo do tempo.

Funcionalidades Principais:
-----------------------------
1. Geração de Datas:
   - Função `gerar_data_aleatoria`: Gera uma data aleatória entre duas datas fornecidas (início e fim).

2. Geração de Dados Gerais:
   - Função `_gerar_dados_gerais`: Utiliza a biblioteca Faker para criar dados gerais (como região, estado, país,
     tipo de cliente, canal de venda, etc.) que são comuns a todas as empresas.

3. Geração de Dados de Empresas:
   - Função `gerar_dados_empresa`: Cria um conjunto extenso de métricas para uma empresa, incluindo:
       * Métricas básicas (número de clientes, ticket médio, receita, custo, lucro, índice de satisfação);
       * Métricas específicas de segmentos pré-definidos, como:
           - "Varejo" e "Indústria": quantidade de produtos, nível de estoque, giro de estoque;
           - "Hotelaria": taxa de ocupação e RevPAR;
           - "Educação": taxa de evasão;
           - "Saúde" e "Hospital": tempo médio de atendimento;
           - "TI", "SaaS" e segmentos relacionados: geração de métricas de uso (usuários ativos, tempo médio de sessão),
             receita recorrente (MRR/ARR) e funcionalidades utilizadas.
       * Métricas de marketing, satisfação, operações e despesas.
   - Suporta dois modos:
       a) Geração inicial (quando não há dados anteriores);
       b) Geração com autocorrelação (quando são fornecidos dados anteriores, permitindo pequenas variações para simular
          a evolução dos indicadores).

4. Aplicação de Outliers:
   - Função `gerar_dados_com_outliers`: Com uma probabilidade configurável, aplica outliers em determinadas métricas,
     alterando seus valores para simular anomalias ou variações extremas.

5. Tratamento Seguro de Limites:
   - A função auxiliar `_safe_randint` garante que os limites passados para `random.randint` sejam convertidos para
     inteiros, evitando erros de tipo ao gerar números aleatórios em intervalos definidos.

Uso:
-----
- Este módulo pode ser utilizado diretamente ou integrado a um script principal (por exemplo, `main.py`), onde o
  usuário pode especificar:
     * O número de registros a serem gerados;
     * Os segmentos para os quais os dados serão criados (ex.: "Varejo", "Hotelaria", "TI", etc.);
     * O período de geração de dados (data de início e data final);
     * A probabilidade de aplicação de outliers;
     * O nome do arquivo de saída (por exemplo, CSV) onde os dados serão salvos.
- Para segmentos que não possuem tratamento específico (por exemplo, "Finanças", "Aviação", "Metalurgia", etc.),
  as métricas específicas desses segmentos não serão aplicadas (ficarão com valor `None` ou padrão), mas as métricas
  gerais continuarão sendo geradas normalmente.

Observações:
-------------
- As bibliotecas Faker e numpy são utilizadas para gerar dados realistas e aplicar distribuições estatísticas.
- O código é modular e permite fácil extensão para adicionar novos segmentos ou métricas, conforme necessário.
- Este módulo foi projetado para suportar a simulação de dados para testes, simulações e análises em projetos de
  Business Intelligence e Data Analytics.

Desenvolvido para facilitar a criação de datasets sintéticos e apoiar a validação e performance de sistemas analíticos.
"""

import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

def gerar_data_aleatoria(inicio, fim):
    """
    Gera uma data aleatória entre 'inicio' e 'fim'.
    """
    delta = fim - inicio
    dias_delta = delta.days
    data_aleatoria = inicio + timedelta(days=random.randint(0, dias_delta))
    return data_aleatoria

def _safe_randint(a, b):
    """
    Versão segura de random.randint, que converte 'a' e 'b' para int,
    e troca se 'a' ficar maior que 'b'.
    """
    a = int(a)
    b = int(b)
    if a > b:
        a, b = b, a
    return random.randint(a, b)

def _gerar_dados_gerais(fake, segmento):
    """
    Função auxiliar para gerar dados gerais (regionais, demográficos, etc.).
    """
    regiao = fake.estado_nome()
    estado = fake.estado_sigla()
    pais = "Brasil"  # fixo, mas pode ser parametrizado
    tipo_cliente = random.choice(["B2B", "B2C", "Pessoa Física", "Pessoa Jurídica"])
    canal_venda = random.choice(["Loja física", "Online", "Aplicativo", "Telefone", "Representante"])

    # Segmentos que podem ter produtos
    categoria_produto = (
        random.choice(["Eletrônicos", "Roupas", "Alimentos", "Livros", "Móveis", "Outros"])
        if segmento in ["Varejo", "Indústria"] else None
    )

    # Segmentos que podem ter serviços
    tipo_servico = (
        random.choice(["Consultoria", "Suporte", "Treinamento", "Desenvolvimento", "Outros"])
        if segmento in ["Serviços", "TI", "Consultoria", "Saúde", "Educação", "Banco", "Hospital"]
        else None
    )

    # Segmentos que podem ter planos (SaaS, etc.)
    plano = (
        random.choice(["Básico", "Premium", "Gratuito", "Teste"])
        if segmento in ["TI", "Serviços", "SaaS"] else None
    )

    faixa_etaria = random.choice(["18-25", "26-35", "36-45", "46-55", "55+"])
    genero = random.choice(["Masculino", "Feminino", "Outro"])
    fonte_trafego = random.choice(["Busca orgânica", "Anúncio pago", "Rede social", "Email", "Referência", "Direto"])
    dispositivo = random.choice(["Desktop", "Mobile", "Tablet"])
    sistema_operacional = random.choice(["Windows", "macOS", "Linux", "Android", "iOS"])
    navegador = random.choice(["Chrome", "Firefox", "Safari", "Edge", "Outro"])

    return (
        regiao,
        estado,
        pais,
        tipo_cliente,
        canal_venda,
        categoria_produto,
        tipo_servico,
        plano,
        faixa_etaria,
        genero,
        fonte_trafego,
        dispositivo,
        sistema_operacional,
        navegador
    )

def gerar_dados_empresa(fake, segmento, data_registro, dados_anteriores=None):
    """
    Gera dados fictícios para uma única empresa, com opção de autocorrelação.

    Se 'dados_anteriores' for None, gera a primeira linha.
    Caso contrário, faz a autocorrelação com base nos valores anteriores.
    """

    # Gera dados gerais independentes
    (
        regiao, estado, pais, tipo_cliente, canal_venda, categoria_produto,
        tipo_servico, plano, faixa_etaria, genero, fonte_trafego,
        dispositivo, sistema_operacional, navegador
    ) = _gerar_dados_gerais(fake, segmento)

    # --------------------------------------------------------------------------------
    # 1) BLOCO INICIAL (SEM autocorrelação)
    # --------------------------------------------------------------------------------
    if dados_anteriores is None:
        # -- MÉTRICAS BÁSICAS --
        numero_clientes = int(np.random.lognormal(mean=4.6, sigma=0.8))  # média ~100
        ticket_medio = round(np.random.lognormal(mean=3.7, sigma=0.5), 2)  # média ~40
        receita = round(numero_clientes * ticket_medio, 2)
        custo = round(receita * np.random.uniform(0.6, 0.95), 2)
        lucro = round(receita - custo, 2)
        indice_satisfacao = max(1.0, min(10.0, round(np.random.normal(loc=7.5, scale=1.5), 1)))
        taxa_ocupacao = (
            round(np.random.uniform(60.0, 100.0), 2)
            if segmento == "Hotelaria" else None
        )
        taxa_crescimento = round(np.random.uniform(-10.0, 30.0), 2)
        custo_marketing = round(receita * np.random.uniform(0.05, 0.2), 2)
        investimento_publicidade = round(np.random.uniform(1000.0, 10000.0), 2)
        previsao_vendas = round(receita * (1 + np.random.uniform(0.05, 0.15)), 2)
        previsao_custos = round(custo * (1 + np.random.uniform(0.0, 0.1)), 2)
        sensibilidade_negocios = round(np.random.uniform(0, 100), 2)
        indice_correcao = round(np.random.uniform(0.95, 1.05), 3)
        programacao_linear = round(np.random.uniform(0, 1000), 2)

        # -- MÉTRICAS NOVAS (INICIAIS) --
        quantidade_produtos = (
            _safe_randint(1, 200)
            if segmento in ["Varejo", "Indústria"] else 0
        )
        custo_por_cliente = round(custo / numero_clientes, 2) if numero_clientes > 0 else 0.0
        receita_por_cliente = round(receita / numero_clientes, 2) if numero_clientes > 0 else 0.0
        lucro_por_cliente = round(lucro / numero_clientes, 2) if numero_clientes > 0 else 0.0
        desconto_medio = round(np.random.uniform(0, 50), 2)
        if (ticket_medio + desconto_medio) > 0:
            percentual_desconto = round((desconto_medio / (ticket_medio + desconto_medio)) * 100, 2)
        else:
            percentual_desconto = 0.0
        taxa_conversao = round(np.random.uniform(1, 10), 2)  # 1–10%
        vendas_por_vendedor = (
            _safe_randint(1, 50)
            if segmento in ["Varejo", "Serviços"] else 0
        )
        comissao_vendas = (
            round(receita * np.random.uniform(0.01, 0.05), 2)
            if vendas_por_vendedor > 0 else 0.0
        )
        valor_impostos = round(receita * np.random.uniform(0.1, 0.3), 2)
        frete_medio = (
            round(np.random.uniform(5, 50), 2)
            if segmento == "Varejo" else 0.0
        )
        pedidos_por_cliente = round(np.random.uniform(1, 3), 2)
        LTV = round(np.random.lognormal(mean=5, sigma=0.7), 2)
        CAC = round(np.random.uniform(10, 100), 2)
        MRR = (
            round(receita * np.random.uniform(0.8, 1.2), 2)
            if segmento in ["SaaS", "TI"] else 0.0
        )
        ARR = round(MRR * 12, 2) if MRR > 0 else 0.0

        # -- MÉTRICAS DE MARKETING --
        receita_media_diaria = round(receita / 30, 2)
        custo_por_clique = round(np.random.uniform(0.5, 5), 2)
        custo_por_mil_impressoes = round(np.random.uniform(5, 20), 2)
        taxa_de_clique = round(np.random.uniform(0.5, 5), 2)
        impressoes = _safe_randint(1000, 10000)
        cliques = int(impressoes * (taxa_de_clique / 100))
        leads_gerados = _safe_randint(10, 100)
        custo_por_lead = (
            round(custo_marketing / leads_gerados, 2)
            if leads_gerados > 0 else 0.0
        )
        ROAS = (
            round(receita / investimento_publicidade, 2)
            if investimento_publicidade > 0 else 0.0
        )

        # -- MÉTRICAS DE SATISFAÇÃO --
        avaliacao_media = max(1.0, min(5.0, round(np.random.normal(loc=4.0, scale=0.5), 1)))
        numero_avaliacoes = _safe_randint(10, 100)
        NPS = _safe_randint(-100, 100)
        CSAT = _safe_randint(1, 5)
        reclamacoes = _safe_randint(0, 10)
        tempo_medio_resposta = round(np.random.uniform(1, 24), 2)  # horas

        # -- MÉTRICAS DE OPERAÇÕES/LOGÍSTICA --
        tempo_medio_entrega = round(np.random.uniform(1, 7), 2)  # dias
        taxa_devolucao = round(np.random.uniform(1, 10), 2)
        nivel_estoque = (
            _safe_randint(100, 1000)
            if segmento in ["Varejo", "Indústria"] else 0
        )
        giro_estoque = (
            round(np.random.uniform(1, 10), 2)
            if nivel_estoque > 0 else 0.0
        )
        custo_estoque = (
            round(nivel_estoque * np.random.uniform(5, 20), 2)
            if nivel_estoque > 0 else 0.0
        )
        numero_fornecedores = _safe_randint(1, 10)
        taxa_de_defeito = round(np.random.uniform(0.1, 5), 2)

        # -- MÉTRICAS DE USO DE PRODUTO/SERVIÇO --
        if segmento in ["SaaS", "TI", "Aplicativo"]:
            usuarios_ativos = int(np.random.lognormal(mean=5, sigma=0.9))
            funcionalidade_mais_usada = random.choice(["FuncA", "FuncB", "FuncC", "Outra"])
        else:
            usuarios_ativos = 0
            funcionalidade_mais_usada = None
        tempo_medio_sessao = round(np.random.uniform(5, 60), 2)
        taxa_retencao = round(np.random.uniform(30, 90), 2)
        churn_rate = round(np.random.uniform(1, 10), 2)
        numero_sessoes = _safe_randint(1, 50)

        # -- MÉTRICAS ESPECÍFICAS --
        RevPAR = (
            round(np.random.uniform(50, 200), 2)
            if segmento == "Hotelaria" else None
        )
        taxa_evasao = (
            round(np.random.uniform(5, 20), 2)
            if segmento == "Educação" else None
        )
        tempo_medio_atendimento = (
            round(np.random.uniform(15, 60), 2)
            if segmento in ["Saúde", "Hospital"] else None
        )

        # -- DESPESAS --
        despesa_administrativa = round(np.random.uniform(500, 5000), 2)
        despesa_com_pessoal = round(np.random.uniform(2000, 20000), 2)
        despesa_fixa = round(np.random.uniform(1000, 10000), 2)
        despesa_variavel = round(np.random.uniform(500, 5000), 2)
        despesa_tributaria = round(receita * np.random.uniform(0.05, 0.15), 2)
        despesa_financeira = round(np.random.uniform(100, 1000), 2)

    # --------------------------------------------------------------------------------
    # 2) BLOCO COM AUTOCORRELAÇÃO (SE dados_anteriores NÃO FOR None)
    # --------------------------------------------------------------------------------
    else:
        # --- MÉTRICAS BÁSICAS ---
        numero_clientes = int(dados_anteriores[7] * np.random.normal(loc=1.0, scale=0.05))
        numero_clientes = max(1, numero_clientes)

        ticket_medio = round(dados_anteriores[8] * np.random.normal(loc=1.0, scale=0.02), 2)
        ticket_medio = max(0.01, ticket_medio)

        receita = round(numero_clientes * ticket_medio, 2)
        custo = round(receita * np.random.uniform(0.6, 0.95), 2)
        if custo > receita:
            custo = round(receita * 0.95, 2)

        lucro = round(receita - custo, 2)
        indice_satisfacao = max(1.0, min(10.0, round(np.random.normal(loc=7.5, scale=1.5), 1)))

        # taxa_ocupacao (só para Hotelaria)
        if segmento == "Hotelaria":
            valor_anterior = dados_anteriores[13]
            if valor_anterior is None:
                taxa_ocupacao = round(np.random.uniform(60, 100), 2)
            else:
                nova = round(np.random.normal(loc=valor_anterior, scale=2.0), 2)
                taxa_ocupacao = max(0.0, min(100.0, nova))
        else:
            taxa_ocupacao = None

        taxa_crescimento = round(np.random.normal(loc=dados_anteriores[14], scale=5.0), 2)
        custo_marketing = round(receita * np.random.uniform(0.05, 0.2), 2)

        # investimento_publicidade varia ± 2000 do valor anterior
        valor_anterior_pub = dados_anteriores[16]
        investimento_publicidade = round(
            np.random.uniform(
                max(0.0, valor_anterior_pub - 2000),
                valor_anterior_pub + 2000
            ), 2
        )

        previsao_vendas = round(receita * (1 + np.random.uniform(0.05, 0.15)), 2)
        previsao_custos = round(custo * (1 + np.random.uniform(0.0, 0.1)), 2)

        sensibilidade_negocios = round(
            np.random.uniform(
                max(0.0, dados_anteriores[19] - 10),
                min(100, dados_anteriores[19] + 10)
            ), 2
        )

        indice_correcao = round(
            np.random.uniform(
                max(0.9, dados_anteriores[20] - 0.05),
                min(dados_anteriores[20] + 0.05, 1.10)
            ), 3
        )

        programacao_linear = round(
            np.random.uniform(
                max(0.0, dados_anteriores[21] - 200),
                dados_anteriores[21] + 200
            ), 2
        )

        # --- MÉTRICAS NOVAS ---
        # quantidade_produtos (só para Varejo/Indústria)
        if segmento in ["Varejo", "Indústria"]:
            valor_anterior_qtd = dados_anteriores[36]
            if valor_anterior_qtd is None:
                # Se não houver valor anterior, gera algo inicial
                quantidade_produtos = _safe_randint(1, 200)
            else:
                lower = max(1, int(valor_anterior_qtd) - 50)
                upper = int(valor_anterior_qtd) + 50
                quantidade_produtos = _safe_randint(lower, upper)
        else:
            quantidade_produtos = 0

        custo_por_cliente = round(custo / numero_clientes, 2) if numero_clientes > 0 else 0.0
        receita_por_cliente = round(receita / numero_clientes, 2) if numero_clientes > 0 else 0.0
        lucro_por_cliente = round(lucro / numero_clientes, 2) if numero_clientes > 0 else 0.0

        # desconto_medio
        valor_anterior_desc = dados_anteriores[40]
        if valor_anterior_desc is None:
            desconto_medio = round(np.random.uniform(0, 50), 2)
        else:
            desconto_medio = round(np.random.normal(loc=valor_anterior_desc, scale=5), 2)
        desconto_medio = max(0.0, desconto_medio)

        if (ticket_medio + desconto_medio) > 0:
            percentual_desconto = round(
                (desconto_medio / (ticket_medio + desconto_medio)) * 100, 2
            )
        else:
            percentual_desconto = 0.0

        # taxa_conversao
        valor_anterior_conv = dados_anteriores[42]
        if valor_anterior_conv is None:
            taxa_conversao = round(np.random.uniform(1, 10), 2)
        else:
            taxa_conversao = round(np.random.normal(loc=valor_anterior_conv, scale=1), 2)
        taxa_conversao = max(0.0, min(100.0, taxa_conversao))

        # vendas_por_vendedor
        if segmento in ["Varejo", "Serviços"]:
            valor_anterior_vpv = dados_anteriores[43]
            if valor_anterior_vpv is None:
                vendas_por_vendedor = _safe_randint(1, 50)
            else:
                lower = max(0, int(valor_anterior_vpv) - 10)
                upper = int(valor_anterior_vpv) + 10
                vendas_por_vendedor = _safe_randint(lower, upper)
        else:
            vendas_por_vendedor = 0

        comissao_vendas = (
            round(receita * np.random.uniform(0.01, 0.05), 2)
            if vendas_por_vendedor > 0 else 0.0
        )

        valor_impostos = round(receita * np.random.uniform(0.1, 0.3), 2)

        # frete_medio (só se Varejo)
        if segmento == "Varejo":
            valor_anterior_frete = dados_anteriores[46]
            if valor_anterior_frete is None:
                frete_medio = round(np.random.uniform(5, 50), 2)
            else:
                frete_medio = round(np.random.normal(loc=valor_anterior_frete, scale=2), 2)
            frete_medio = max(0.0, frete_medio)
        else:
            frete_medio = 0.0

        # pedidos_por_cliente
        valor_anterior_ped = dados_anteriores[47]
        if valor_anterior_ped is None:
            pedidos_por_cliente = round(np.random.uniform(1, 3), 2)
        else:
            pedidos_por_cliente = round(
                np.random.uniform(
                    max(1.0, valor_anterior_ped - 0.5),
                    valor_anterior_ped + 0.5
                ), 2
            )
        pedidos_por_cliente = max(1.0, pedidos_por_cliente)

        # LTV
        valor_anterior_ltv = dados_anteriores[48]
        if valor_anterior_ltv and valor_anterior_ltv > 0:
            LTV = round(
                np.random.lognormal(mean=np.log(max(1, valor_anterior_ltv)), sigma=0.2),
                2
            )
        else:
            LTV = round(np.random.lognormal(mean=5, sigma=0.7), 2)

        # CAC
        valor_anterior_cac = dados_anteriores[49]
        if valor_anterior_cac is None:
            CAC = round(np.random.uniform(10, 100), 2)
        else:
            CAC = round(np.random.normal(loc=valor_anterior_cac, scale=5), 2)
        CAC = max(0.0, CAC)

        # MRR e ARR (somente se SaaS/TI)
        if segmento in ["SaaS", "TI"]:
            MRR = round(receita * np.random.uniform(0.8, 1.2), 2)
            ARR = round(MRR * 12, 2)
        else:
            MRR = 0.0
            ARR = 0.0

        receita_media_diaria = round(receita / 30, 2)

        # --- MÉTRICAS DE MARKETING ---
        valor_anterior_cpc = dados_anteriores[53]
        if valor_anterior_cpc is None:
            custo_por_clique = round(np.random.uniform(0.5, 5), 2)
        else:
            custo_por_clique = round(np.random.normal(loc=valor_anterior_cpc, scale=0.5), 2)
        custo_por_clique = max(0.01, custo_por_clique)

        valor_anterior_cpm = dados_anteriores[54]
        if valor_anterior_cpm is None:
            custo_por_mil_impressoes = round(np.random.uniform(5, 20), 2)
        else:
            custo_por_mil_impressoes = round(np.random.normal(loc=valor_anterior_cpm, scale=2), 2)
        custo_por_mil_impressoes = max(0.01, custo_por_mil_impressoes)

        valor_anterior_tclique = dados_anteriores[55]
        if valor_anterior_tclique is None:
            taxa_de_clique = round(np.random.uniform(0.5, 5), 2)
        else:
            taxa_de_clique = round(np.random.normal(loc=valor_anterior_tclique, scale=0.5), 2)
        taxa_de_clique = max(0.0, min(100.0, taxa_de_clique))

        valor_anterior_impress = dados_anteriores[56]
        if valor_anterior_impress is None:
            impressoes = _safe_randint(1000, 10000)
        else:
            lower = max(100, int(valor_anterior_impress) - 1000)
            upper = int(valor_anterior_impress) + 1000
            impressoes = _safe_randint(lower, upper)

        cliques = int(impressoes * (taxa_de_clique / 100))

        valor_anterior_leads = dados_anteriores[58]
        if valor_anterior_leads is None:
            leads_gerados = _safe_randint(10, 100)
        else:
            lower = max(0, int(valor_anterior_leads) - 20)
            upper = int(valor_anterior_leads) + 20
            leads_gerados = _safe_randint(lower, upper)

        custo_por_lead = (
            round(custo_marketing / leads_gerados, 2)
            if leads_gerados > 0 else 0.0
        )

        ROAS = (
            round(receita / investimento_publicidade, 2)
            if investimento_publicidade > 0 else 0.0
        )

        # --- MÉTRICAS DE SATISFAÇÃO ---
        valor_anterior_av = dados_anteriores[61]
        if valor_anterior_av is None:
            avaliacao_media = max(1.0, min(5.0, round(np.random.normal(loc=4.0, scale=0.5), 1)))
        else:
            avaliacao_media = max(
                1.0,
                min(5.0, round(np.random.normal(loc=valor_anterior_av, scale=0.3), 1))
            )

        lower = max(0, int(dados_anteriores[62]) - 20)
        upper = int(dados_anteriores[62]) + 20
        numero_avaliacoes = _safe_randint(lower, upper)

        nps_lower = max(-100, int(dados_anteriores[63]) - 20)
        nps_upper = min(100, int(dados_anteriores[63]) + 20)
        NPS = _safe_randint(nps_lower, nps_upper)

        csat_lower = max(1, int(dados_anteriores[64]) - 1)
        csat_upper = min(5, int(dados_anteriores[64]) + 1)
        CSAT = _safe_randint(csat_lower, csat_upper)

        lower = max(0, int(dados_anteriores[65]) - 2)
        upper = int(dados_anteriores[65]) + 2
        reclamacoes = _safe_randint(lower, upper)

        valor_anterior_tmr = dados_anteriores[66]
        if valor_anterior_tmr is None:
            tempo_medio_resposta = round(np.random.uniform(1, 24), 2)
        else:
            tempo_medio_resposta = round(
                np.random.uniform(
                    max(0.1, valor_anterior_tmr - 2),
                    valor_anterior_tmr + 2
                ), 2
            )
        tempo_medio_resposta = max(0.1, tempo_medio_resposta)

        # --- MÉTRICAS DE OPERAÇÕES/LOGÍSTICA ---
        valor_anterior_tent = dados_anteriores[67]
        if valor_anterior_tent is None:
            tempo_medio_entrega = round(np.random.uniform(1, 7), 2)
        else:
            tempo_medio_entrega = round(
                np.random.uniform(
                    max(0.1, valor_anterior_tent - 1),
                    valor_anterior_tent + 1
                ), 2
            )
        tempo_medio_entrega = max(0.1, tempo_medio_entrega)

        valor_anterior_tdev = dados_anteriores[68]
        if valor_anterior_tdev is None:
            taxa_devolucao = round(np.random.uniform(1, 10), 2)
        else:
            taxa_devolucao = round(
                np.random.uniform(
                    max(0.0, valor_anterior_tdev - 2),
                    min(valor_anterior_tdev + 2, 100.0)
                ), 2
            )

        if segmento in ["Varejo", "Indústria"]:
            val_estq = dados_anteriores[69]
            if val_estq is None:
                nivel_estoque = _safe_randint(100, 1000)
            else:
                lower = max(0, int(val_estq) - 200)
                upper = int(val_estq) + 200
                nivel_estoque = _safe_randint(lower, upper)
        else:
            nivel_estoque = 0

        val_giro = dados_anteriores[70]
        if nivel_estoque > 0 and val_giro is not None:
            giro_estoque = round(
                np.random.uniform(
                    max(0.1, val_giro - 2),
                    val_giro + 2
                ), 2
            )
        elif nivel_estoque > 0:
            giro_estoque = round(np.random.uniform(1, 10), 2)
        else:
            giro_estoque = 0.0

        custo_estoque = (
            round(nivel_estoque * np.random.uniform(5, 20), 2)
            if nivel_estoque > 0 else 0.0
        )

        nf_lower = max(1, int(dados_anteriores[72]) - 2)
        nf_upper = int(dados_anteriores[72]) + 2
        numero_fornecedores = _safe_randint(nf_lower, nf_upper)

        valor_anterior_def = dados_anteriores[73]
        if valor_anterior_def is None:
            taxa_de_defeito = round(np.random.uniform(0.1, 5), 2)
        else:
            taxa_de_defeito = round(
                np.random.uniform(
                    max(0.0, valor_anterior_def - 0.5),
                    min(valor_anterior_def + 0.5, 100.0)
                ), 2
            )

        # --- MÉTRICAS DE USO DE PRODUTO/SERVIÇO ---
        if segmento in ["SaaS", "TI", "Aplicativo"]:
            valor_anterior_ua = dados_anteriores[74]
            if valor_anterior_ua is None or valor_anterior_ua <= 0:
                usuarios_ativos = int(np.random.lognormal(mean=5, sigma=0.9))
            else:
                usuarios_ativos = int(np.random.lognormal(mean=np.log(max(1, valor_anterior_ua)), sigma=0.2))
            funcionalidade_mais_usada = random.choice(["FuncA", "FuncB", "FuncC", "Outra"])
        else:
            usuarios_ativos = 0
            funcionalidade_mais_usada = None

        valor_anterior_sessao = dados_anteriores[75]
        if valor_anterior_sessao is None:
            tempo_medio_sessao = round(np.random.uniform(5, 60), 2)
        else:
            tempo_medio_sessao = round(
                np.random.uniform(
                    max(0.1, valor_anterior_sessao - 10),
                    valor_anterior_sessao + 10
                ), 2
            )

        valor_anterior_ret = dados_anteriores[76]
        if valor_anterior_ret is None:
            taxa_retencao = round(np.random.uniform(30, 90), 2)
        else:
            taxa_retencao = round(
                np.random.uniform(
                    max(0.0, valor_anterior_ret - 10),
                    min(valor_anterior_ret + 10, 100)
                ), 2
            )

        valor_anterior_churn = dados_anteriores[77]
        if valor_anterior_churn is None:
            churn_rate = round(np.random.uniform(1, 10), 2)
        else:
            churn_rate = round(
                np.random.uniform(
                    max(0.0, valor_anterior_churn - 2),
                    min(valor_anterior_churn + 2, 100)
                ), 2
            )

        valor_anterior_sessoes = dados_anteriores[79]
        if valor_anterior_sessoes is None:
            numero_sessoes = _safe_randint(1, 50)
        else:
            lower = max(1, int(valor_anterior_sessoes) - 5)
            upper = int(valor_anterior_sessoes) + 5
            numero_sessoes = _safe_randint(lower, upper)

        # --- MÉTRICAS ESPECÍFICAS ---
        # RevPAR (só se Hotelaria)
        if segmento == "Hotelaria":
            valor_anterior_revpar = dados_anteriores[80]
            if valor_anterior_revpar is None:
                RevPAR = round(np.random.uniform(50, 200), 2)
            else:
                RevPAR = round(
                    np.random.uniform(
                        max(0.0, valor_anterior_revpar - 20),
                        valor_anterior_revpar + 20
                    ), 2
                )
        else:
            RevPAR = None

        # taxa_evasao (só se Educação)
        if segmento == "Educação":
            valor_anterior_evasao = dados_anteriores[81]
            if valor_anterior_evasao is None:
                taxa_evasao = round(np.random.uniform(5, 20), 2)
            else:
                taxa_evasao = round(
                    np.random.uniform(
                        max(0.0, valor_anterior_evasao - 5),
                        min(valor_anterior_evasao + 5, 100)
                    ), 2
                )
        else:
            taxa_evasao = None

        # tempo_medio_atendimento (só se Saúde/Hospital)
        if segmento in ["Saúde", "Hospital"]:
            valor_anterior_tma = dados_anteriores[82]
            if valor_anterior_tma is None:
                tempo_medio_atendimento = round(np.random.uniform(15, 60), 2)
            else:
                tempo_medio_atendimento = round(
                    np.random.uniform(
                        max(0.1, valor_anterior_tma - 15),
                        valor_anterior_tma + 15
                    ), 2
                )
        else:
            tempo_medio_atendimento = None

        # --- DESPESAS ---
        valor_anterior_adm = dados_anteriores[83]
        if valor_anterior_adm is None:
            despesa_administrativa = round(np.random.uniform(500, 5000), 2)
        else:
            despesa_administrativa = round(np.random.normal(loc=valor_anterior_adm, scale=500), 2)
        despesa_administrativa = max(0.0, despesa_administrativa)

        valor_anterior_pessoal = dados_anteriores[84]
        if valor_anterior_pessoal is None:
            despesa_com_pessoal = round(np.random.uniform(2000, 20000), 2)
        else:
            despesa_com_pessoal = round(np.random.normal(loc=valor_anterior_pessoal, scale=1000), 2)
        despesa_com_pessoal = max(0.0, despesa_com_pessoal)

        valor_anterior_fixa = dados_anteriores[85]
        if valor_anterior_fixa is None:
            despesa_fixa = round(np.random.uniform(1000, 10000), 2)
        else:
            despesa_fixa = round(np.random.normal(loc=valor_anterior_fixa, scale=500), 2)
        despesa_fixa = max(0.0, despesa_fixa)

        valor_anterior_var = dados_anteriores[86]
        if valor_anterior_var is None:
            despesa_variavel = round(np.random.uniform(500, 5000), 2)
        else:
            despesa_variavel = round(np.random.normal(loc=valor_anterior_var, scale=500), 2)
        despesa_variavel = max(0.0, despesa_variavel)

        despesa_tributaria = round(receita * np.random.uniform(0.05, 0.15), 2)

        valor_anterior_fin = dados_anteriores[88]
        if valor_anterior_fin is None:
            despesa_financeira = round(np.random.uniform(100, 1000), 2)
        else:
            despesa_financeira = round(np.random.normal(loc=valor_anterior_fin, scale=100), 2)
        despesa_financeira = max(0.0, despesa_financeira)

    # --------------------------------------------------------------------------------
    # 3) MONTA O VETOR DE RETORNO
    # --------------------------------------------------------------------------------
    return [
        data_registro.strftime("%Y-%m-%d"),  #  0
        data_registro.year,                  #  1
        data_registro.month,                 #  2
        data_registro.day,                   #  3
        segmento,                            #  4
        fake.company(),                      #  5
        fake.city(),                         #  6
        numero_clientes,                     #  7
        ticket_medio,                        #  8
        receita,                             #  9
        custo,                               # 10
        lucro,                               # 11
        indice_satisfacao,                   # 12
        taxa_ocupacao,                       # 13
        taxa_crescimento,                    # 14
        custo_marketing,                     # 15
        investimento_publicidade,            # 16
        previsao_vendas,                     # 17
        previsao_custos,                     # 18
        sensibilidade_negocios,              # 19
        indice_correcao,                     # 20
        programacao_linear,                  # 21
        regiao,                              # 22
        estado,                              # 23
        pais,                                # 24
        tipo_cliente,                        # 25
        canal_venda,                         # 26
        categoria_produto,                   # 27
        tipo_servico,                        # 28
        plano,                               # 29
        faixa_etaria,                        # 30
        genero,                              # 31
        fonte_trafego,                       # 32
        dispositivo,                         # 33
        sistema_operacional,                 # 34
        navegador,                           # 35
        quantidade_produtos,                 # 36
        custo_por_cliente,                   # 37
        receita_por_cliente,                 # 38
        lucro_por_cliente,                   # 39
        desconto_medio,                      # 40
        percentual_desconto,                 # 41
        taxa_conversao,                      # 42
        vendas_por_vendedor,                 # 43
        comissao_vendas,                     # 44
        valor_impostos,                      # 45
        frete_medio,                         # 46
        pedidos_por_cliente,                 # 47
        LTV,                                 # 48
        CAC,                                 # 49
        MRR,                                 # 50
        ARR,                                 # 51
        receita_media_diaria,                # 52
        custo_por_clique,                    # 53
        custo_por_mil_impressoes,            # 54
        taxa_de_clique,                      # 55
        impressoes,                          # 56
        cliques,                             # 57
        leads_gerados,                       # 58
        custo_por_lead,                      # 59
        ROAS,                                # 60
        avaliacao_media,                     # 61
        numero_avaliacoes,                   # 62
        NPS,                                 # 63
        CSAT,                                # 64
        reclamacoes,                         # 65
        tempo_medio_resposta,                # 66
        tempo_medio_entrega,                 # 67
        taxa_devolucao,                      # 68
        nivel_estoque,                       # 69
        giro_estoque,                        # 70
        custo_estoque,                       # 71
        numero_fornecedores,                 # 72
        taxa_de_defeito,                     # 73
        usuarios_ativos,                     # 74
        tempo_medio_sessao,                  # 75
        taxa_retencao,                       # 76
        churn_rate,                          # 77
        funcionalidade_mais_usada,           # 78
        numero_sessoes,                      # 79
        RevPAR,                              # 80
        taxa_evasao,                         # 81
        tempo_medio_atendimento,             # 82
        despesa_administrativa,              # 83
        despesa_com_pessoal,                 # 84
        despesa_fixa,                        # 85
        despesa_variavel,                    # 86
        despesa_tributaria,                  # 87
        despesa_financeira                   # 88
    ]

def gerar_dados_com_outliers(dados, probabilidade_outlier=0.01):
    """
    Aplica outliers em certas colunas numéricas, com determinada probabilidade.
    """
    if random.random() < probabilidade_outlier:
        # Índices das colunas que podem ter outliers
        indices_numericos = [
            8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
            33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
            47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
            61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
            75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88
        ]

        indice_outlier = random.choice(indices_numericos)
        fator_outlier = np.random.uniform(0.5, 2.0)

        if isinstance(dados[indice_outlier], (int, float)):
            valor_modificado = dados[indice_outlier] * fator_outlier
            dados[indice_outlier] = round(valor_modificado, 2)

            # Ajustes para manter valores mínimos
            if indice_outlier in [
                8, 9, 10, 16, 17, 18, 19, 22, 33, 34, 35, 36, 40, 41, 42,
                43, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 56, 57, 60,
                61, 63, 64, 66, 67, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88
            ]:
                dados[indice_outlier] = max(1, dados[indice_outlier])
            elif indice_outlier in [13, 38, 55, 58, 59, 62, 65, 68, 72]:
                # Exemplo de indices que precisam ficar >= 0 e <= 100
                dados[indice_outlier] = max(0.0, min(dados[indice_outlier], 100.0))

    return dados
