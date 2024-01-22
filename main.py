import os
import streamlit as st
import geopandas as gpd
import pydeck as pdk

# Lendo o arquivo shapefile dos municípios de Mato Grosso
estado = gpd.read_file("./mtmap/LIMITE_ESTADO/LIMITE_ESTADO.shp")
municipios = gpd.read_file("./mtmap/MT_Municipios_2022/MT_Municipios_2022.shp")
microbacias = gpd.read_file("./mtmap/SHAPEFILES/DELIMITA├З├ГO/Microbacia_UPG4_SEMA.shp")


microbacias = microbacias.to_crs(municipios.crs)

camada_selecionada = st.selectbox("Selecione a camada:", ["Municípios", "Microbacias"])


if camada_selecionada == "Microbacias":
    properties_keys = list(microbacias.columns)

    variavel_selecionada = st.selectbox("Selecione a variável:", properties_keys)

    # Adiciona uma coluna 'weight' com base na variável selecionada
    microbacias['weight'] = microbacias[variavel_selecionada]

    # Define a escala máxima para normalização dos pesos (ajuste conforme necessário)
    max_weight = microbacias['weight'].max()

    # Normaliza os pesos para o intervalo [0, 1]
    microbacias['weight_normalized'] = microbacias['weight'] / max_weight
else:
    properties_keys = list(municipios.columns)

    variavel_selecionada = st.selectbox("Selecione a variável:", properties_keys)
    # Normaliza os pesos para o intervalo [0, 1]
    microbacias['weight_normalized'] = 0




# Configuração do estado inicial do mapa
view_state = pdk.ViewState(
    longitude=municipios.geometry.centroid.x.mean(),
    latitude=municipios.geometry.centroid.y.mean(),
    zoom=6,
)

# Criação das camadas
municipios_layer = pdk.Layer(
    "GeoJsonLayer",
    data=municipios,
    get_fill_color=[0, 255, 0, 100],
    pickable=True,
    auto_highlight=True,
    filled=True,
    extruded=False,
    wireframe=False,
    get_line_color=[255, 0, 255, 200],
    get_line_width=20,
    highlight_color=[255, 255, 0, 100],
)

microbacias_layer = pdk.Layer(
    "GeoJsonLayer",
    data=microbacias,
    get_fill_color=f"[255 * (1 - weight_normalized), 0, 255 * weight_normalized, 200]",
    pickable=True,
    auto_highlight=True,
    filled=True,
    extruded=False,
    wireframe=False,
    get_line_color=[255, 255, 255],
    get_line_width=1,
    highlight_color=[255, 255, 0, 100],
)

tooltip = {""}

# Verifica a camada selecionada e cria o deck com a camada correspondente
if camada_selecionada == "Municípios":
    layers = [municipios_layer]
else:
    layers = [microbacias_layer]

# Criação do deck com a camada selecionada
r = pdk.Deck(
    layers=layers,
    initial_view_state=view_state,
    map_style="road",
    tooltip={"html": f"<b>{variavel_selecionada}:</b> {{{variavel_selecionada}}}", "style": {"color": "white"}},
)

# Exibir o mapa no Streamlit
st.pydeck_chart(r)
