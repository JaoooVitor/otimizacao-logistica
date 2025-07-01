import networkx as nx


def gerar_grafo_completo(grafo_original):
    G = nx.Graph()

    for cidade, vizinhos in grafo_original.items():
        for vizinho, distancia in vizinhos.items():
            G.add_edge(cidade, vizinho, weight=distancia)

    grafo_completo = {}
    for origem in grafo_original.keys():
        grafo_completo[origem] = {}
        for destino in grafo_original.keys():
            if origem != destino:
                try:
                    distancia = nx.shortest_path_length(G, origem, destino, weight='weight')
                    grafo_completo[origem][destino] = distancia
                except nx.NetworkXNoPath:
                    grafo_completo[origem][destino] = 9999  

    return grafo_completo
