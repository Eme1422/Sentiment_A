from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from deep_translator import GoogleTranslator

st.title('Análisis de Sentimiento')

image = Image.open('emoticones.jpg')
st.image(image)

st.subheader("Por favor escribe en el campo de texto la frase que deseas analizar")

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")

    st.write("""
    Polaridad: Indica si el sentimiento expresado en el texto es positivo,
    negativo o neutral. Su valor oscila entre -1 (muy negativo) y 1
    (muy positivo), con 0 representando un sentimiento neutral.

    Subjetividad: Mide cuánto del contenido es subjetivo (opiniones,
    emociones, creencias) frente a objetivo (hechos). Va de 0 a 1,
    donde 0 es completamente objetivo y 1 es completamente subjetivo.
    """)

with st.expander('Analizar texto'):

    text = st.text_input('Escribe por favor: ')

    if text:

        # Traducción del español al inglés
        trans_text = GoogleTranslator(
            source='es',
            target='en'
        ).translate(text)

        # Análisis del sentimiento
        blob = TextBlob(trans_text)

        polarity = round(blob.sentiment.polarity, 2)
        subjectivity = round(blob.sentiment.subjectivity, 2)

        st.write('Polarity: ', polarity)
        st.write('Subjectivity: ', subjectivity)

        # Clasificación del sentimiento
        if polarity > 0:
            st.write('Es un sentimiento Positivo 😊')

        elif polarity < 0:
            st.write('Es un sentimiento Negativo 😔')

        else:
            st.write('Es un sentimiento Neutral 😐')
