import networkx as nx


def gerar_grafo_completo(grafo_original):
    G = nx.Graph()

    # Adiciona arestas existentes
    for cidade, vizinhos in grafo_original.items():
        for vizinho, distancia in vizinhos.items():
            G.add_edge(cidade, vizinho, weight=distancia)

    # Calcula menores distâncias entre todos os pares
    grafo_completo = {}
    for origem in grafo_original.keys():
        grafo_completo[origem] = {}
        for destino in grafo_original.keys():
            if origem != destino:
                try:
                    distancia = nx.shortest_path_length(G, origem, destino, weight='weight')
                    grafo_completo[origem][destino] = distancia
                except nx.NetworkXNoPath:
                    grafo_completo[origem][destino] = 9999  # Penaliza se não existir caminho

    return grafo_completo
