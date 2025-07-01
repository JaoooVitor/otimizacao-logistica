import matplotlib.pyplot as plt
import pandas as pd
from utils.grafo_utils import (
    carregar_grafo,
    tornar_grafo_bidirecional,
    aplicar_restricoes,
    aplicar_custos_extras,
)
from utils.grafo_completo import gerar_grafo_completo
from algoritmos.aco import ACO
from algoritmos.genetico import AlgoritmoGenetico
from utils.mapa_visualizacao import (
    gerar_mapa_comparativo,
    gerar_mapa_multirotas
)

def gerar_grafico_comparativo():
    df = pd.read_csv("tabela_comparativa.csv")

    algoritmos = df["Algoritmo"]
    distancia_base = df["Distância Base"]
    custo_extra = df["Custo Extra"]
    custo_total = df["Custo Total"]

    bar_width = 0.2
    index = range(len(algoritmos))

    plt.figure(figsize=(10, 6))
    plt.bar(index, distancia_base, bar_width, label="Distância Base")
    plt.bar([i + bar_width for i in index], custo_extra, bar_width, label="Custo Extra")
    plt.bar([i + bar_width*2 for i in index], custo_total, bar_width, label="Custo Total")

    plt.xlabel("Algoritmo")
    plt.ylabel("Valor")
    plt.title("Comparação de Métricas: ACO vs Genético")
    plt.xticks([i + bar_width for i in index], algoritmos)
    plt.legend()
    plt.tight_layout()
    plt.savefig("grafico_comparativo.png")
    plt.close()
    print("📊 Gráfico comparativo salvo como grafico_comparativo.png")

def gerar_html_tabela_comparativa():
    df = pd.read_csv("tabela_comparativa.csv")

    html = """
    <html>
    <head>
        <meta charset=\"UTF-8\">
        <title>Tabela Comparativa - ACO e GA</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 30px;
                background-color: #f9f9f9;
            }
            h2, h3 {
                text-align: center;
                margin-top: 40px;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                background-color: white;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }
            th, td {
                border: 1px solid #ccc;
                padding: 10px 15px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            img {
                display: block;
                margin: 40px auto;
                max-width: 90%;
            }
        </style>
    </head>
    <body>
        <h2>Tabela Comparativa - ACO x Algoritmo Genético</h2>
        <table>
            <tr>
                <th>Algoritmo</th>
                <th>Distância Base</th>
                <th>Custo Extra</th>
                <th>Custo Total</th>
                <th>Tempo Execução (s)</th>
                <th>Iterações/Formigas</th>
                <th>Melhor Rota</th>
            </tr>
    """

    for _, row in df.iterrows():
        html += f"""
        <tr>
            <td>{row['Algoritmo']}</td>
            <td>{row['Distância Base']}</td>
            <td>{row['Custo Extra']}</td>
            <td>{row['Custo Total']}</td>
            <td>{row['Tempo Execução (s)']}</td>
            <td>{row['Iterações/Formigas']}</td>
            <td>{row['Melhor Rota']}</td>
        </tr>
        """

    html += """
        </table>
        <h3>Gráfico Comparativo</h3>
        <img src=\"grafico_comparativo.png\" alt=\"Gráfico Comparativo\">
    </body>
    </html>
    """

    with open("tabela_comparativa_render.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("📄 Tabela HTML com gráfico gerada com sucesso: tabela_comparativa_render.html")

def main():
    print("\n=== OTIMIZAÇÃO DE ROTAS — ALTO PARANAÍBA ===")

    grafo = carregar_grafo('data/grafo.json')
    grafo = tornar_grafo_bidirecional(grafo)

    print("\nInforme as estradas bloqueadas no formato: Cidade1-Cidade2")
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

    print("\nInforme custos extras no formato: Cidade1-Cidade2-Custo")
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

    grafo_restrito = aplicar_restricoes(grafo, estradas_bloqueadas)
    grafo_com_custos = aplicar_custos_extras(grafo_restrito, custos_extras)
    grafo_completo = gerar_grafo_completo(grafo_com_custos)

    print("\n>>> Executando ACO...")
    aco = ACO(grafo_completo, num_formigas=50, num_iteracoes=500)
    resultado_aco = aco.executar()

    print("\n>>> Executando Algoritmo Genético...")
    ga = AlgoritmoGenetico(grafo_completo, tamanho_populacao=300, taxa_mutacao=0.02, num_geracoes=500)
    resultado_ga = ga.executar()

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
        ("ACO", resultado_aco, 200),
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
    gerar_grafico_comparativo()
    gerar_html_tabela_comparativa()

    print("\n=== TABELA COMPARATIVA ===")
    print(df)

    # 🗺️ Mapas
    gerar_mapa_comparativo(
        resultado_aco['melhor_rota'],
        resultado_ga['melhor_rota'],
        estradas_bloqueadas,
        nome_arquivo="mapa_comparativo.html"
    )

    gerar_mapa_multirotas(
        resultado_aco['top3_rotas'],
        estradas_bloqueadas,
        nome_arquivo="mapa_aco_top3.html",
        algoritmo="ACO"
    )

    gerar_mapa_multirotas(
        resultado_ga['top3_rotas'],
        estradas_bloqueadas,
        nome_arquivo="mapa_genetico_top3.html",
        algoritmo="Genético"
    )

if __name__ == "__main__":
    main()
