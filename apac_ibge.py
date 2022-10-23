# 1. Importar bibliotecas
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt


# 2. Ler os dados base do Censo
df = pd.read_excel('Basico_PE.xls')


# 3. Identificar setores presentes na planície de inundação
# a. Importando shapefiles | Obs.: coordenadas geográficas
planicie = gpd.read_file("planicie_una_200_cb.shp") # Shapefile da planície de inundação
#planicie.plot()
#plt.show()
print(planicie.crs)

setores = gpd.read_file('26SEE250GC_SIR.shp') # Shapefile dos setores censitários
setores_copy = setores
#setores.plot()
#plt.show()
#print(setores_copy.columns)
setores_copy = setores_copy.rename(columns={'CD_GEOCODI': 'Cod_setor'}) # Obs.: Estabelecer coluna com o mesmo nome no df e no shape
#print(setores_copy.columns)
#print(setores['CD_GEOCODI'])
print(setores_copy.crs)

# Convertendo shapefiles para o mesmo Sistema de Coordenadas
    # fonte: https://epsg.io/4326
    # EPSG:4326 = WGS84 - World Geodetic System 1984
planicie_reprojected = planicie.to_crs('epsg:4326')
setores_reprojected = setores_copy.to_crs('epsg:4326')

print(planicie_reprojected.crs)
print(setores_reprojected.crs)

# b. Combinar setores (shape e excel)
#Convert 'Cod_setor' variable in df to integer
df['Cod_setor'] = df['Cod_setor'].astype(np.int64)
setores_reprojected['Cod_setor'] = setores_reprojected['Cod_setor'].astype(np.int64)

# Column join - take dataset A + dataset B = dataset AB, based on a common column
pernambuco_merge = setores_reprojected.merge(df, on='Cod_setor') # Unindo Dataframe(df) e tabela de atributos do shapefile
print(pernambuco_merge.head())
print(pernambuco_merge.columns)

# c. Máscara | geopandas.clip(gdf, mask, keep_geom_type=False)
clip = gpd.clip(pernambuco_merge, planicie_reprojected, keep_geom_type=False)
clip.plot()
plt.show()
print(clip.head())
print(clip.columns)


# 4. Imprimir resultados (tabela) | Apenas setores de interessa

    # Arquivo: Basico_PE
    # Nº de domicílios (V001)
    # Nº de moradores (V002)
    # Renda (V005) sum 9797276.83

# a.  Renomear colunas de interesse para melhor identificação
clip = clip.rename(columns={'V001': 'numero_de_domicilios', 'V002': 'numero_de_moradores', 'V005': 'renda'})
print(clip.columns)
print(clip.head())

# b. Plotar colunas selecionadas
columns = ['NM_MUNICIP', 'numero_de_domicilios', 'numero_de_moradores', 'renda']
clip_results = pd.DataFrame(clip, columns=columns)
print(clip_results)

# 5. Salvar no banco de dados