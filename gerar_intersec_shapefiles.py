import geopandas as gpd
import matplotlib.pyplot as plt
from load_data import GeoDataLoader
from utils import find_intersections
import numpy as np
import matplotlib.patches as mpatches
import pandas as pd
# Carregar o arquivo shapefile
import os
arquivos = {
        "car": "dados/PARA/CAR/AREA_IMOVEL_1.shp",
        "municipios": "dados/PARA/Municipios/PA_Municipios_2023.shp",
        "uf": "dados/PARA/UF/PA_UF_2023.shp",
                "UCs": "dados/PARA/UCs/cat60_protected_area_WGS84_v2.shp",

        "Assen.": "dados/PARA/Assentamentos/cat63_settlements_WGS84.shp",
        "Quil.": "dados/PARA/Quilombolas/cat62_quilombola_WGS84.shp",
       
       
        "Agua": "dados/PARA/Agua/geoft_bho_massa_dagua_v2019.shp",
    
        "TIs": "dados/PARA/TIs/cat61_indigenous_territories_WGS84.shp",
}
datasets = GeoDataLoader().load_all(arquivos)
uf = datasets.get("uf")
municipios = datasets.get("municipios")
car = datasets.get("car")
print(car.columns)
print(car["des_condic"].head())
#car = car[car['des_condic'].str.startswith("Analisado sem")]


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
    print(datasets[dset].columns)
    
    print(datasets[dset].head())
    # Encontrar interseções já calculadas
   # print(car)
    print(datasets[dset].head())
 
    intersect[dset] = find_intersections(car, datasets[dset])
    
    print(intersect[dset].head())   
    intersect[dset]['overlap_area'] = intersect[dset]['intersection_area']
    

    
    
    os.makedirs(f'Resultados/{dset}_intersect/', exist_ok=True)
    intersect[dset].to_file(f'Resultados/{dset}_intersect/shapes_intersect.shp')
            
    #
