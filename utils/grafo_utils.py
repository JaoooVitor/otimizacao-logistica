import json
import networkx as nx
import matplotlib.pyplot as plt


# Carregar grafo
def carregar_grafo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        grafo = json.load(arquivo)
    return grafo


# Tornar grafo bidirecional
def tornar_grafo_bidirecional(grafo):
    grafo_bidirecional = {}
    for cidade, vizinhos in grafo.items():
        if cidade not in grafo_bidirecional:
            grafo_bidirecional[cidade] = {}
        for vizinho, distancia in vizinhos.items():
            grafo_bidirecional[cidade][vizinho] = distancia
            if vizinho not in grafo_bidirecional:
                grafo_bidirecional[vizinho] = {}
            grafo_bidirecional[vizinho][cidade] = distancia
    return grafo_bidirecional


# Aplicar restrições (bloquear estradas)
def aplicar_restricoes(grafo, estradas_bloqueadas):
    grafo_restrito = json.loads(json.dumps(grafo))  # Copia profunda
    for cidade1, cidade2 in estradas_bloqueadas:
        if cidade2 in grafo_restrito.get(cidade1, {}):
            del grafo_restrito[cidade1][cidade2]
        if cidade1 in grafo_restrito.get(cidade2, {}):
            del grafo_restrito[cidade2][cidade1]
    return grafo_restrito


# Aplicar custos extras nas estradas
def aplicar_custos_extras(grafo, custos_extras):
    grafo_modificado = json.loads(json.dumps(grafo))  # Copia profunda
    for cidade1, cidade2, custo in custos_extras:
        if cidade2 in grafo_modificado.get(cidade1, {}):
            grafo_modificado[cidade1][cidade2] += custo
        if cidade1 in grafo_modificado.get(cidade2, {}):
            grafo_modificado[cidade2][cidade1] += custo
    return grafo_modificado


# Desenhar grafo (opcional)
def desenhar_grafo(grafo):
    G = nx.Graph()

    for cidade, vizinhos in grafo.items():
        for vizinho, distancia in vizinhos.items():
            G.add_edge(cidade, vizinho, weight=distancia)

    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Mapa das Cidades - Alto Paranaíba")
    plt.axis('off')
    plt.show()
