import geopandas as gpd
import matplotlib.pyplot as plt

import geopandas as gpd

class GeoDataLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_and_clean(filepath):
        """
        Loads a shapefile and cleans the geometries by removing empty, null, and invalid geometries.

        :param filepath: Path to the shapefile
        :return: A cleaned GeoDataFrame
        """
        crs_proj = 'EPSG:32723'
        try:
            gdf = gpd.read_file(filepath)
            # Remove empty geometries
            gdf = gdf[~gdf.is_empty]
            # Remove null geometries
            gdf = gdf[gdf.notna()]
            # Remove invalid geometries
            gdf = gdf[gdf.is_valid]
          #  gdf=gdf.to_crs(crs_proj)
            return gdf
        except Exception as e:
            print(f"Error loading or cleaning file {filepath}: {e}")
            return None

    @staticmethod
    def load_all(files):
        """
        Loads and cleans a list of shapefiles.

        :param files: Dictionary of file labels and file paths
        :return: Dictionary of file labels and cleaned GeoDataFrames
        """
        data = {}
        for label, path in files.items():
            print(f"Loading {label} from {path}...")
            gdf = GeoDataLoader.load_and_clean(path)
            if gdf is not None:
                data[label] = gdf
            #print(gdf)
        return data

# Rodr o main para baixar
if __name__ == "__main__":
    files = {
        "imov": "PARA/imov/AREA_IMOVEL_1.shp",
        "municipios": "PARA/municipios/PA_Municipios_2023.shp",
        "uf": "PARA/PA_UF_2023/PA_UF_2023.shp",
        "ucs": "UCs/lim_unidade_protecao_integral_a.shp"
    }

    datasets = GeoDataLoader().load_all(files)

    # Access specific datasets
    if "imov" in datasets:
        print(datasets["imov"].head())
