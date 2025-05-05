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
plotar=False


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Inicializar um dicionário para armazenar os resultados organizados
resultados_cidade = {}
intersect={}
# Reprojetar geometria da cidade para uma CRS projetada (e.g., UTM zone 23S)
# Ajuste o EPSG conforme sua região (exemplo: EPSG:32723 para UTM Zona 23S)
crs_proj = 'EPSG:32723'  # Substitua pelo CRS adequado para sua região


resultados_prop = {}

for dset in q_is:
    print(f"Processando dataset: {dset}")
    
    # Encontrar interseções já calculadas
    try:
        intersect[dset] = find_intersections(car, datasets[dset])
        intersect[dset]['overlap_area'] = intersect[dset]['intersection_area']
        
    #    print(intersect[dset].head())
        
        
        # Criar dicionário para armazenar resultados agregados por property_id

        
        for idx, row in car.iterrows():
            #print(row)
            prop_id=row["cod_imovel"]
            if prop_id not in resultados_prop:
                
                
                resultados_prop[prop_id] = {}
        # print(row)
            #print(intersect[dset])
            #print(car)
            intersect[dset]["prop_id"]=intersect[dset]["property_id"]
            intersects = intersect[dset][intersect[dset]['prop_id'] == row["cod_imovel"]]
            #print("found")
            #print(intersects)
            
            #print(intersects)
            #print(row)
            resultados_prop[prop_id].update({
                    "CAR": row["cod_imovel"],
                    "cond":row["des_condic"],
                    "cidade":row["municipio"],
                    
                    "Área_Total": row.geometry.area*111*110.8,
                    f"Área CAR sob {dset}": np.sum(intersects.geometry.area*111*110.8),
                    f"PC CAR sob {dset}": 100*np.sum(intersects.geometry.area*111*110.8)/(row.geometry.area*111*110.8),
                    
                })
    except:
        for idx, row in car.iterrows():
            #print(row)                 
            prop_id=row["cod_imovel"]

            if prop_id not in resultados_prop:
                
                
                resultados_prop[prop_id] = {}
            #print(intersects)
            #print(row)
            resultados_prop[prop_id].update({
                
                    "CAR": row["cod_imovel"],
                    "cond":row["des_condic"],
                    "cidade":row["municipio"],
                    
                    "Área_Total": row.geometry.area*111*110.8,
                    f"Área CAR sob {dset}": 0,
                    f"PC CAR sob {dset}": 0,
                    
                })

# Converter resultados para DataFrame e salvar
df_resultados = pd.DataFrame.from_dict(resultados_prop, orient='index')
df_resultados.to_csv('Resultados/resultados_por_car.csv', encoding='utf-8')

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
