import streamlit as st
import os
from utils import *
from langchainModel import LangchainModel


from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

st.set_page_config('preguntaDOC')
st.header("Pregunta a tus documentos")

LangchainModel.initialize_model()

with st.sidebar:
    
    st.subheader("Carga tus documentos")
    files_uploaded = st.file_uploader(
        "Carga tu archivo",
        type="pdf",
        accept_multiple_files=True
        )
    
    
    input_url_video = st.text_input("URL del video", key="url")
    
    if st.button('Procesar'):
        if files_uploaded:
            for pdf in files_uploaded:
                if pdf is not None and pdf.name not in archivos:
                    text_to_chromadb(pdf)
        elif input_url_video:
            text_to_chromadb(input_url_video)
            print('url', input_url_video)
        else:
            st.warning('No hay archivos cargados')
        
    print('archivos antes de eliminar', archivos)
    if len(archivos) > 0:
        st.write("Archivos cargados:")
        lista_documentos = st.empty()
        with lista_documentos.container():
            for arch in archivos:
                st.write(arch)
            if st.button('Borrar documentos'):
                clean_files(FILE_LIST)
                print('archivos', archivos)
                lista_documentos.empty()

# Initialize conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey! 👋"]
    
for i in range(len(st.session_state['generated'])):
    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
    message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")


if archivos:
    user_question = st.chat_input("Say something")
    if user_question:

        display_msg(user_question, 'past')
        respuesta = LangchainModel.query(user_question, st.session_state['history'])
        print('respuesta', respuesta)
        display_msg(respuesta, 'generated')
        print('memoria chat', st.session_state['history'])
