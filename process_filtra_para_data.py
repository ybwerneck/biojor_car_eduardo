import geopandas as gpd
from load_data import GeoDataLoader  # Ensure GeoDataLoader is defined as before
import os
from shapely.geometry.base import BaseGeometry
from geopandas import GeoDataFrame

import matplotlib.pyplot as plt
def filter_and_save_to_para(datasets, uf_gdf, base_input_folder, target_folder_keyword, path):
    """
    Filters datasets based on whether their geometries are within the specified UF boundary,
    combines all geometries into a MultiPolygon for 'agua', and saves them to a target folder.
    """
    # Ensure the UF GeoDataFrame has a unified geometry
    para_boundary = uf_gdf.unary_union

    for label, gdf in datasets.items():
        if gdf is not None:
            print(f"Processing {label}...")

            # Perform cleaning operations
            gdf = gdf.dropna(subset=['geometry'])
            gdf = gdf[gdf.is_valid]
            gdf = gdf[~gdf['geometry'].is_empty]

            if gdf.crs is None:
                gdf = gdf.set_crs("EPSG:4326")

            # Filter geometries within the UF boundary
            filtered_gdf = gdf[gdf.geometry.intersects(para_boundary)]

            if label == "agua":
                print(f"Combining all geometries in {label} into a MultiPolygon...")
                # Combine all geometries into a single MultiPolygon
                combined_geometry = filtered_gdf.geometry.unary_union
                combined_gdf = GeoDataFrame(geometry=[combined_geometry], crs=filtered_gdf.crs)
                output_path = path[label].replace(base_input_folder, target_folder_keyword)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Save combined geometry as a single MultiPolygon shapefile
                combined_gdf.to_file(output_path)
                print(f"Combined MultiPolygon saved to {output_path}")

                # Save the combined geometry to a CSV (if needed, save metadata without geometry)
                csv_file_path = f"{output_path[:-10]}_combined.csv"
                combined_gdf.drop(columns=['geometry']).to_csv(csv_file_path, index=False)
                print(f"CSV saved to {csv_file_path}")

                continue  # Skip further processing for "agua"

            # For other datasets, proceed with regular processing
            input_path = path[label]
            output_path = input_path.replace(base_input_folder, target_folder_keyword)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            filtered_gdf.to_file(output_path)

            if not filtered_gdf.empty:
                print(f"Filtered {label} saved to {output_path}")
                data_to_save = filtered_gdf.drop(columns=['geometry'])
                csv_file_path = f"{output_path[:-10]}_selected.csv"
                data_to_save.to_csv(csv_file_path, index=False)
                print(f"CSV saved to {csv_file_path}")
            else:
                print(f"No geometries in {label} are within PARA.")

if __name__ == "__main__":
    # File paths
    brasil_files = {
       # "astm": "dados/brasil/Assentamentos/cat63_settlements_WGS84.shp",
       # "fpnds": "dados/brasil/FPND/florestas_publicas_naodestinadas.shp",
       # "qlbs": "dados/brasil/Quilombolas/cat62_quilombola_WGS84.shp",
       # "tis": "dados/brasil/TIs/cat61_indigenous_territories_WGS84.shp",
       # "ucs": "dados/brasil/UCs/cat60_protected_area_WGS84_v2.shp",
        "agua": "dados/brasil/Agua/geoft_bho_massa_dagua_v2019.shp",
    }
    uf_file = "dados/PARA/UF/PA_UF_2023.shp"
    base_input_folder = "dados/brasil"
    target_folder_keyword = "dados/PARA"

    # Load datasets
    loader = GeoDataLoader()
    datasets = loader.load_all(brasil_files)
    uf_gdf = loader.load_and_clean(uf_file)

    if uf_gdf is not None:
        # Filter datasets and save them to PARA folder
        filter_and_save_to_para(datasets, uf_gdf, base_input_folder, target_folder_keyword,brasil_files)
    else:
        print("Failed to load the UF boundary data.")
