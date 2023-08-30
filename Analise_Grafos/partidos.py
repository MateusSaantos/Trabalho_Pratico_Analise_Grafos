import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

#Essa é a função para interagir com o usuario
def funcao_obter_filtro_usuario():
    ano = input("Digite o ano que deseja visualizar os dados: ")

    escolha_partidos = input("Deseja buscar partidos específicos (1) ou todos (2)? ")

    if escolha_partidos == "1":
        num_partidos = int(input("Quantos partidos deseja buscar? "))
        partidos_selecionados = []
        for i in range(num_partidos):
            partido = input(f"Digite o nome do partido {i+1}: ")
            partidos_selecionados.append(partido)
        
        threshold = input("Qual o Threshold deseja considerar? ")  
        return ano, partidos_selecionados, threshold
    
    elif escolha_partidos == "2":
        todos_partidos = "datasets/politicians" + ano + ".txt"
        partidos_sem_duplicata = obter_partidos_do_arquivo(todos_partidos)
        print(partidos_sem_duplicata)
        threshold = input("Qual o Threshold deseja considerar? ")  
        return ano, partidos_sem_duplicata, threshold  # Retorna o vetor vazio
    else:
        print("Opção inválida.")
        return None, None, None
    
#-------------------------------------------------------------------------------------

def obter_partidos_do_arquivo(nome_arquivo):
    partidos_sem_duplicata = set()  
    
    with open(nome_arquivo, 'r', encoding='utf-8-sig') as file:
        for linha in file:
            elementos = linha.strip().split(';')
            if len(elementos) >= 2:
                partidos_sem_duplicata.add(elementos[1])  
    
    return list(partidos_sem_duplicata)
  

#-------------------------------------------------------------------------------------
    
def funcao_normalizacao(partidos_selecionados, ano, threshold):

    grafo_threshold = nx.Graph()
    grafo_normal = nx.Graph()
    deputados = []
    arquivo_politician = "datasets/politicians" + ano + ".txt"
    arquivo_grafo = "datasets/graph" + ano + ".txt"
    partido = {}
    chave_remove = []

    with open(arquivo_politician, 'r', encoding='utf-8') as file:
        nome_candidato = []
        votos = {}

        x = file.readline()
        while x:
            controle = x.strip().split(';')
            if controle[1] in partidos_selecionados:
                nome_candidato.append(controle[0])
                partido[controle[0]] = controle[1]
                votos[controle[0]] = int(controle[2])
            x = file.readline()

    with open(arquivo_grafo, 'r', encoding='utf-8') as file:
        x = file.readline()
        while x:
            controle = x.strip().split(';')
            if controle[0] in nome_candidato and controle[1] in nome_candidato:
                peso = int(controle[2]) / min(votos[controle[0]], votos[controle[1]])
                grafo_normal.add_edge(controle[0], controle[1], weight=peso)
                grafo_threshold.add_edge(controle[0], controle[1], weight=1 - peso)
                if peso < float(threshold):
                    grafo_threshold.remove_edge(controle[0], controle[1])
                    deputados.append(controle[0])
            x = file.readline()

    betweenness = nx.betweenness_centrality(grafo_threshold)
    funcao_criacao_grafico(betweenness, deputados)
    plotagem(grafo_threshold, partidos_selecionados, partido)
    generate_heatmap(betweenness, deputados)

#-------------------------------------------------------------------------------

def funcao_criacao_grafico(betweenness, deputados): 
    fig, ax = plt.subplots() 
  
    centralidade = [] 
  
    for deputado in deputados: 
        centralidade.append(betweenness[deputado]) 
  
    bar_labels = 'green' 
    bar_colors = 'red' 
  
    ax.bar(deputados, centralidade, label=bar_labels, color=bar_colors) 
  
    ax.set_ylabel('Betweenness') 
    ax.set_xlabel('Deputados') 
    ax.set_title('Centralidade') 
  
    plt.xticks(rotation=45, ha="right", fontsize=3) 
    plt.tight_layout() 
  
    plt.savefig("representacao_grafico.png", dpi=140, bbox_inches='tight')

#-----------------------------------------------------------------------------------------

def plotagem(grafo, partidos, partido_deputado):
    cores_hex_profissionais = [
        '#1f77b4',
        '#ff7f0e',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf'
    ]
    
    layout = nx.spring_layout(grafo, seed=42)
    
    plt.figure(figsize=(10, 8))
    
    node_colors = [cores_hex_profissionais[partidos.index(partido_deputado[deputado])] for deputado in grafo.nodes()]
    
    nx.draw(
        grafo,
        pos=layout,
        with_labels=True,
        node_size=600,
        node_color=node_colors,
        font_size=6,  # Reduzindo o tamanho da fonte
        font_color='black',
        font_weight='bold',
        edge_color='gray',
        width=0.5,
        alpha=0.8,
    )
    
    plt.title('Grafo de Representantes', fontsize=16)
    plt.savefig("representacao_plotagem.png", dpi=300, bbox_inches='tight')
    #plt.show()

#-------------------------------------------------------------------------------------------------

def generate_heatmap(betweenness, deputados):
    correlation_matrix = np.zeros((len(deputados), len(deputados)))

    for i, deputado_1 in enumerate(deputados):
        for j, deputado_2 in enumerate(deputados):
            correlation_matrix[i, j] = abs(betweenness[deputado_1] - betweenness[deputado_2])

    fig, ax = plt.subplots()
    cax = ax.matshow(correlation_matrix, cmap='coolwarm')
    fig.colorbar(cax)

    ax.set_xticks(np.arange(len(deputados)))
    ax.set_yticks(np.arange(len(deputados)))
    ax.set_xticklabels(deputados, rotation=45, ha="right", fontsize=10)
    ax.set_yticklabels(deputados, fontsize=10)

    plt.title('Correlacao Heatmap')
    plt.tight_layout()
    plt.savefig("heatmap.png", dpi=140, bbox_inches='tight')
    #plt.show()
