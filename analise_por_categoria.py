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

print(car)
q_is = np.array(list(arquivos.keys()))[3:]  # Convertendo as chaves para um array
print(q_is)
#car['area_rural'] = car.geometry.area
# Plotando (se definido como True)
plotar=True


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Inicializar um dicionário para armazenar os resultados organizados
resultados_cidade = {}
intersect={}
# Reprojetar geometria da cidade para uma CRS projetada (e.g., UTM zone 23S)
# Ajuste o EPSG conforme sua região (exemplo: EPSG:32723 para UTM Zona 23S)
crs_proj = 'EPSG:32723'  # Substitua pelo CRS adequado para sua região


resultados_categoria = {}
from shapely.ops import unary_union

for dset in q_is:
    print(f"Processando dataset: {dset}")
    
    # Encontrar interseções já calculadas
    intersect[dset] = find_intersections(car, datasets[dset])
    intersect[dset]['overlap_area'] = intersect[dset]['intersection_area']
    
#    print(intersect[dset].head())
    
    
    # Criar dicionário para armazenar resultados agregados por property_id

     
    for idx, row in datasets[dset].iterrows():
        uc__id=row["id"]
       # print(row)
        intersects = intersect[dset][intersect[dset]['uc_id'] == row["id"]]

        collapsed = intersects.dissolve().reset_index()
        collapsed["geometry"] = collapsed["geometry"].apply(unary_union)
        
    
        try :
            a=np.sum(collapsed.geometry.area*111*110.8)
        except:
            a=0
        
        resultados_categoria[uc__id] = {}
        #print(intersect)
        resultados_categoria[uc__id] = {
                "Dataset": dset,
                "Nome":row["name"],
                "unit_id": uc__id,
                "Área_Total": row.geometry.area*111*110.8,
                "Área sobreposta com CAR": a,
                "CARs na interseção": len(intersects)
            }
        

    # Calcular percentual de sobreposição
    for prop_id, data in resultados_categoria.items():
        data["Percentual sobreposto"] = (data["Área sobreposta com CAR"] / data["Área_Total"]) * 100 if data["Área_Total"] > 0 else 0


# Converter resultados para DataFrame e salvar
df_resultados = pd.DataFrame.from_dict(resultados_categoria, orient='index')
df_resultados.to_csv('Resultados/resultados_por_categoria.csv', encoding='utf-8')

i=0



cores = ["blue", "yellow", "orange", "pink", "purple"]
plotar=False
    
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

if(plotar):

    # Supondo que 'arquivos' e 'datasets' já estejam definidos
    fig, ax = plt.subplots(figsize=(30, 16), dpi=100)

    uf.plot(ax=ax, color='white', edgecolor='black', linewidth=1, alpha=1, figsize=(25, 12))
    municipios.plot(ax=ax, color='white', edgecolor='black', linewidth=0.2, alpha=1, figsize=(30, 16))

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
