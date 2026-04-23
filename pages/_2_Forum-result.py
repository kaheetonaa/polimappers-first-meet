import streamlit as st
import pandas as pd
from pymongo import MongoClient

st.set_page_config(layout="wide")
st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css?family=Comfortaa:wght@100&display=swap'); 

    html, body, h1,h2,h3,p{
        font-family: 'Comfortaa', sans-serif; 
        
    }
    div[data-baseweb="select"] > div {
    background-color: #62cbec10;
            color:white;
            font-family: 'Comfortaa', sans-serif;
    }

    body{
        font-size: 18px;
        gap: 20px;
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
            
    .bubble {
  --r: 1em;  /* the radius */
  --t: 1.5em; /* the size of the tail */
  
  max-width: 400px;
  padding: 1em;
  border-inline: var(--t) solid #0000;
  border-radius: calc(var(--r) + var(--t))/var(--r);
  mask: 
    radial-gradient(100% 100% at var(--_p) 0,#0000 99%,#000 102%) 
      var(--_p) 100%/var(--t) var(--t) no-repeat,
    linear-gradient(#000 0 0) padding-box;
  background: #62cbec;
  color: #fff;
}
.left {
  --_p: 0;
  border-bottom-left-radius: 0 0;
  place-self: start;
}
.right {
  --_p: 100%;
  border-bottom-right-radius: 0 0;
  place-self: end;
}
</style>
""", unsafe_allow_html=True)
@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = init_connection()

db=client['rovereto']
collection=db['rovereto-forum']
result=pd.DataFrame(list(collection.find().sort("_id", -1)))

st.title('Domande')

#st.write(result)

for i in range(len(result)):
  comment=result['comment'][i]
  if i % 2:
    st.markdown("""<div class="bubble right">"""+comment+"""</div>""",unsafe_allow_html=True)
  else:
    st.markdown("""<div class="bubble left">"""+comment+"""</div>""",unsafe_allow_html=True)