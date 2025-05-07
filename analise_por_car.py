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
     #   "Agua": "dados/PARA/Agua/geoft_bho_massa_dagua_v2019.shp"
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
                    "data":row["dat_atuali"],
                    
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
                    "data":row["dat_atuali"],
                    
                    "Área_Total": row.geometry.area*111*110.8,
                    f"Área CAR sob {dset}": 0,
                    f"PC CAR sob {dset}": 0,
                    
                })

import geopandas as gpd
from shapely.strtree import STRtree

# Assuming 'car' is a GeoDataFrame

import pandas as pd
from shapely.strtree import STRtree

# Assuming 'car' is a GeoDataFrame
# Calculate the area of each property in hectares
car['total_area_ha'] = car.geometry.area * 111 * 110.8  # Approximate conversion to hectares

# Create a spatial index for faster intersection checks
spatial_index = STRtree(car.geometry)


# Iterate over each property and calculate contested areas
for idx, car_row in car.iterrows():
    current_car_geom = car_row.geometry
    car_id = car_row["cod_imovel"]
    total_area = car_row["total_area_ha"]

    # Query the spatial index for potential intersections
    potential_matches = [geom for geom in spatial_index.query(current_car_geom) if geom != current_car_geom]
    potential_intersections = car.iloc[potential_matches]
    # Calculate intersection areas with other properties
    contested_area =  sum(
        row.geometry.intersection(contested_row.geometry).area
        for _, contested_row in potential_intersections.iterrows())

    # Calculate contested area percentage
    contested_percentage = 100 * contested_area / total_area if total_area > 0 else 0

    # Store results in the dictionary
    resultados_prop[row["cod_imovel"]].update({
                
                    "CAR": row["cod_imovel"],
                    "cond":row["des_condic"],
                    "cidade":row["municipio"],
                    
                    "Área_Total": row.geometry.area*111*110.8,
                    
                    f"Área CAR sob car(ha)": contested_area*111*110.8,
                    f"PC CAR sob car": 100* contested_area / total_area if total_area > 0 else 0,
                    
                })


# Convert the resultados_prop dictionary to a DataFrame
df_resultados = pd.DataFrame.from_dict(resultados_prop, orient='index')

# Save the results to a CSV file
df_resultados.to_csv('Resultados/resultados_por_car.csv', encoding='utf-8')
