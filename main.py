from utils.grafo_utils import (
    carregar_grafo,
    tornar_grafo_bidirecional,
    aplicar_restricoes,
    aplicar_custos_extras,
)
from utils.grafo_completo import gerar_grafo_completo
from algoritmos.aco import ACO
from algoritmos.genetico import AlgoritmoGenetico
from utils.mapa_visualizacao import gerar_mapa_comparativo

import pandas as pd


def main():
    print("\n=== OTIMIZAÇÃO DE ROTAS — ALTO PARANAÍBA ===")

    # 🚩 Carregar grafo original
    grafo = carregar_grafo('data/grafo.json')
    grafo = tornar_grafo_bidirecional(grafo)

    # 🚧 Estradas bloqueadas
    print("\nInforme as estradas bloqueadas no formato: Cidade1-Cidade2")
    print("Exemplo: Patrocínio-Coromandel")
    print("Digite 'ok' quando terminar.\n")

    estradas_bloqueadas = []
    while True:
        entrada = input("Bloquear estrada (ou 'ok'): ").strip()

        if entrada.lower() == 'ok':
            break

        try:
            cidade1, cidade2 = entrada.split('-')
            cidade1 = cidade1.strip().title()
            cidade2 = cidade2.strip().title()

            estradas_bloqueadas.append((cidade1, cidade2))
            print(f"✅ Estrada {cidade1} ↔ {cidade2} bloqueada!")
        except:
            print("❌ Formato inválido. Use o formato: Cidade1-Cidade2")

    # 💸 Custos extras
    print("\nInforme custos extras no formato: Cidade1-Cidade2-Custo")
    print("Exemplo: Patrocínio-Coromandel-50")
    print("Digite 'ok' quando terminar.\n")

    custos_extras = []
    while True:
        entrada = input("Adicionar custo extra (ou 'ok'): ").strip()

        if entrada.lower() == 'ok':
            break

        try:
            cidade1, cidade2, custo = entrada.split('-')
            cidade1 = cidade1.strip().title()
            cidade2 = cidade2.strip().title()
            custo = float(custo.strip())

            custos_extras.append((cidade1, cidade2, custo))
            print(f"💰 Custo extra de {custo} aplicado na estrada {cidade1} ↔ {cidade2}")
        except:
            print("❌ Formato inválido. Use: Cidade1-Cidade2-Custo")

    # 🔧 Aplicar restrições e custos
    grafo_restrito = aplicar_restricoes(grafo, estradas_bloqueadas)
    grafo_com_custos = aplicar_custos_extras(grafo_restrito, custos_extras)
    grafo_completo = gerar_grafo_completo(grafo_com_custos)

    # 🐜 Executar ACO
    print("\n>>> Executando ACO...")
    aco = ACO(grafo_completo, num_formigas=30, num_iteracoes=100)
    resultado_aco = aco.executar()

    # 🧬 Executar GA
    print("\n>>> Executando Algoritmo Genético...")
    ga = AlgoritmoGenetico(grafo_completo, tamanho_populacao=200, taxa_mutacao=0.02, num_geracoes=500)
    resultado_ga = ga.executar()

    # 📊 Gerar tabela comparativa
    def calcular_custo_extra(rota):
        custo_extra = 0
        for i in range(len(rota) - 1):
            origem = rota[i]
            destino = rota[i + 1]

            custo_base = grafo_restrito.get(origem, {}).get(destino, 9999)
            custo_modificado = grafo_com_custos.get(origem, {}).get(destino, 9999)

            custo_extra += (custo_modificado - custo_base)
        return custo_extra

    resultados = []

    for nome_alg, resultado, iteracoes in [
        ("ACO", resultado_aco, 100),
        ("Genético", resultado_ga, 500)
    ]:
        custo_extra = calcular_custo_extra(resultado['melhor_rota'])
        distancia_base = resultado["distancia"] - custo_extra

        resultados.append({
            "Algoritmo": nome_alg,
            "Distância Base": distancia_base,
            "Custo Extra": custo_extra,
            "Custo Total": resultado["distancia"],
            "Tempo Execução (s)": round(resultado["tempo"], 2),
            "Iterações/Formigas": iteracoes,
            "Melhor Rota": ' → '.join(resultado["melhor_rota"])
        })

    df = pd.DataFrame(resultados)
    df.to_csv("tabela_comparativa.csv", index=False)

    print("\n=== TABELA COMPARATIVA ===")
    print(df)

    # 🗺️ Gerar mapa
    gerar_mapa_comparativo(
        resultado_aco['melhor_rota'],
        resultado_ga['melhor_rota'],
        estradas_bloqueadas=estradas_bloqueadas,
        nome_arquivo="mapa_comparativo.html"
    )


if __name__ == "__main__":
    main()
