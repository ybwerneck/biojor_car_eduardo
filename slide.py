import pandas as pd

# Load the CAR data
file1 = "Resultados/resultados_por_car.csv"
df_car = pd.read_csv(file1)

# Display basic statistics
print("\n=== Basic Statistics for CAR Data ===")
print(df_car.describe())

# Check for missing values
print("\n=== Missing Values in CAR Data ===")
print(df_car.isnull().sum())

# Display unique values in the 'cond' column, if it exists
if "cond" in df_car.columns:
    print("\n=== Unique Conditions in CAR Data ===")
    print(df_car["cond"].value_counts())

# Agrupar por cidade e calcular as contagens de status
print(df_car.columns)
if "cidade" in df_car.columns and "cond" in df_car.columns:
    city_status_counts = df_car.groupby("cidade")["cond"].value_counts(normalize=True).unstack(fill_value=0)

    # Converter para porcentagens
    city_status_percentages = city_status_counts * 100

    print("\n=== Percentuais de Status por Cidade ===")
    print(city_status_percentages)


import matplotlib.pyplot as plt

# Calculate the number of cars per city
city_car_counts = df_car['cidade'].value_counts()

# Get the top 20 cities with the most cars
top_20_cities = city_car_counts.head(20).index

# Filter the original data to only include these top 20 cities
df_top_20 = df_car[df_car['cidade'].isin(top_20_cities)]

# Group by city and condition, then calculate percentages
city_status_counts_top_20 = df_top_20.groupby("cidade")["cond"].value_counts(normalize=True).unstack(fill_value=0)

# Convert to percentage
city_status_percentages_top_20 = city_status_counts_top_20 * 100

# Plot the stacked bar chart for top 20 cities
plt.figure(figsize=(14, 8))
city_status_percentages_top_20.plot(kind='bar', stacked=True, colormap='viridis', figsize=(14, 8))

# Add labels and title
plt.title("Percentuais de Status por Cidade (Top 20 com Mais CARs)", fontsize=16)
plt.xlabel("Cidades", fontsize=12)
plt.ylabel("Percentual (%)", fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Display the legend
plt.legend(title="Status", bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent clipping
plt.tight_layout()

# Show plot
plt.show()

import matplotlib.pyplot as plt

# Define the custom color mapping
color_map = {
    'Analisado, aguardando atendimento a notificacao': 'green',   # Green for completed analysis
    'Em analise': 'yellow',                                      # Yellow for analysis in process
    'Cancelado por decisao administrativa': 'red',                # Red for cancelled by administrative decision
    'Aguardando analise': 'grey',                           # Lighter green for waiting for analysis
    'Analisado sem pendencias': 'darkgreen',                      # Dark green for analyzed without pending issues
    'Analisado, aguardando regularizacao ambiental (Lei n 12.651/2012)': 'lightseagreen',  # Light greenish
    'Cancelado por decisao judicial': 'firebrick',                 # Brick red for cancelled by judicial decision
    'Analisado, em conformidade com a Lei n 12.651/2012': 'darkolivegreen',  # Olive green for law compliance
    'Cancelado por duplicidade': 'darkred',                       # Dark red for cancellation due to duplication
    'Analisado, em regularizacao ambiental (Lei n 12.651/2012)': 'mediumseagreen'  # Medium green for environmental regularization
}

# Plot the stacked bar chart for the top 20 cities
plt.figure(figsize=(14, 8))

# Plot the stacked bar chart with custom colors
city_status_percentages_top_20.plot(kind='bar', stacked=True, figsize=(14, 8), color=[color_map.get(status, 'gray') for status in city_status_percentages_top_20.columns])

# Add labels and title
plt.title("Percentuais de Status por Cidade (Top 20 com Mais CARs)", fontsize=16)
plt.xlabel("Cidades", fontsize=12)
plt.ylabel("Percentual (%)", fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Display the legend with custom labels
plt.legend(title="Status", bbox_to_anchor=(1.05, 1), loc='upper left', labels=[label for label in city_status_percentages_top_20.columns])

# Adjust layout to prevent clipping
plt.tight_layout()

# Show plot
plt.savefig("city.png")
