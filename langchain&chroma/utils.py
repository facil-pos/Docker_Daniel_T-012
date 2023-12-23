
import os
import streamlit as st
from streamlit_chat import message
import urllib
import chromadb
import tempfile
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings 

FILE_LIST = "archivos.txt"
INDEX_NAME = 'taller'

chroma_client = chromadb.HttpClient(host="host.docker.internal", port=8000)

def save_name_files(path, new_files):

    old_files = load_name_files(path)

    with open(path, "a") as file:
        for item in new_files:
            if item not in old_files:
                file.write(item + "\n")
                old_files.append(item)
    
    return old_files


def load_name_files(path):

    archivos = []
    print("Cargando archivos", archivos)
    with open(path, "r") as file:
        for line in file:
            archivos.append(line.strip())

    return archivos

archivos = load_name_files(FILE_LIST)

def clean_files(path):
    archivos.clear() 
    with open(path, "w") as file:
        pass
    chroma_client.delete_collection(INDEX_NAME)
    chroma_client.create_collection(INDEX_NAME)

    return True

def text_to_chromadb(file):
    print()
    try:
        if type(file) == str:
            if not is_youtube_url(file):
                return False
            print(f"Procesando archivo: {file}")
            loader = YoutubeLoader.from_youtube_url(
                file, add_video_info=True, language="es"
            )
            text = loader.load()
            archivos.append(text[0].metadata["title"])
            save_name_files(FILE_LIST, [f'{text[0].metadata["title"]}'])
            with st.spinner(f'Creando embedding fichero: {text[0].metadata["title"]}'):
                create_embeddings(text[0].metadata["title"], text)
            return True
        elif file.name.endswith(".pdf"):
            print("Procesando archivo")
            with tempfile.TemporaryDirectory() as temp_dir:
                print("Creando archivo temporal")
                temp_filepath = os.path.join(temp_dir, file.name)
                with open(temp_filepath, "wb") as f:
                    f.write(file.read())

                loader = PyPDFLoader(temp_filepath)
                text = loader.load()
                archivos.append(file.name)
                save_name_files(FILE_LIST, [f'{file.name}'])
                with st.spinner(f'Creando embedding fichero: {file.name}'):
                    create_embeddings(file.name, text)
                return True


        # Aquí puedes agregar más condiciones para otros tipos de archivos

        return False  # Retorna False si no es un archivo PDF

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return False


def is_youtube_url(url: str):
    """ Verifica si la cadena proporcionada es una URL de YouTube válida. """
    parsed_url = urllib.parse.urlparse(url)
    print(parsed_url.netloc in ["www.youtube.com", "youtube.com", "youtu.be"])
    return parsed_url.netloc in ["www.youtube.com", "youtube.com", "youtu.be"]


def create_embeddings(file_name, text):
    print(f"Creando embeddings del archivo: {file_name}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len
        )        
    
    chunks = text_splitter.split_documents(text)

    embeddings = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])
    
    Chroma.from_documents(
        chunks,
        embeddings,   
        client=chroma_client,
        collection_name=INDEX_NAME)
        
    return True

def display_msg(msg:str, author:str) -> None:
    """Método para mostrar mensajes en la interfaz de usuario

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state[author].append(msg)
    
    if author == 'past':
        message(msg, is_user=True, key=str(len(st.session_state["past"])) + '_user', avatar_style="thumbs")
    else:
        message(msg, key=str(len(st.session_state["generated"])), avatar_style="fun-emoji")
    