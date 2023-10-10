import streamlit as st
import sounddevice as sd
import numpy as np
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Configura la autenticación de Google Cloud
# Aquí debes configurar las credenciales de tu cuenta de Google Cloud

st.title("Grabación de Audio y Reconocimiento de Voz")

# Función para grabar audio
def record_audio():
    st.subheader("Grabación de Audio")
    with st.spinner("Grabando..."):
        duration = 10  # Duración de la grabación en segundos
        audio_data = sd.rec(int(duration * 44100), samplerate=44100, channels=1)
        sd.wait()
        st.success("Grabación completa")
        return audio_data

# Función para transcribir audio a texto
def transcribe_audio(audio_data):
    st.subheader("Transcripción de Audio a Texto")
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(content=audio_data.tobytes())

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="es-MX",  # Cambia a tu idioma preferido
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript

if st.button("Iniciar Grabación"):
    audio_data = record_audio()
    transcript = transcribe_audio(audio_data)
    st.subheader("Texto Transcrito:")
    st.write(transcript)
