import json
import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)


# Función para cargar la animación Lottie local (.json o .lottie)
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as source:
            return json.load(source)
    except Exception:
        return None


# Cargar la animación en lugar de la imagen estática
lottie_animation = load_lottie_file("Moods.lottie")

st.title("Análisis de Sentimiento")

# Se muestra la animación Lottie donde antes estaba la imagen
if lottie_animation:
    st_lottie(lottie_animation, height=300, key="cabecera_animada")
else:
    st.info("Carga el archivo 'Moods.lottie' en GitHub para ver la animación.")

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

# Barra lateral informativa
with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.markdown(
        """
    * **Polaridad:** Indica si el sentimiento expresado es positivo, negativo o neutral. 
      Su valor oscila entre **-1** (muy negativo) y **1** (muy positivo), con **0** representando neutralidad.
      
    * **Subjetividad:** Mide cuánto del contenido es subjetivo (opiniones, emociones) frente a objetivo (hechos). 
      Va de **0** (objetivo) a **1** (subjetivo).
    """
    )

# Campo de entrada de texto
text = st.text_area(
    "Escribe tu frase aquí:",
    placeholder="Ejemplo: ¡Hoy es un excelente día para aprender!",
)

if st.button("Analizar Sentimiento", type="primary"):
    if text.strip():
        # Traducción
        trans_text = GoogleTranslator(source="auto", target="en").translate(text)
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.markdown("---")
        st.subheader("Resultados del Análisis")

        col1, col2 = st.columns(2)
        col1.metric("Polaridad", polarity)
        col2.metric("Subjetividad", subjectivity)

        # Respuesta e interacción según el sentimiento
        if polarity > 0.05:
            st.success("¡Es un sentimiento **Positivo**! 😊")
            st.write("¡Sigue propagando esa buena energía!")

        elif polarity < -0.05:
            st.error("Es un sentimiento **Negativo** 😔")
            st.write("Parece un comentario amargo.")

        else:
            st.info("Es un sentimiento **Neutral** 😐")
            st.write("Un mensaje objetivo y neutral.")
    else:
        st.warning("Por favor ingresa un texto válido antes de analizar.")
