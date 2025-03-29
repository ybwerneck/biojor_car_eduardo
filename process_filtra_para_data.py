import geopandas as gpd
from load_data import GeoDataLoader  # Ensure GeoDataLoader is defined as before
import os

def filter_and_save_to_para(datasets, uf_gdf, base_input_folder, target_folder_keyword,path):
    """
    Filters datasets based on whether their geometries are within the specified UF boundary
    and saves them to a target folder by replacing part of the original file path.

    :param datasets: Dictionary of GeoDataFrames to filter
    :param uf_gdf: GeoDataFrame representing the UF boundary (e.g., PARA)
    :param base_input_folder: Base input folder containing the original files
    :param target_folder_keyword: Keyword in the input paths to replace for target folder (e.g., 'brasil' -> 'PARA')
    """
    # Ensure the UF GeoDataFrame has a unified geometry
    para_boundary = uf_gdf.unary_union

    for label, gdf in datasets.items():
        if gdf is not None:
            print(f"Filtering {label} for geometries within PARA...")
            # Perform the spatial filter
            filtered_gdf = gdf[gdf.geometry.within(para_boundary)]
            
            if not filtered_gdf.empty:
                # Replace the keyword in the file path
                input_path = path[label]
                output_path = input_path.replace(base_input_folder, target_folder_keyword)

                # Ensure the target folder exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Save the filtered GeoDataFrame
                filtered_gdf.to_file(output_path)
                print(f"Filtered {label} saved to {output_path}")
            else:
                print(f"No geometries in {label} are within PARA.")

if __name__ == "__main__":
    # File paths
    brasil_files = {
        "astm": "dados/brasil/Assentamentos/cat63_settlements_WGS84.shp",
        "fpnds": "dados/brasil/FPND/florestas_publicas_naodestinadas.shp",
        "qlbs": "dados/brasil/Quilombolas/cat62_quilombola_WGS84.shp",
        "tis": "dados/brasil/TIs/cat61_indigenous_territories_WGS84.shp",
        "ucs": "dados/brasil/UCs/cat60_protected_area_WGS84_v2.shp",
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
