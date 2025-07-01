import folium
from folium.plugins import BeautifyIcon
from folium import Popup
import pandas as pd
from utils.coordenadas import coordenadas

def aplicar_offset(pontos, offset_lat=0, offset_lon=0):
    return [(lat + offset_lat, lon + offset_lon) for lat, lon in pontos]

def gerar_mapa_comparativo(rota_aco, rota_ga, estradas_bloqueadas, nome_arquivo="mapa_comparativo.html"):
    mapa = folium.Map(location=[-18.9, -47.2], zoom_start=8)

    cor_aco = 'red'
    cor_ga = 'blue'

    ordem_aco = {cidade: idx + 1 for idx, cidade in enumerate(rota_aco)}
    ordem_ga = {cidade: idx + 1 for idx, cidade in enumerate(rota_ga)}

    for cidade1, cidade2 in estradas_bloqueadas:
        try:
            ponto1 = coordenadas[cidade1]
            ponto2 = coordenadas[cidade2]
            folium.PolyLine(
                [ponto1, ponto2],
                color='black',
                weight=6,
                opacity=1,
                tooltip=f"Bloqueado: {cidade1} ↔ {cidade2}"
            ).add_to(mapa)
        except:
            print(f"Erro ao desenhar estrada bloqueada entre {cidade1} e {cidade2}")

    rotas = [rota_aco, rota_ga]
    cores = [cor_aco, cor_ga]
    nomes = ["ACO", "GA"]
    offsets = [(0.002, 0.002), (-0.002, -0.002)]

    for rota, cor, nome, (lat_off, lon_off) in zip(rotas, cores, nomes, offsets):
        pontos_originais = [coordenadas[c] for c in rota]
        pontos_offset = aplicar_offset(pontos_originais, lat_off, lon_off)
        folium.PolyLine(
            pontos_offset,
            color=cor,
            weight=5,
            opacity=0.7,
            tooltip=f'Rota {nome}'
        ).add_to(mapa)

    for cidade, (lat, lon) in coordenadas.items():
        popup_text = f"<b>{cidade}</b><br>"
        popup_text += f"Ordem ACO: {ordem_aco.get(cidade, 'N/A')}<br>"
        popup_text += f"Ordem GA: {ordem_ga.get(cidade, 'N/A')}"

        folium.Marker(
            location=(lat, lon),
            popup=Popup(popup_text, max_width=300),
            icon=BeautifyIcon(
                icon_shape='marker',
                border_color='darkgreen',
                text_color='white',
                background_color='green'
            )
        ).add_to(mapa)

    legenda_html = '''
     <div style="
     position: fixed;
     bottom: 50px;
     left: 50px;
     width: 200px;
     height: 180px;
     z-index:9999;
     background-color:white;
     border:2px solid grey;
     padding: 10px;
     font-size:14px;
     ">
     <b>Legenda</b><br>
     <i style="color:red;">&#9632;</i> Rota ACO<br>
     <i style="color:blue;">&#9632;</i> Rota GA<br>
     <i style="color:black;">&#9632;</i> Estrada Bloqueada<br>
     <i style="color:green;">&#9873;</i> Cidades<br>
     <br><b>Popup:</b><br>
     Ordem nas rotas (ACO e GA)
     <br>
     </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda_html))

    df = pd.read_csv("tabela_comparativa.csv")
    tabela_html = """
    <div style="
        position: fixed; 
        top: 50px; right: 50px; 
        width: 450px; 
        background-color: white;
        border: 2px solid grey;
        border-radius: 10px;
        padding: 10px;
        z-index:9999;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        font-size: 13px;">
        <h4 style="text-align:center; margin-top:0;">Tabela Comparativa</h4>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th>Algoritmo</th>
                <th>Distância Base</th>
                <th>Custo Extra</th>
                <th>Custo Total</th>
                <th>Tempo (s)</th>
                <th>Iterações</th>
            </tr>
    """
    for _, row in df.iterrows():
        tabela_html += f"""
            <tr>
                <td>{row['Algoritmo']}</td>
                <td>{row['Distância Base']}</td>
                <td>{row['Custo Extra']}</td>
                <td>{row['Custo Total']}</td>
                <td>{row['Tempo Execução (s)']}</td>
                <td>{row['Iterações/Formigas']}</td>
            </tr>
        """
    tabela_html += "</table></div>"
    mapa.get_root().html.add_child(folium.Element(tabela_html))
    mapa.save(nome_arquivo)
    print(f"Mapa salvo como {nome_arquivo}")

def gerar_mapa_multirotas(rotas, estradas_bloqueadas, nome_arquivo, algoritmo):
    mapa = folium.Map(location=[-18.9, -47.2], zoom_start=8)
    cores = ['red', 'blue', 'green']

    for cidade1, cidade2 in estradas_bloqueadas:
        try:
            ponto1 = coordenadas[cidade1]
            ponto2 = coordenadas[cidade2]
            folium.PolyLine(
                [ponto1, ponto2],
                color='black',
                weight=6,
                opacity=1,
                tooltip=f"Bloqueado: {cidade1} ↔ {cidade2}"
            ).add_to(mapa)
        except:
            print(f"Erro ao desenhar estrada bloqueada entre {cidade1} e {cidade2}")

    for idx, rota in enumerate(rotas):
        pontos_originais = [coordenadas[cidade] for cidade in rota]
        offset = 0.002 * (idx - 1)  # -0.002, 0, 0.002
        pontos = aplicar_offset(pontos_originais, offset, offset)
        folium.PolyLine(
            pontos,
            color=cores[idx % len(cores)],
            weight=5,
            opacity=0.7,
            tooltip=f"{algoritmo} - Rota #{idx + 1}"
        ).add_to(mapa)

    for cidade, (lat, lon) in coordenadas.items():
        folium.Marker(
            location=(lat, lon),
            icon=BeautifyIcon(
                icon_shape='marker',
                border_color='darkgreen',
                text_color='white',
                background_color='green'
            ),
            popup=cidade
        ).add_to(mapa)

    legenda_html = f'''
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 220px;
        height: 160px;
        z-index:9999;
        background-color:white;
        border:2px solid grey;
        padding: 10px;
        font-size:14px;
    ">
    <b>Legenda</b><br>
    <i style="color:red;">&#9632;</i> Rota #1<br>
    <i style="color:blue;">&#9632;</i> Rota #2<br>
    <i style="color:green;">&#9632;</i> Rota #3<br>
    <i style="color:black;">&#9632;</i> Estrada Bloqueada<br>
    </div>
    '''
    mapa.get_root().html.add_child(folium.Element(legenda_html))
    mapa.save(nome_arquivo)
    print(f"Mapa salvo como {nome_arquivo}")
