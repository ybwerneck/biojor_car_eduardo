import geopandas as gpd
import matplotlib.pyplot as plt
from load_data import GeoDataLoader
from utils import find_intersections
import matplotlib.patches as mpatches

# === PARÂMETROS DEFINIDOS PELO USUÁRIO ===
categoria_escolhida = "UCs"  # "TIs", "Assen.", "Quil.", etc.
nome_unidade = "Floresta Nacional do Tapajós"  # substitua pelo nome exato da unidade

# === ARQUIVOS ===
arquivos = {
    "car": "dados/PARA/CAR/AREA_IMOVEL_1.shp",
    "municipios": "dados/PARA/Municipios/PA_Municipios_2023.shp",
    "uf": "dados/PARA/UF/PA_UF_2023.shp",
    "Assen.": "dados/PARA/Assentamentos/cat63_settlements_WGS84.shp",
    "Quil.": "dados/PARA/Quilombolas/cat62_quilombola_WGS84.shp",
    "TIs": "dados/PARA/TIs/cat61_indigenous_territories_WGS84.shp",
    "UCs": "dados/PARA/UCs/cat60_protected_area_WGS84_v2.shp",
}

# === CARREGAMENTO ===
datasets = GeoDataLoader().load_all(arquivos)
car = datasets["car"]
uf = datasets["uf"]
municipios = datasets["municipios"]
categoria = datasets[categoria_escolhida]

# === FILTRAR UNIDADE ESPECÍFICA ===
unidade = categoria[categoria["name"] == nome_unidade]

if unidade.empty:
    raise ValueError(f"Unidade '{nome_unidade}' não encontrada na categoria '{categoria_escolhida}'.")

# === CALCULAR INTERSEÇÃO COM CAR ===
intersect = find_intersections(car, unidade)

# === PLOTAGEM ===
fig, ax = plt.subplots(figsize=(20, 12), dpi=100)
uf.plot(ax=ax, color='white', edgecolor='black', linewidth=1)
municipios.plot(ax=ax, color='white', edgecolor='grey', linewidth=0.5)

# Plotar a unidade
unidade.plot(ax=ax, color='orange', edgecolor='black', linewidth=1, alpha=0.6)
unidade_proxy = mpatches.Patch(color='orange', label=nome_unidade)

# Plotar os CARs
car.plot(ax=ax, color='green', edgecolor='black', linewidth=0.1, alpha=0.1)
car_proxy = mpatches.Patch(color='green', label='CAR')

# Plotar interseções
if not intersect.empty:
    intersect.plot(ax=ax, color='red', edgecolor='black', linewidth=0.1, alpha=0.5)
    inter_proxy = mpatches.Patch(color='red', label='Interseções com CAR')
else:
    inter_proxy = mpatches.Patch(color='red', label='Nenhuma interseção')

# Legenda
ax.legend(handles=[unidade_proxy, car_proxy, inter_proxy])
plt.title(f"{nome_unidade} — Interseção com CAR", fontsize=16)
plt.tight_layout()

# === SALVAR ===
nome_slug = nome_unidade.lower().replace(" ", "_").replace("/", "_")
plt.savefig(f"Resultados/intersec_{categoria_escolhida}_{nome_slug}.png", bbox_inches='tight')
plt.close()
