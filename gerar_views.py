import pandas as pd

def read_csv_files(file1, file2, file3):
    df_car = pd.read_csv(file1)
    df_cat = pd.read_csv(file2)
    df_cid = pd.read_csv(file3)
    
    return df_car, df_cat, df_cid

def filter_top_categories(df_cat):
    df_cat["Percentual sobreposto"] = df_cat["Percentual sobreposto"].round(4)
    df_cat = df_cat.sort_values(by=["Área sobreposta com CAR"], ascending=[False])

    top_ucs = df_cat[df_cat["Dataset"] == "UCs"]
    top_asse = df_cat[df_cat["Dataset"] == "Assen."]
    top_qui = df_cat[df_cat["Dataset"] == "Quil."]
    top_tis = df_cat[df_cat["Dataset"] == "TIs"]

    top_ucs = top_ucs.head(10)
    top_asse = top_asse.head(10)
    top_qui = top_qui.head(10)
    top_tis = top_tis.head(10)

    # Exibir as primeiras linhas de cada DataFrame
    print("Top UCs mais interseccionados:")
    print(top_ucs)
    print("\nTop Assentamentos mais interseccionados:")
    print(top_asse)
    print("\nTop Quilombolas mais interseccionados:")
    print(top_qui)
    print("\nTop TIs mais interseccionados:")
    print(top_tis)

    top_ucs.to_csv("./Resultados_Visualização/Categorias/top_ucs.csv")
    top_tis.to_csv("./Resultados_Visualização/Categorias/top_tis.csv")
    top_asse.to_csv("./Resultados_Visualização/Categorias/top_assentamentos.csv")
    top_qui.to_csv("./Resultados_Visualização/Categorias/top_quilombos.csv")
    


def filter_top_cars(df_car):
    df_car_ucs = df_car[['CAR','cond','cidade','Área_Total','Área CAR sob UCs','PC CAR sob UCs']]
    df_car_tis = df_car[['CAR','cond','cidade','Área_Total','Área CAR sob TIs','PC CAR sob TIs']]
    df_car_asse = df_car[['CAR','cond','cidade','Área_Total','Área CAR sob Assen.','PC CAR sob Assen.']]
    df_car_qui = df_car[['CAR','cond','cidade','Área_Total','Área CAR sob Quil.','PC CAR sob Quil.']]

    df_car_ucs = df_car_ucs.sort_values(by=["Área CAR sob UCs"], ascending=[False])
    df_car_tis = df_car_tis.sort_values(by=["Área CAR sob TIs"], ascending=[False])
    df_car_asse = df_car_asse.sort_values(by=["Área CAR sob Assen."], ascending=[False])
    df_car_qui = df_car_qui.sort_values(by=["Área CAR sob Quil."], ascending=[False])

    df_car_ucs=df_car_ucs.head(10)
    df_car_tis=df_car_tis.head(10)
    df_car_asse=df_car_asse.head(10)
    df_car_qui=df_car_qui.head(10)

    print("Top CARs que mais sobrepõem UCs:")
    print(df_car_ucs)
    print("Top CARs que mais sobrepõem TIs:")
    print(df_car_tis)
    print("Top CARs que mais sobrepõem Assentamentos:")
    print(df_car_asse)
    print("Top CARs que mais sobrepõem Quilombolas:")
    print(df_car_qui)

    df_car_ucs.to_csv("./Resultados_Visualização/CARs/top_cars_ucs.csv")
    df_car_tis.to_csv("./Resultados_Visualização/CARs/top_cars_tis.csv")
    df_car_asse.to_csv("./Resultados_Visualização/CARs/top_cars_assentamentos.csv")
    df_car_qui.to_csv("./Resultados_Visualização/CARs/top_cars_quilombos.csv")

def filter_top_cities(df_cid):

    #df_cid = df_cid.sort_values(by=["Área CAR sob UCs"], ascending=[False])
    df_cid_ucs = df_cid[['Unnamed: 0','Area Cidade','Car Registros','CAR - Area','Percentual CAR','UCs - Area CAT ','UCs - Area CAR sob CAT','UCs - N CAR sob CAT','UCs - Pc CAR sob CAT']]
    df_cid_tis = df_cid[['Unnamed: 0','Area Cidade','Car Registros','CAR - Area','Percentual CAR','TIs - Area CAT ','TIs - Area CAR sob CAT','TIs - N CAR sob CAT','TIs - Pc CAR sob CAT']]
    df_cid_asse = df_cid[['Unnamed: 0','Area Cidade','Car Registros','CAR - Area','Percentual CAR','Assen. - Area CAT ','Assen. - Area CAR sob CAT','Assen. - N CAR sob CAT','Assen. - Pc CAR sob CAT']]
    df_cid_qui = df_cid[['Unnamed: 0','Area Cidade','Car Registros','CAR - Area','Percentual CAR','Quil. - Area CAT ','Quil. - Area CAR sob CAT','Quil. - N CAR sob CAT','Quil. - Pc CAR sob CAT']]
    
    df_cid_ucs = df_cid_ucs.sort_values(by=["UCs - Area CAR sob CAT"], ascending=[False])
    df_cid_tis = df_cid_tis.sort_values(by=["TIs - Area CAR sob CAT"], ascending=[False])
    df_cid_asse = df_cid_asse.sort_values(by=["Assen. - Area CAR sob CAT"], ascending=[False])
    df_cid_qui = df_cid_qui.sort_values(by=["Quil. - Area CAR sob CAT"], ascending=[False])

    df_cid_ucs=df_cid_ucs.head(5)
    df_cid_tis=df_cid_tis.head(5)
    df_cid_asse=df_cid_asse.head(5)
    df_cid_qui=df_cid_qui.head(5)

    print("Top cidades com mais UCs sobrepostos:")
    print(df_cid_ucs)
    print("Top cidades com mais TIs sobrepostos:")
    print(df_cid_tis)
    print("Top cidades com mais Assentamentos sobrepostos:")
    print(df_cid_asse)
    print("Top cidades com mais Quilombolas sobrepostos:")
    print(df_cid_qui)

    df_cid_ucs.to_csv("./Resultados_Visualização/Cidades/top_cidades_ucs.csv")
    df_cid_tis.to_csv("./Resultados_Visualização/Cidades/top_cidades_tis.csv")
    df_cid_asse.to_csv("./Resultados_Visualização/Cidades/top_cidades_assentamentos.csv")
    df_cid_qui.to_csv("./Resultados_Visualização/Cidades/top_cidades_quilombos.csv")


# Exemplo de uso
file1 = "Resultados/resultados_por_car.csv"
file2 = "Resultados/resultados_por_categoria.csv"
file3 = "Resultados/resultados_por_cidade.csv"

df_car, df_cat, df_cid = read_csv_files(file1, file2, file3)

filter_top_categories(df_cat)
filter_top_cars(df_car)
filter_top_cities(df_cid)


