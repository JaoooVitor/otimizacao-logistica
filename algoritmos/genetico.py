import random
import time


class AlgoritmoGenetico:
    def __init__(self, grafo, tamanho_populacao=50, taxa_mutacao=0.01, num_geracoes=100, origem="Patrocínio"):
        self.grafo = grafo
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.num_geracoes = num_geracoes
        self.origem = origem
        self.cidades = list(grafo.keys())
        self.cidades.remove(self.origem)

    def criar_rota(self):
        rota = self.cidades.copy()
        random.shuffle(rota)
        return [self.origem] + rota + [self.origem]

    def criar_populacao(self):
        return [self.criar_rota() for _ in range(self.tamanho_populacao)]

    def calcular_distancia(self, rota):
        distancia = 0
        for i in range(len(rota) - 1):
            origem = rota[i]
            destino = rota[i + 1]
            distancia += self.grafo[origem][destino]
        return distancia

    def rankear_rotas(self, populacao):
        return sorted(populacao, key=lambda x: self.calcular_distancia(x))

    def selecao(self, populacao_rankeada):
        return populacao_rankeada[:int(0.2 * self.tamanho_populacao)]

    def crossover(self, pai1, pai2):
        pai1_meio = pai1[1:-1]
        pai2_meio = pai2[1:-1]

        start = random.randint(0, len(pai1_meio) - 2)
        end = random.randint(start + 1, len(pai1_meio) - 1)

        filho_p1 = pai1_meio[start:end]
        filho_p2 = [cidade for cidade in pai2_meio if cidade not in filho_p1]

        filho = [self.origem] + filho_p2[:start] + filho_p1 + filho_p2[start:] + [self.origem]
        return filho

    def mutacao(self, rota):
        rota_meio = rota[1:-1]
        for i in range(len(rota_meio)):
            if random.random() < self.taxa_mutacao:
                j = random.randint(0, len(rota_meio) - 1)
                rota_meio[i], rota_meio[j] = rota_meio[j], rota_meio[i]
        return [self.origem] + rota_meio + [self.origem]

    def gerar_nova_geracao(self, populacao_atual):
        populacao_rankeada = self.rankear_rotas(populacao_atual)
        elite = self.selecao(populacao_rankeada)

        filhos = []
        while len(filhos) < self.tamanho_populacao - len(elite):
            pai1 = random.choice(elite)
            pai2 = random.choice(elite)
            filho = self.crossover(pai1, pai2)
            filho = self.mutacao(filho)
            filhos.append(filho)

        nova_geracao = elite + filhos
        return nova_geracao

    def executar(self):
        inicio = time.time()

        populacao = self.criar_populacao()
        melhor_rota = None
        melhor_distancia = float('inf')
        todas_rotas = []

        for geracao in range(self.num_geracoes):
            populacao = self.gerar_nova_geracao(populacao)
            populacao_rankeada = self.rankear_rotas(populacao)

            distancia_atual = self.calcular_distancia(populacao_rankeada[0])
            todas_rotas.extend([(ind, self.calcular_distancia(ind)) for ind in populacao_rankeada])

            if distancia_atual < melhor_distancia:
                melhor_rota = populacao_rankeada[0]
                melhor_distancia = distancia_atual

            print(f"Geração {geracao + 1}: Melhor distância = {melhor_distancia}")

        fim = time.time()
        tempo_execucao = fim - inicio

        # Filtrar 3 melhores rotas únicas
        rotas_unicas = {}
        for rota, dist in todas_rotas:
            chave = tuple(rota)
            if chave not in rotas_unicas or dist < rotas_unicas[chave]:
                rotas_unicas[chave] = dist

        top3 = sorted(rotas_unicas.items(), key=lambda x: x[1])[:3]

        return {
            "melhor_rota": top3[0][0],
            "distancia": top3[0][1],
            "tempo": tempo_execucao,
            "top3_rotas": [rota for rota, _ in top3]
        }
