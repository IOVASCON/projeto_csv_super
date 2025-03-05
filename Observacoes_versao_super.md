# Documentação dos Scripts do Projeto

Este documento explica de forma detalhada os scripts criados neste projeto, facilitando a compreensão e manutenção do código. Abaixo, os principais pontos de cada arquivo são apresentados em tópicos, com emojis para melhor visualização.

---

## :file_folder: Arquivos do Projeto

- **geradores.py**  
  Responsável por gerar os dados sintéticos de empresas, simulando métricas financeiras, operacionais, de marketing, satisfação, entre outras. Suporta geração inicial e autocorrelação (evolução dos dados) e também aplica outliers.

- **main.py**  
  Script principal que orquestra a geração dos dados. Processa os parâmetros da linha de comando, integra as funções do `geradores.py` e salva o dataset final em um arquivo CSV.

- **util.py**  
  Contém funções utilitárias, especialmente para a criação e escrita de arquivos CSV, permitindo que os dados gerados sejam exportados de forma organizada.

---

## :hammer_and_wrench: Detalhamento dos Scripts

### :sparkles: **geradores.py**

- **Objetivo:**  
  Gerar dados fictícios realistas para simular indicadores de empresas, com suporte para:
  - Geração inicial de dados.
  - Autocorrelação (simulação da evolução dos indicadores com base em dados anteriores).
  - Aplicação de outliers para simular variações extremas.

- **Funções Principais:**
  - **`gerar_data_aleatoria(inicio, fim)`**  
    - :calendar: **Propósito:** Gera uma data aleatória entre as datas `inicio` e `fim`.
    - :arrow_right: Calcula a quantidade de dias entre as datas.
    - :arrow_right: Retorna uma data obtida somando um número aleatório de dias ao `inicio`.

  - **`_gerar_dados_gerais(fake, segmento)`**  
    - :computer: **Propósito:** Utiliza a biblioteca Faker para criar dados gerais (região, estado, país, tipo de cliente, etc.).
    - :arrow_right: Ajusta valores específicos de acordo com o segmento (ex.: categoria de produto para "Varejo" e "Indústria", tipo de serviço para "Saúde" ou "TI", etc.).

  - **`gerar_dados_empresa(fake, segmento, data_registro, dados_anteriores=None)`**  
    - :chart_with_upwards_trend: **Propósito:** Gera um conjunto completo de métricas para uma empresa.
    - :one: **Geração Inicial:** Se `dados_anteriores` for `None`, calcula as métricas iniciais usando distribuições estatísticas.
    - :two: **Autocorrelação:** Se dados anteriores forem fornecidos, gera os novos valores variando levemente os dados anteriores, simulando a evolução dos indicadores.
    - :information_source: **Detalhes:** Trata tanto métricas gerais (receita, custo, lucro, etc.) quanto específicas de segmentos (ex.: taxa de ocupação e RevPAR para "Hotelaria"; taxa de evasão para "Educação"; tempo médio de atendimento para "Saúde"/"Hospital"; etc.).
    - :warning: Possui verificações para valores `None`, evitando erros em operações aritméticas.

  - **`gerar_dados_com_outliers(dados, probabilidade_outlier=0.01)`**  
    - :warning: **Propósito:** Com uma probabilidade definida, aplica outliers a certos campos numéricos.
    - :arrow_right: Seleciona aleatoriamente um índice numérico e multiplica o valor por um fator (entre 0.5 e 2.0).
    - :arrow_right: Ajusta os valores para garantir que não fiquem abaixo de limites mínimos ou acima de máximos.

  - **Função Auxiliar: `_safe_randint(a, b)`**  
    - :1234: **Propósito:** Garante que os limites passados para `random.randint` sejam convertidos para inteiros.
    - :arrow_right: Converte os limites, inverte a ordem se necessário, evitando erros de tipo (por exemplo, quando os limites forem floats).

---

### :sparkles: **main.py**

- **Objetivo:**  
  Orquestrar a geração dos dados sintéticos e salvar o dataset resultante em um arquivo CSV.

- **Passo a Passo das Funcionalidades:**
  - **Processamento de Argumentos:**  
    - :keyboard: Utiliza bibliotecas (por exemplo, `argparse`) para processar parâmetros fornecidos na linha de comando.
    - :arrow_right: Permite configurar:
      - O número de registros a serem gerados (`--registros`).
      - Os segmentos de mercado (`--segmentos`).
      - O intervalo de datas para os registros (`--data_inicio` e `--data_fim`).
      - A probabilidade de aplicação de outliers (`--outliers`).
      - O nome do arquivo de saída (`--arquivo_saida`).
  
  - **Integração com `geradores.py`:**  
    - :gear: Importa e utiliza as funções de `geradores.py` para criar os dados.
    - :arrow_right: Gera os dados de acordo com os segmentos informados, aplicando a lógica de autocorrelação (quando aplicável).
  
  - **Salvamento dos Dados:**  
    - :floppy_disk: Após a geração, os dados são exportados para um arquivo CSV.
    - :arrow_right: O arquivo é salvo com um cabeçalho e os registros gerados, facilitando análises posteriores.

---

### :sparkles: **util.py**

- **Objetivo:**  
  Fornecer funções utilitárias para a manipulação de arquivos CSV.

- **Funções Principais:**
  - **`criar_arquivo_csv(nome_arquivo, cabecalho, dados)`**  
    - :page_facing_up: **Propósito:** Cria um arquivo CSV com os dados fornecidos.
    - :arrow_right: Abre o arquivo em modo de escrita, com codificação UTF-8 e tratamento adequado de quebras de linha.
    - :arrow_right: Escreve a linha de cabeçalho seguida pelas linhas de dados.
    - :information_source: **Utilidade:** Facilita a exportação dos datasets gerados para análise e integração com outras ferramentas.

---

## :memo: Considerações Finais

- **Modularidade:**  
  Cada módulo (geradores.py, main.py, util.py) possui responsabilidades bem definidas, facilitando a manutenção e possíveis extensões do projeto.

- **Robustez:**  
  O tratamento de valores `None` e a conversão segura de limites para inteiros garantem que o script não quebre mesmo quando novos segmentos são adicionados ou quando os dados anteriores não estão completos.

- **Flexibilidade:**  
  O sistema permite a inclusão de novos segmentos sem causar erros, bastando que os campos específicos para esses segmentos sejam tratados ou deixados como valores padrão (por exemplo, `None`).

- **Aplicação:**  
  Este conjunto de scripts foi desenvolvido para gerar datasets sintéticos que podem ser utilizados em testes, simulações e análises em projetos de Business Intelligence e Data Analytics.

Esperamos que este guia ajude a esclarecer o funcionamento interno dos scripts e auxilie quem for trabalhar no projeto! 🚀

## Outras explicações - A seguir está uma versão completa e refatorada do arquivo geradores.py

    1. Inclui tratamento para valores None em métricas específicas (segmentos).
    2. Faz conversão de limites para inteiro antes de chamar random.randint(...), evitando o erro TypeError: 'float' object cannot be interpreted as an integer.
    3. Mantém a lógica de autocorrelação para gerar dados consistentes ao longo do tempo.

O que foi alterado (principais pontos)

    1. Função _safe_randint(a, b):
        Converte a e b em int e inverte se a > b.
        Garante que random.randint() receba limites inteiros, evitando o erro 'float' object cannot be interpreted as an integer'.

    2. Locais com random.randint(...):
        Agora usam _safe_randint(...), ou convertem explicitamente os valores de dados_anteriores[...] para inteiro.
        Por exemplo, impressoes, leads_gerados, vendas_por_vendedor, numero_avaliacoes, nivel_estoque etc.

    3. Tratamento de None:
        Se dados_anteriores[...] estiver None, definimos um valor padrão ou simplesmente geramos algo novo.
        Evita “TypeError” ao fazer None - 10.

    4. Mantido o resto da lógica (autocorrelação, outliers, etc.) inalterado, exceto por ajustes de conversão para inteiro e checagens de limites.

Com essas modificações, o script passa a gerar dados de forma consistente, mesmo que surjam valores decimais nos campos, sem quebrar no randint.

## Perguntas

1. Se informado no script de execução segmentos que não estejam pré-configurados, o script quebrará??

    o script não vai quebrar se você incluir segmentos que não estão tratados especificamente no código. Ele simplesmente não vai entrar nos trechos if/else específicos de cada segmento (por exemplo, não vai gerar taxa_ocupacao se não for "Hotelaria", etc.).

    O que acontece internamente é que, se o segmento não bater em nenhum if segmento == ... ou if segmento in [...], as métricas específicas daquele segmento serão definidas como None ou valores padrão (normalmente 0.0, caso seja numérico). Mas as demais métricas gerais (receita, custo, clientes etc.) ainda serão geradas sem problemas.

    Portanto, o script vai rodar normalmente com segmentos como "Aviação", "Finanças", "Metalurgia", "Automobilismo", etc. Você só não terá os cálculos extras (como RevPAR, taxa_evasao, tempo_medio_atendimento, etc.) que são feitos para segmentos pré-definidos.

2. Quais segmentos pré-definidos no script?

    No código há alguns segmentos que recebem tratamentos específicos para determinadas métricas. De forma resumida, os segmentos "pré-definidos" ou tratados de forma diferenciada são:

        Varejo e Indústria
            Geram métricas como categoria_produto, quantidade_produtos, nível de estoque, entre outros.

        Serviços, TI e SaaS
            Definem plano (para TI, Serviços, SaaS), e para TI e SaaS há também métricas de receita recorrente (MRR/ARR).
            Além disso, se o segmento for TI (ou incluir "SaaS"), influenciam a geração de tipo_serviço e métricas de uso (como usuários ativos e funcionalidade mais usada).

        Hotelaria
            Tem métricas específicas como taxa de ocupação e RevPAR.

        Educação
            É o segmento onde é calculada a taxa de evasão.

        Saúde e Hospital
            Geram a métrica tempo médio de atendimento.

    Além desses, no gerar_dados_gerais há referências a outros segmentos para definir o tipo de serviço, como Consultoria e Banco (usados na escolha do tipo_serviço).
    Também é considerada a possibilidade de o segmento ser Aplicativo, que afeta a geração de métricas de uso do produto (como usuários ativos).

    Ou seja, os segmentos com tratamento específico no código são:

        Varejo
        Indústria
        Serviços
        TI
        SaaS
        Hotelaria
        Educação
        Saúde
        Hospital
        Aplicativo (para uso do produto)
        Consultoria e Banco (no contexto de definição do tipo de serviço)

    Se você usar segmentos que não se encaixem nesses casos (por exemplo, "Aviação", "Finanças", "Metalurgia", "Automobilismo"), o código não vai dar erro – ele simplesmente não aplicará os tratamentos especiais para esses segmentos, e os campos específicos relacionados a eles (como RevPAR, taxa de evasão, etc.) ficarão como None ou serão gerados com valores padrão.

## Colunas do CSV criadas pelo script

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
