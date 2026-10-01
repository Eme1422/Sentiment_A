import json
import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image
from streamlit_lottie import st_lottie
from textblob import TextBlob

# Configuración inicial de la página
st.set_page_config(
    page_title="Análisis de Sentimiento", page_icon="🎭", layout="centered"
)


# Función para cargar la animación local Lottie (.json o .lottie)
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as source:
            return json.load(source)
    except FileNotFoundError:
        return None
    except Exception:
        # En caso de que el archivo .lottie no sea un JSON directo
        return None


# Cargar tu animación 'Moods.lottie'
lottie_animation = load_lottie_file("Moods.lottie")

st.title("Análisis de Sentimiento con Interacción 🎭")

# Mostrar la animación principal arriba
if lottie_animation:
    st_lottie(lottie_animation, height=250, key="moods_anim")

# Intentar cargar la imagen de encabezado si existe
try:
    image = Image.open("emoticones.jpg")
    st.image(image, use_container_width=True)
except FileNotFoundError:
    pass

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

# Área de entrada de texto
text = st.text_area(
    "Escribe tu frase aquí:",
    placeholder="Ejemplo: ¡Hoy es un excelente día para aprender!",
)

if st.button("Analizar Sentimiento", type="primary"):
    if text.strip():
        # Traducción con deep-translator (evita errores en la nube)
        trans_text = GoogleTranslator(source="auto", target="en").translate(text)
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.markdown("---")
        st.subheader("Resultados del Análisis")

        col1, col2 = st.columns(2)
        col1.metric("Polaridad", polarity)
        col2.metric("Subjetividad", subjectivity)

        # Respuestas interactivas según el análisis
        if polarity > 0.05:
            st.success("¡Es un sentimiento **Positivo**! 😊")
            st.write("¡Excelente! El mensaje transmite una buena vibra.")

        elif polarity < -0.05:
            st.error("Es un sentimiento **Negativo** 😔")
            st.write("El mensaje contiene una carga negativa o crítica.")

        else:
            st.info("Es un sentimiento **Neutral** 😐")
            st.write("Es un mensaje informativo o sin sesgo emocional.")
    else:
        st.warning("Por favor ingresa un texto válido antes de analizar.")
        
