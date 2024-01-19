import os
import streamlit as st
import geopandas as gpd
import pydeck as pdk

# Lendo o arquivo shapefile dos municípios de Mato Grosso
estado = gpd.read_file("./mtmap/LIMITE_ESTADO/LIMITE_ESTADO.shp")
municipios = gpd.read_file("./mtmap/MT_Municipios_2022/MT_Municipios_2022.shp")
microbacias = gpd.read_file("./mtmap/SHAPEFILES/DELIMITA├З├ГO/Microbacia_UPG4_SEMA.shp")


# Verifique qual é o sistema de coordenadas do GeoDataFrame
print("CRS Municípios:", estado.crs)
print("microbacias:", microbacias)


# Reprojeta os GeoDataFrames para o CRS de 'estado'
microbacias = microbacias.to_crs(municipios.crs)


# Verificar as propriedades disponíveis nas microbacias
properties_keys = list(microbacias.columns)

# Criar um menu dropdown para selecionar a variável
variavel_selecionada = st.selectbox("Selecione a variável:", properties_keys)



municipios_layer = pdk.Layer(
    "GeoJsonLayer",
    data=municipios,
    get_fill_color=[0, 255, 0, 100],  # Green color with 100 alpha (transparency)
    pickable=True,
    auto_highlight=True,
    filled=True,  # Ensure that polygons are filled
    extruded=False,  # Set to True if you want extruded polygons
    wireframe=False,  # Set to True if you want wireframe polygons
    get_line_color=[255, 255, 255],  # Line color for polygons
    get_line_width=1,  # Line width for polygons
    highlight_color=[255, 255, 0, 100],  # Highlight color when hovered

)
microbacias_layer = pdk.Layer(
    "GeoJsonLayer",
    data=microbacias,
    get_fill_color=[255, 0, 100],
    pickable=True,
    auto_highlight=True,
    filled=True,
    extruded=False,
    wireframe=False,
    get_line_color=[255, 255, 255],
    get_line_width=1,
    highlight_color=[255, 255, 0, 100],
)


view_state = pdk.ViewState(
    longitude=municipios.geometry.centroid.x.mean(),
    latitude=municipios.geometry.centroid.y.mean(),
    zoom=6,
)

r = pdk.Deck(
    layers=[microbacias_layer],
    initial_view_state=view_state,
    map_style="road",
    tooltip={"html": f"<b>{variavel_selecionada}:</b> {{{variavel_selecionada}}}", "style": {"color": "white"}},
)



# Exibir o mapa no Streamlit
st.pydeck_chart(r)
