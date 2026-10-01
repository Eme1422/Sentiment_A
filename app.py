import pandas as pd
import requests
import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="😊", layout="centered"
)

# Función para cargar animaciones Lottie desde URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# URLs de las animaciones Lottie
LOTTIE_POSITIVE = "https://assets2.lottiefiles.com/packages/lf20_tpb93910.json"
LOTTIE_NEGATIVE = "https://assets9.lottiefiles.com/packages/lf20_9xR83L.json"
LOTTIE_NEUTRAL = "https://assets10.lottiefiles.com/packages/lf20_f333a92p.json"

lottie_pos = load_lottieurl(LOTTIE_POSITIVE)
lottie_neg = load_lottieurl(LOTTIE_NEGATIVE)
lottie_neu = load_lottieurl(LOTTIE_NEUTRAL)

st.title("Análisis de Sentimiento con Interacción 🎭")

try:
    image = Image.open("emoticones.jpg")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# Barra lateral
with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.markdown(
        """
    * **Polaridad:** Indica si el sentimiento es positivo, negativo o neutral. 
      Su valor oscila entre **-1** (muy negativo) y **1** (muy positivo), con **0** representando un sentimiento neutral.
      
    * **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones) frente a objetivo (hechos). 
      Va de **0** (completamente objetivo) a **1** (completamente subjetivo).
    """
    )

# Campo de texto e interacción
text = st.text_area("Escribe tu frase aquí:", placeholder="Ejemplo: ¡Hoy es un excelente día para aprender!")

if st.button("Analizar Sentimiento", type="primary"):
    if text.strip():
        # Traducción con deep-translator
        trans_text = GoogleTranslator(source="auto", target="en").translate(text)
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.markdown("---")
        st.subheader("Resultados del Análisis")

        col1, col2 = st.columns(2)
        col1.metric("Polaridad", polarity)
        col2.metric("Subjetividad", subjectivity)

        if polarity > 0.05:
            st.success("¡Es un sentimiento **Positivo**! 😊")
            st.write("¡Sigue propagando esa buena energía!")
            if lottie_pos:
                st_lottie(lottie_pos, height=200, key="positive_anim")

        elif polarity < -0.05:
            st.error("Es un sentimiento **Negativo** 😔")
            st.write("Parece un comentario amargo. ¡Espero que las cosas mejoren pronto!")
            if lottie_neg:
                st_lottie(lottie_neg, height=200, key="negative_anim")

        else:
            st.info("Es un sentimiento **Neutral** 😐")
            st.write("Un mensaje objetivo y sin sesgos emocionales.")
            if lottie_neu:
                st_lottie(lottie_neu, height=200, key="neutral_anim")
    else:
        st.warning("Por favor ingresa un texto válido antes de analizar.")
