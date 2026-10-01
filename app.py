import pandas as pd
import requests
import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)


# Función para cargar animaciones Lottie vía URL JSON
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Animación en la cabecera que reemplaza a la imagen 'emoticones.jpg'
lottie_main = load_lottieurl(
    "https://assets10.lottiefiles.com/packages/lf20_f333a92p.json"
)

st.title("Análisis de Sentimiento 🎭")

# Se muestra la animación Lottie en la parte superior
if lottie_main:
    st_lottie(lottie_main, height=250, key="cabecera_animada")

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# Barra lateral informativa
with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.markdown(
        """
    * **Polaridad:** Indica si el sentimiento es positivo, negativo o neutral. 
      Su valor oscila entre **-1** (muy negativo) y **1** (muy positivo), con **0** representando neutralidad.
      
    * **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones) frente a objetivo (hechos). 
      Va de **0** (completamente objetivo) a **1** (completamente subjetivo).
    """
    )

# Entrada de texto del usuario
text = st.text_area(
    "Escribe tu frase aquí:",
    placeholder="Ejemplo: ¡Hoy es un excelente día para aprender Python!",
)

# Botón de análisis e interacción
if st.button("Analizar Sentimiento", type="primary"):
    if text.strip():
        # Traducción e inferencia de sentimiento con TextBlob
        trans_text = GoogleTranslator(source="auto", target="en").translate(text)
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.markdown("---")
        st.subheader("Resultados del Análisis")

        # Visualización de métricas
        col1, col2 = st.columns(2)
        col1.metric("Polaridad", polarity)
        col2.metric("Subjetividad", subjectivity)

        # Lógica de respuesta e interacción
        if polarity > 0.05:
            st.success("¡Es un sentimiento **Positivo**! 😊")
            st.write("¡Sigue propagando esa buena energía!")

        elif polarity < -0.05:
            st.error("Es un sentimiento **Negativo** 😔")
            st.write("Parece un comentario amargo. ¡Ánimo!")

        else:
            st.info("Es un sentimiento **Neutral** 😐")
            st.write("Un mensaje objetivo y sin sesgos emocionales.")
    else:
        st.warning("Por favor ingresa un texto válido antes de analizar.")
