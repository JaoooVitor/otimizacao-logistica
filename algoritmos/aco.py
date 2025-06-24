import random
import time


class ACO:
    def __init__(self, grafo, num_formigas=20, num_iteracoes=100, alfa=1.0, beta=5.0, rho=0.5, q=100):
        self.grafo = grafo
        self.num_formigas = num_formigas
        self.num_iteracoes = num_iteracoes
        self.alfa = alfa  # Peso do feromônio
        self.beta = beta  # Peso da distância (heurística)
        self.rho = rho    # Taxa de evaporação
        self.q = q        # Quantidade de feromônio depositado

        # Inicializar feromônio nas arestas existentes
        self.feromonio = {}
        for cidade in grafo:
            self.feromonio[cidade] = {}
            for vizinho in grafo[cidade]:
                self.feromonio[cidade][vizinho] = 1.0  # Inicializa com 1.0

    def escolher_proxima(self, atual, visitados):
        vizinhos = self.grafo[atual]
        probabilidades = []
        soma = 0

        for vizinho in vizinhos:
            if vizinho not in visitados:
                tau = self.feromonio[atual][vizinho] ** self.alfa
                eta = (1 / self.grafo[atual][vizinho]) ** self.beta
                prob = tau * eta
                probabilidades.append((vizinho, prob))
                soma += prob

        if soma == 0:
            return None

        r = random.uniform(0, soma)
        acumulado = 0
        for vizinho, prob in probabilidades:
            acumulado += prob
            if acumulado >= r:
                return vizinho

        return probabilidades[-1][0]

    def executar(self, origem="Patrocínio"):
        melhor_rota = None
        melhor_distancia = float('inf')
        inicio = time.time()

        for iteracao in range(self.num_iteracoes):
            todas_rotas = []

            for _ in range(self.num_formigas):
                rota = [origem]
                while len(rota) < len(self.grafo):
                    proxima = self.escolher_proxima(rota[-1], rota)
                    if proxima is None:
                        break
                    rota.append(proxima)
                rota.append(origem)  # Retorna pra cidade inicial

                # Calcular distância da rota
                distancia = 0
                for i in range(len(rota) - 1):
                    cidade = rota[i]
                    destino = rota[i + 1]
                    if destino in self.grafo.get(cidade, {}):
                        distancia += self.grafo[cidade][destino]
                    else:
                        distancia += 9999  # Penalidade pra conexão inexistente

                todas_rotas.append((rota, distancia))

                if distancia < melhor_distancia:
                    melhor_rota = rota
                    melhor_distancia = distancia

            # Evaporação do feromônio
            for cidade in self.feromonio:
                for vizinho in self.feromonio[cidade]:
                    self.feromonio[cidade][vizinho] *= (1 - self.rho)

            # Depósito de feromônio nas rotas encontradas
            for rota, distancia in todas_rotas:
                for i in range(len(rota) - 1):
                    cidade = rota[i]
                    vizinho = rota[i + 1]
                    if vizinho in self.feromonio.get(cidade, {}):
                        self.feromonio[cidade][vizinho] += self.q / distancia

            print(f"Iteração {iteracao + 1}: Melhor distância até agora = {melhor_distancia}")

        fim = time.time()
        tempo_execucao = fim - inicio

        return {
            "melhor_rota": melhor_rota,
            "distancia": melhor_distancia,
            "tempo": tempo_execucao
        }
