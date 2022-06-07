import pandas as pd
import re
import numpy as np
from pathlib import Path

# Carreguem el joc de dades
df = pd.read_csv("barcelona_pisos_dataset.csv")

# Eliminem els pisos repetits
bool_series = df.duplicated(keep='first')
df = df[~bool_series]

# Eliminem les files que tenen valors nuls
df = df.dropna()

# Ens quedem amb les següents característiques generals: Aire acondicionado, Amueblado, Año construcción, Calefacción, Cerca de transporte público, Chimenea, Obra nueva, Piscina propia, Plaza parking
Aire_acondicionat = []
Moblat = []
Any_construccio = []
Calefaccio = []
Transport_public_proper = []
Llar_de_foc = []
Obra_nova = []
Piscina_propia = []
Plaza_parking = []
for i in df["CaracteristicasGenerales"].tolist():
    if 'Aire acondicionado ' in i:
        Aire_acondicionat.append(1)
    else:
        Aire_acondicionat.append(0)
    if 'Amueblado ' in i:
        Moblat.append(1)
    else:
        Moblat.append(0)
    if 'Calefacción ' in i:
        Calefaccio.append(1)
    else:
        Calefaccio.append(0)
    if 'Cerca de transporte público ' in i:
        Transport_public_proper.append(1)
    else:
        Transport_public_proper.append(0)
    if 'Chimenea ' in i:
        Llar_de_foc.append(1)
    else:
        Llar_de_foc.append(0)
    if 'Obra nueva ' in i:
        Obra_nova.append(1)
    else:
        Obra_nova.append(0)
    if 'Piscina propia ' in i:
        Piscina_propia.append(1)
    else:
        Piscina_propia.append(0)
    if 'Plaza parking ' in i:
        Plaza_parking.append(1)
    else:
        Plaza_parking.append(0)
    if re.search("[0-9]{4}", i) is None:
        Any_construccio.append("n/a")
    else:
        Any_construccio.append(re.search("[0-9]{4}", i).group())
df =df.assign(Aire_acondicionat = Aire_acondicionat,Moblat = Moblat, Any_construccio = Any_construccio, Calefaccio = Calefaccio,Transport_public_proper = Transport_public_proper,
              Llar_de_foc = Llar_de_foc, Obra_nova=Obra_nova, Piscina_propia=Piscina_propia, Plaza_parking=Plaza_parking)

# Ens quedem amb les següents equipaments comunitaris: Ascensor, Cuota comunidad, Equipamiento deportivo, Jardín comunitario, Piscina comunitaria, Vigilancia
Ascensor = []
Cuota_comunitat = []
Equipamient_esportiu = []
Jardi_comunitari = []
Piscina_comunitaria = []
Vigilancia = []

for i in df["EquipamientoComunitario"].tolist():
    if 'Ascensor ' in i:
        Ascensor.append(1)
    else:
        Ascensor.append(0)
    if 'Cuota_comunidad ' in i:
        Cuota_comunitat.append(1)
    else:
        Cuota_comunitat.append(0)
    if 'Equipamiento deportivo ' in i:
        Equipamient_esportiu.append(1)
    else:
        Equipamient_esportiu.append(0)
    if 'Jardín comunitario ' in i:
        Jardi_comunitari.append(1)
    else:
        Jardi_comunitari.append(0)
    if 'Piscina comunitaria ' in i:
        Piscina_comunitaria.append(1)
    else:
        Piscina_comunitaria.append(0)
    if 'Vigilancia ' in i:
        Vigilancia.append(1)
    else:
        Vigilancia.append(0)
df =df.assign(Ascensor = Ascensor, Cuota_comunitat = Cuota_comunitat, Equipamient_esportiu = Equipamient_esportiu, Jardi_comunitari = Jardi_comunitari, Piscina_comunitaria=Piscina_comunitaria,Vigilancia=Vigilancia)

# Eliminem columnes que no necessitem
df = df.drop(columns=['CaracteristicasGenerales', 'EquipamientoComunitario', 'Title'])

# Eliminem les files que tenen valors nuls
df = df.dropna()

# Eliminem les files amb valors incorrectes de "Año_construcción"
df.drop(df.index[df['Any_construccio'] == "n/a"], inplace=True)
df['Any_construccio'] = pd.to_numeric(df['Any_construccio'])

# Eliminem les files amb valors extrems de "ConsumokW" i "Emisioneskg"
df.drop(df.index[df['ConsumokW'] >= ((np.mean(df['ConsumokW']) + 2 * np.std(df['ConsumokW'])))], inplace=True)
df.drop(df.index[df['ConsumokW'] <= ((np.mean(df['ConsumokW']) - 2 * np.std(df['ConsumokW'])))], inplace=True)
df.drop(df.index[df['Emisioneskg'] >= ((np.mean(df['Emisioneskg']) + 2 * np.std(df['Emisioneskg'])))], inplace=True)
df.drop(df.index[df['Emisioneskg'] <= ((np.mean(df['Emisioneskg']) - 2 * np.std(df['Emisioneskg'])))], inplace=True)

# Eliminem es files amb valors extrems de "Preu"
df['Preu'] = df['Preu'].str.replace('.', '')
df['Preu'] = df.Preu.str.replace(r"[a-zA-Zéò]", '')
df['Preu'] = pd.to_numeric(df['Preu'])
df.drop(df.index[df['Preu'] <= 1000], inplace=True)
df.drop(df.index[df['Preu'] >= 1500000], inplace=True)
df = df.dropna()

# Eliminem "Preu m2" perquè es pot calcular a partir d'altres dades del dataset
df = df.drop(columns=['Preu m2'])

# Eliminem es files amb valors extrems de "Nº Lavabos"
df.drop(df.index[df["Lavabos"].apply(lambda x: not (x.strip().isnumeric()))], axis=0, inplace=True)
df['Lavabos'] = pd.to_numeric(df['Lavabos'])
df.drop(df.index[df['Lavabos'] <= ((np.mean(df['Lavabos']) - 2 * np.std(df['Lavabos'])))], inplace=True)
df.drop(df.index[df['Lavabos'] >= ((np.mean(df['Lavabos']) + 2 * np.std(df['Lavabos'])))], inplace=True)


# Eliminem es files amb valors extrems de "Nº Habitacions"
df['Habitacions'] = pd.to_numeric(df['Habitacions'])
df.drop(df.index[df['Habitacions'] >= ((np.mean(df['Habitacions']) + 2 * np.std(df['Habitacions'])))], inplace=True)
df.drop(df.index[df['Habitacions'] <= ((np.mean(df['Habitacions']) - 2 * np.std(df['Habitacions'])))], inplace=True)

# Eliminem es files amb valors extrems de "Area"
df['Area'] = pd.to_numeric(df['Area'])
df.drop(df.index[df['Area'] >= ((np.mean(df['Area']) + 2 * np.std(df['Area'])))], inplace=True)
df.drop(df.index[df['Area'] <= ((np.mean(df['Area']) - 2 * np.std(df['Area'])))], inplace=True)

# Creem la columna Districte a partir de la del Barri
Districte = []
for i in df["Barri"].tolist():
    if i in ["Esquerra Alta de l´Eixample", "Dreta de l´Eixample", "Esquerra Baixa de l´Eixample", "Fort Pienc", "Sagrada Família", "Sant Antoni"]:
        Districte.append("Eixample")
    elif i in ["Barceloneta", "Gòtic", "Raval", "St. Pere - Sta. Caterina - El Born"]:
        Districte.append("Ciutat Vella")
    elif i in ["Badal", "Font de la Guatlla", "Hostafrancs", "La Bordeta", "La Marina-Montjuïc", "La Marina-Port", "Poble Sec", "Sants"]:
        Districte.append("Sants Montjuic")
    elif i in ["Les Corts", "Pedralbes", "Sant Ramon - Maternitat"]:
        Districte.append("Les Corts")
    elif i in ["Putget - Farró", "Sant Gervasi - Bonanova", "Sant Gervasi - Galvany", "Sarrià", "Tres Torres", "Vallvidrera - Tibidabo - Les Planes"]:
        Districte.append("Sarria Sant Gervasi")
    elif i in ["Camp d´en Grassot - Gràcia N.", "El Coll", "La Salut", "Vallcarca - Penitents", "Vila de Gràcia"]:
        Districte.append("Gracia")
    elif i in ["Baix Guinardó", "Can Baró", "Carmel", "Font d´en Fargas", "Guinardó","Horta","Montbau","Sant Genís dels Agudells","Taxonera","Vall d´Hebron"]:
        Districte.append("Horta Guinardo")
    elif i in ["Canyelles", "Ciutat Meridiana", "La Guineueta", "Porta", "Prosperitat","Roquetes","Torre Baró","Trinitat Nova","Turó de la Peira - Can Peguera","Vallbona","Verdun","Vilapicina - Torre Llobeta"]:
        Districte.append("Nou Barris")
    elif i in ["Bon Pastor", "Congrés - Indians", "La Sagrera", "Navas", "Sant Andreu","Trinitat Vella"]:
        Districte.append("Sant Andreu")
    elif i in ["Besòs - Maresme", "Camp de l´Arpa", "Diagonal Mar - La Mar Bella", "El Clot", "Glòries El Parc","La Verneda - La Pau","Poblenou","Provençals del Poblenou","Sant Martí","Vila Olímpica"]:
        Districte.append("Sant Marti")
    else:
        Districte.append("")
df = df.dropna()
df = df.assign(Districte = Districte)


pd.set_option('display.width', 800)
pd.set_option('display.max_columns', 26)
print(df)
filepath = Path('home/out.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(filepath)
