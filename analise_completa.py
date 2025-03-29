import geopandas as gpd
import matplotlib.pyplot as plt
from load_data import GeoDataLoader
from utils import find_intersections
import numpy as np
import matplotlib.patches as mpatches




# Carregar o arquivo shapefile


files = {
        "car": "dados/PARA/CAR/AREA_IMOVEL_1.shp",
        "municipios": "dados/PARA/Municipios/PA_Municipios_2023.shp",
        "uf": "dados/PARA/UF/PA_UF_2023.shp",
        "ucs": "dados/PARA/UCs/cat60_protected_area_WGS84_v2.shp",
         "astm": "dados/PARA/Assentamentos/cat63_settlements_WGS84.shp",
       # "fpnds": "dados/PARA/FPND/florestas_publicas_naodestinadas.shp",
        "qlbs": "dados/PARA/Quilombolas/cat62_quilombola_WGS84.shp",
        "tis": "dados/PARA/TIs/cat61_indigenous_territories_WGS84.shp",
        "ucs": "dados/PARA/UCs/cat60_protected_area_WGS84_v2.shp",
}
datasets = GeoDataLoader().load_all(files)

uf = datasets.get("uf")
municipios = datasets.get("municipios")
car = datasets.get("car")
q_is = np.array(list(files.keys()))[3:]  # Convert keys to an array
print(q_is)




plot=True
if(plot):

    # Assuming 'files' and 'datasets' are already defined elsewhere
    fig, ax = plt.subplots(figsize=(30, 16),dpi=100)

    uf.plot(ax=ax,color='white', edgecolor='black',linewidth=1, alpha=1,figsize=(25, 12))
    municipios.plot(ax=ax,color='white', edgecolor='black',linewidth=0.2, alpha=1,figsize=(30, 16))

    colors = ["blue", "yellow", "orange", "pink", "purple"]
    i = 0

    # Create a figure and axis for plotting

    # List to hold proxy artists for the legend
    proxy_artists = []

    # Plot each dataset using GeoPandas
    for dset in q_is:
        print(dset)
        # Plot each dataset
        datasets[dset].plot(ax=ax, edgecolor='black', linewidth=0, color=colors[i], alpha=0.6)
        
        # Create a proxy artist (for legend) that looks like the plot
        proxy = mpatches.Patch(color=colors[i], label=dset)
        proxy_artists.append(proxy)
        i += 1

    # Plot the 'car' dataset with its own label
    car_plot_obj = car.plot(ax=ax, color='green', edgecolor='black', linewidth=0.001, alpha=0.1)

    # Create a proxy artist for 'Car Data'
    car_proxy = mpatches.Patch(color='green', label='car')
    proxy_artists.append(car_proxy)

    # Manually create the legend using proxy artists
    ax.legend(handles=proxy_artists)

    # Adjust layout to avoid overlap and ensure the legend is visible
    plt.tight_layout()

    # Save the plot to a file
    plt.savefig("plot_all.png", bbox_inches='tight')  # Ensures legend is not cut off

    # Optionally, you can display the plot (if running in an interactive environment)
    # plt.show()


intersect={}
i = 0

for dset in q_is:
    print(dset)
    intersect[dset]=find_intersections(car,datasets[dset])
    print(intersect[dset].head())
    
    if(plot):

        # Create a figure and axis for plotting
        fig, ax = plt.subplots(figsize=(30, 16),dpi=100)
        uf.plot(ax=ax,color='white', edgecolor='black',linewidth=0.01, alpha=1)
        municipios.plot(ax=ax,color='white', edgecolor='black',linewidth=0.005, alpha=1)

        # List to hold proxy artists for the legend
        proxy_artists = []

        # Plot each dataset using GeoPandas

            # Plot each dataset
        datasets[dset].plot(ax=ax, edgecolor='black', linewidth=0, color=colors[i], alpha=0.6)
            
            # Create a proxy artist (for legend) that looks like the plot
        proxy = mpatches.Patch(color=colors[i], label=dset)
        proxy_artists.append(proxy)
        i += 1

        # Plot the 'car' dataset with its own label
        car_plot_obj = car.plot(ax=ax, color='green', edgecolor='black', linewidth=0.001, alpha=0.1)

        # Create a proxy artist for 'Car Data'
        car_proxy = mpatches.Patch(color='green', label='car')
        proxy_artists.append(car_proxy)
        
        i_obj=intersect[dset].plot(ax=ax, color='red', edgecolor='black', linewidth=0.001, alpha=0.4)

        # Create a proxy artist for 'Car Data'
        i_proxy = mpatches.Patch(color='red', label='intersections')
        proxy_artists.append(i_proxy)
        

        # Manually create the legend using proxy artists
        ax.legend(handles=proxy_artists)

        # Adjust layout to avoid overlap and ensure the legend is visible
        plt.tight_layout()

        # Save the plot to a file
        plt.savefig(f"plot_{dset}.png", bbox_inches='tight')  # Ensures legend is not cut off

    # Optionally, you can display the plot (if running in an interactive environment)
    # plt.show()

