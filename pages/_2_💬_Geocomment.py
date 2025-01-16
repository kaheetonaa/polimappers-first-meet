import streamlit as st
import requests
import geopandas as gpd
import folium
from folium.features import GeoJsonPopup
from streamlit_folium import st_folium
from pymongo import MongoClient


st.set_page_config(layout="wide")

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = init_connection()

db=client['Open-Geodata-Workshop']
collection=db['Open-Geodata-Workshop']


st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec10;
            color:black;
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

popup = GeoJsonPopup(
    fields=['projecId-str']
)
def load_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        raise
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        raise

def style_function(feature):
    props = feature.get('properties')
    markup = f"""
            <div style="width: 20px;
                        height: 20px;
                        border: 1px solid red;
                        border-radius: 10px;
                        background-color: #ff000030;">
            </div>
        </div>
    """
    return {"html": markup}

@st.fragment
def drawMap(location,zoom):
    map = folium.Map(
    location=location, zoom_start=zoom, max_zoom=21)
    st_map= st_folium(
    map,
    width='100%',
    height=400
    )
    st.session_state.location=[st_map['center']['lat'],st_map['center']['lng']]
    st.session_state.zoom=st_map['zoom']
    st.session_state.bounds=st_map['bounds']

#form
comment = st.text_input("Have you ever mapped? Tell us one of your experience. Zoom in the place occured and write your experience there in the text box, then click Submit.", "")

if st.button('Submit'):
    if comment!="":
        st.write("✅You submit the area at coordinate",str(st.session_state.location),'at the zoom of',str(st.session_state.zoom),'with the story of', comment)
        post={'bounds':'POLYGON (('+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+','+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_northEast']['lat'])+','+str(st.session_state.bounds['_northEast']['lng'])+' '+str(st.session_state.bounds['_northEast']['lat'])+','+str(st.session_state.bounds['_northEast']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+','+str(st.session_state.bounds['_southWest']['lng'])+' '+str(st.session_state.bounds['_southWest']['lat'])+'))','comment':comment,'center':'POINT ('+str(st.session_state.location[1])+' '+str(st.session_state.location[0])+')','zoom':st.session_state.zoom}
        collection.insert_one(post)

#referencing


if 'location' not in st.session_state:
    st.session_state.location = [0, 0]
if 'zoom' not in st.session_state:
    st.session_state.zoom = 5
#map
a=drawMap(st.session_state.location,st.session_state.zoom)








