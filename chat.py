import streamlit as st
import openai
import nltk
import os
import tempfile
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import PyPDF2

# Configuración de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Función para cargar el texto del PDF
def extraer_texto_pdf(archivo):
    texto = ""
    if archivo:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(archivo.read())
            temp_file_path = temp_file.name
        with open(temp_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in range(len(reader.pages)):
                texto += reader.pages[page].extract_text()
        os.unlink(temp_file_path)  # Eliminar el archivo temporal después de usarlo
    return texto

# Función para preprocesar texto
def preprocesar_texto(texto):
    tokens = word_tokenize(texto, language='spanish')
    tokens = [word.lower() for word in tokens if word.isalpha()]
    stopwords_es = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if not word in stopwords_es]
    stemmer = SnowballStemmer('spanish')
    tokens = [stemmer.stem(word) for word in tokens]
    return " ".join(tokens)

# Función para obtener respuesta de OpenAI

def obtener_respuesta(pregunta, modelo="text-davinci-003"):
    client = openai.OpenAI(api_key="TU_OPENAI_API_KEY_AQUÍ")
    respuesta = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": pregunta}],
    )
    return respuesta.choices[0].message.content.strip()

# Interfaz de usuario con Streamlit
def main():
    st.title("Chatbot con OpenAI")

    st.sidebar.header("Cargar Documento PDF")
    archivo_pdf = st.sidebar.file_uploader("Cargar PDF", type='pdf')

    st.sidebar.header("Configuración del Modelo de Lenguaje")
    modelo = st.sidebar.selectbox(
        "Selecciona el modelo de lenguaje de OpenAI",
        ["gpt-3.5-turbo", "davinci-codex", "text-davinci-003"]
    )

    st.sidebar.header("Chatbot")
    pregunta_usuario = st.text_input("Pregunta:")
    enviar_pregunta = st.button("Enviar")

    if enviar_pregunta:
        if archivo_pdf:
            texto_pdf = extraer_texto_pdf(archivo_pdf)
            texto_preprocesado = preprocesar_texto(texto_pdf)
            respuesta = obtener_respuesta(pregunta_usuario + "\n" + texto_preprocesado, modelo=modelo)
            st.text_area("Respuesta:", value=respuesta, height=200)
        else:
            st.warning("Por favor, carga un documento PDF primero.")

if __name__ == "__main__":
    main()
