import geopandas as gpd
import matplotlib.pyplot as plt
from load_data import GeoDataLoader
from utils import find_intersections
import numpy as np
import matplotlib.patches as mpatches
import pandas as pd
# Carregar o arquivo shapefile

arquivos = {
        "car": "dados/PARA/CAR/AREA_IMOVEL_1.shp",
        "municipios": "dados/PARA/Municipios/PA_Municipios_2023.shp",
        "uf": "dados/PARA/UF/PA_UF_2023.shp",
        "Assen.": "dados/PARA/Assentamentos/cat63_settlements_WGS84.shp",
       # "fpnds": "dados/PARA/FPND/florestas_publicas_naodestinadas.shp",
        "Quil.": "dados/PARA/Quilombolas/cat62_quilombola_WGS84.shp",
        "TIs": "dados/PARA/TIs/cat61_indigenous_territories_WGS84.shp",
        "UCs": "dados/PARA/UCs/cat60_protected_area_WGS84_v2.shp",
}
datasets = GeoDataLoader().load_all(arquivos)

uf = datasets.get("uf")
municipios = datasets.get("municipios")
car = datasets.get("car")
q_is = np.array(list(arquivos.keys()))[3:]  # Convertendo as chaves para um array
print(q_is)
car['area_rural'] = car.geometry.area
# Plotando (se definido como True)
plotar=True
if(plotar):

    # Supondo que 'arquivos' e 'datasets' já estejam definidos
    fig, ax = plt.subplots(figsize=(30, 16), dpi=100)

    uf.plot(ax=ax, color='white', edgecolor='black', linewidth=1, alpha=1, figsize=(25, 12))
    municipios.plot(ax=ax, color='white', edgecolor='black', linewidth=0.2, alpha=1, figsize=(30, 16))

    cores = ["blue", "yellow", "orange", "pink", "purple"]
    i = 0

    # Criar uma lista para armazenar os "proxy artists" para a legenda
    proxy_artists = []

    # Plotar cada dataset usando o GeoPandas
    for dset in q_is:
        print(dset)
        # Plotar cada dataset
        datasets[dset].plot(ax=ax, edgecolor='black', linewidth=0, color=cores[i], alpha=0.6)
        
        # Criar um "proxy artist" (para a legenda) que se parece com o gráfico
        proxy = mpatches.Patch(color=cores[i], label=dset)
        proxy_artists.append(proxy)
        i += 1

    # Plotar o dataset 'car' com sua própria legenda
    car_plot_obj = car.plot(ax=ax, color='green', edgecolor='black', linewidth=0.001, alpha=0.1)

    # Criar um "proxy artist" para 'Car Data'
    car_proxy = mpatches.Patch(color='green', label='car')
    proxy_artists.append(car_proxy)

    # Criar a legenda manualmente usando os "proxy artists"
    ax.legend(handles=proxy_artists)

    # Ajustar o layout para evitar sobreposição e garantir que a legenda seja visível
    plt.tight_layout()

    # Salvar o gráfico em um arquivo
    plt.savefig("Resultados/plot_all.pdf", bbox_inches='tight')  # Garante que a legenda não será cortada

    # Opcionalmente, você pode exibir o gráfico (se estiver rodando em um ambiente interativo)
    # plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Inicializar um dicionário para armazenar os resultados organizados
resultados_cidade = {}
intersect={}
# Reprojetar geometria da cidade para uma CRS projetada (e.g., UTM zone 23S)
# Ajuste o EPSG conforme sua região (exemplo: EPSG:32723 para UTM Zona 23S)
crs_proj = 'EPSG:32723'  # Substitua pelo CRS adequado para sua região

# Processar os datasets
for dset in q_is:
    print(f"Processando dataset: {dset}")
    
    # Encontrar as interseções para o dataset atual
    intersect[dset] = find_intersections(car, datasets[dset])
    intersect[dset]['overlap_area'] = intersect[dset].geometry.area

    print(intersect[dset].head())

    # Loop por cada cidade no conjunto de cidades
    for _, city_row in municipios.iterrows():
        nome_cidade = city_row['NM_MUN']  # Nome da cidade
        geometria_cidade = city_row.geometry  # Reprojetar geometria da cidade
        area_cidade = geometria_cidade.area  # Área total da cidade

        # Encontrar a categoria ds dentro da cidade, incluindo sobreposições parciais
        categoria_ds_na_cidade = datasets[dset][datasets[dset].geometry.intersects(geometria_cidade)]

        # Agora precisamos calcular a área de sobreposição proporcional
        # Para cada UC que intersecta a cidade, calcular a área da sobreposição e atribuí-la
        area_categoria_ds_na_cidade = 0
        for _, row in categoria_ds_na_cidade.iterrows():
            uc_geom = row.geometry
            # Calcular a interseção da UC com a cidade
            intersection_geom = uc_geom.intersection(geometria_cidade)
            
            # Se houver uma interseção, calcule a área da interseção
            if intersection_geom.is_empty:
                continue

            # Somar a área da interseção
            area_categoria_ds_na_cidade += intersection_geom.area
        
        # Calcular a área das propriedades rurais dentro da cidade
        car_na_cidade=car[car.geometry.intersects(geometria_cidade)]
        area_rural_na_cidade = 0


 # Para cada UC que intersecta a cidade, calcular a área da sobreposição e atribuí-la
        area_rural_na_cidade = 0
        for _, row in car_na_cidade.iterrows():
            car_geom = row.geometry
            # Calcular a interseção de CAR com a cidade
            intersection_geom = car_geom.intersection(geometria_cidade)
            
            # Se houver uma interseção, calcule a área da interseção
            if intersection_geom.is_empty:
                continue

            # Somar a área da interseção
            area_rural_na_cidade += intersection_geom.area







        # Encontrar as interseções das propriedades rurais na cidade com UCs
        sobreposicoes_na_cidade = intersect[dset][intersect[dset].geometry.intersects(geometria_cidade)]

        # Clipping the intersection geometries to be within the city boundary
        sobreposicoes_na_cidade['geometry'] = sobreposicoes_na_cidade['geometry'].apply(lambda x: x.intersection(geometria_cidade))

        # Recalcular a área das interseções
        area_sobreposicao_na_cidade = sobreposicoes_na_cidade['geometry'].area.sum()

        # Calcular as porcentagens
        percent_cidade_rural = (area_rural_na_cidade / area_cidade) * 100 if area_cidade > 0 else 0
        percent_sobreposicao_rural = (area_sobreposicao_na_cidade / area_rural_na_cidade) * 100 if area_rural_na_cidade > 0 else 0
        percent_categoria_ds = (area_categoria_ds_na_cidade / area_cidade) * 100 if area_cidade > 0 else 0

        # Adicionar os resultados da cidade atual aos resultados do dataset
        if nome_cidade not in resultados_cidade:
            resultados_cidade[nome_cidade] = {}
        
        resultados_cidade[nome_cidade].update({
            f"Area Cidade": area_cidade,
            f"Car Registros":len(car_na_cidade),
            f"CAR - Area": area_rural_na_cidade,
            f"Percentual CAR": percent_cidade_rural,
            f"{dset} - Area CAT ": area_categoria_ds_na_cidade,  # Adicionando a área da categoria ds
            f"{dset} - Area CAR sob CAT": area_sobreposicao_na_cidade,
            f"{dset} - N CAR sob CAT": len(sobreposicoes_na_cidade),
            f"{dset} - Pc CAR sob CAT": percent_sobreposicao_rural,
        })

    # Opcional: Criar um gráfico para o dataset atual

i=0
    
if plotar:
    for dset in q_is:
        fig, ax = plt.subplots(figsize=(30, 16), dpi=100)
        uf.plot(ax=ax, color='white', edgecolor='black', linewidth=1, alpha=1)
        municipios.plot(ax=ax, color='white', edgecolor='black', linewidth=1, alpha=1)

        proxy_artists = []

        datasets[dset].plot(ax=ax, edgecolor='black', linewidth=0, color=cores[i], alpha=0.6)
        proxy = mpatches.Patch(color=cores[i], label=dset)
        proxy_artists.append(proxy)
        i += 1
        print(i)

        car_plot_obj = car.plot(ax=ax, color='green', edgecolor='black', linewidth=0.001, alpha=0.1)
        car_proxy = mpatches.Patch(color='green', label='car')
        proxy_artists.append(car_proxy)

        i_obj = intersect[dset].plot(ax=ax, color='red', edgecolor='black', linewidth=0.001, alpha=0.4)
        i_proxy = mpatches.Patch(color='red', label='interseções')
        proxy_artists.append(i_proxy)

        ax.legend(handles=proxy_artists)
        plt.tight_layout()

        plt.savefig(f"Resultados/plot_{dset}.png", bbox_inches='tight')

df_resultados = pd.DataFrame.from_dict(resultados_cidade, orient='index')
df_resultados.to_csv('resultados_por_cidade.csv', encoding='utf-8')


