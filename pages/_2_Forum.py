import streamlit as st
from pymongo import MongoClient
st.set_page_config(
  page_title="🌐 Rovereto quizz",
  page_icon="❓",
  layout="wide"
)
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
    
    div[data-testid='stVerticalBlockBorderWrapper']{
        background-color: #ffffffC0;
    }
            .center {
    display: block;
    margin-left: auto;
    margin-right: auto;
        width:200px;
            }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    return MongoClient("mongodb+srv://kuquanghuy:quanghuy123456@cluster0.6mzug.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = init_connection()

db=client['rovereto']
collection=db['rovereto-forum']
st.title('mappatura del territorio in caso di calamità ?')
container1 = st.container()
def submit_answer():
        if (comment!=""):
                st.write(comment)
                post={'comment':comment}
                collection.insert_one(post)
                st.session_state.answer_submitted=True
                st.write(st.session_state.answer_submitted)
        else:
                st.warning('Nessuna domanda scritta!')
with container1:
    st.markdown(""" ___""")
    if "answer_submitted" not in st.session_state:
        comment = st.text_input("Domanda per la mappatura del territorio in caso di calamità ?", "")
        st.button('Consegna', on_click=submit_answer)
    else:
        st.balloons()
        st.write('Hai consegnato la domanda!')

        




