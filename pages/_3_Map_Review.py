import geopandas as gpd
import osmium
from streamlit_folium import st_folium
import folium
from folium.features import GeoJsonPopup
import streamlit as st



st.set_page_config(layout="wide")
st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec;
            color:white;
            font-family: 'Comfortaa', sans-serif;
    }

    body{
        font-size: 18px;
    }

    [role=radiogroup]{
        gap: 1rem;
    }
    h1 {
        text-align: center
    }
    h2 {
        text-align: center
    }
    h3 {
        text-align: center
    }
    
    div[data-testid='stAppViewBlockContainer']{
        background-color: #62cbec10;
    }
            .center {
    display: block;
    margin-left: auto;
    margin-right: auto;
        width:200px;
}
</style>
""", unsafe_allow_html=True)

input_osm=osmium.FileProcessor("https://api06.dev.openstreetmap.org/api/0.6/map?bbox=9.21734%2C45.47109%2C9.23813%2C45.48607",osmium.osm.WAY)
osm_data= input_osm.with_filter(osmium.filter.GeoInterfaceFilter()) #.with_areas()
START_LOCATION = [9.227909,45.478059]
START_ZOOM = 16

features = gpd.GeoDataFrame.from_features(osm_data).set_crs(epsg=4326)

#for o in input_osm:
#    print(o)
    #for member in o.members:
        #st.write(f"Type: {member.type}  ID: {member.ref}  Role: {member.role}")

building=features[features.geometry.type=='MultiPolygon'][features.building.notnull()]
#highway=features[features.geometry.type=='LineString'][features.highway.notnull()]

building_style = {"fillColor": "red", "fillOpacity": 0.2,"color":"red"}
#highway_style = {"color":"white","weight":5}

building_popup = GeoJsonPopup(
    fields=list(building.columns)[1:],

)

#highway_popup = GeoJsonPopup(
#    fields=list(highway.columns)[1:],

#)

building_json = folium.GeoJson(data=building, style_function=lambda _x: building_style,popup=building_popup)
#highway_json = folium.GeoJson(data=highway, style_function=lambda _x: highway_style,popup=highway_popup)

map = folium.Map(
    location=START_LOCATION, zoom_start=START_ZOOM, max_zoom=21
)

folium.TileLayer(name='ESRI',tiles='https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}?blankTile=false',attr='esri',max_zoom=21,max_native_zoom=17,opacity=1).add_to(map)


lc=folium.LayerControl().add_to(map)

fg = folium.FeatureGroup(name="Icon collection", control=False).add_to(map)

building_json.add_to(fg)

map.fit_bounds(map.get_bounds(), padding=(30, 30))

st_folium(
            map,
            width="100%",
            height=600,
            returned_objects=[]
)


#If btn is pressed or True
if st.button('Refresh'):
    #This would empty everything inside the container
    st.empty()