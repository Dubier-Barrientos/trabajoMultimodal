import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob

from gtts import gTTS
from googletrans import Translator

selected_page = st.sidebar.radio("Selecciona una opción:", ["Multilenguaje", "Cámara"])

if selected_page == "Multilenguaje":
    st.title("Escucha tu voz en otros idiomas")
    st.subheader("Toca el Botón y habla lo que quires traducir")
    
    
    #image = Image.open('traductor.jpg')
    #st.image(image)

    text=""
    
    stt_button = Button(label=" Graba aquí ", width=300)
    
    stt_button.js_on_event("button_click", CustomJS(code="""
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
     
        recognition.onresult = function (e) {
            var value = "";
            for (var i = e.resultIndex; i < e.results.length; ++i) {
                if (e.results[i].isFinal) {
                    value += e.results[i][0].transcript;
                }
            }
            if ( value != "") {
                document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
            }
        }
        recognition.start();
        """))
    
    result = streamlit_bokeh_events(
        stt_button,
        events="GET_TEXT",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)
    
    if result:
        if "GET_TEXT" in result:
            st.write(result.get("GET_TEXT"))
        try:
            os.mkdir("temp")
        except:
            pass

        translator = Translator()
        
        text = str(result.get("GET_TEXT"))
        in_lang = st.selectbox(
            "Selecciona el lenguaje de Entrada",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Italiano"),
        )
        if in_lang == "Inglés":
            input_language = "en"
        elif in_lang == "Español":
            input_language = "es"
        elif in_lang == "Bengali":
            input_language = "bn"
        elif in_lang == "Coreano":
            input_language = "ko"
        elif in_lang == "Mandarín":
            input_language = "zh-cn"
        elif in_lang == "Japonés":
            input_language = "ja"
        elif in_lang == "Italiano":
            input_language = "it"   
        
        out_lang = st.selectbox(
            "Selecciona el lenguaje de salida",
            ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés", "Italiano"),
        )
        if out_lang == "Inglés":
            output_language = "en"
        elif out_lang == "Español":
            output_language = "es"
        elif out_lang == "Bengali":
            output_language = "bn"
        elif out_lang == "Coreano":
            output_language = "ko"
        elif out_lang == "Mandarín":
            output_language = "zh-cn"
        elif out_lang == "Japonés":
            output_language = "ja"
        elif out_lang == "Italiano":
            output_language = "it"   
        
        def text_to_speech(input_language, output_language, text, tld):
            translation = translator.translate(text, src=input_language, dest=output_language)
            trans_text = translation.text
            tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
            try:
                my_file_name = text[0:20]
            except:
                my_file_name = "audio"
            tts.save(f"temp/{my_file_name}.mp3")
            return my_file_name, trans_text
        
        
        display_output_text = st.checkbox("Mostrar el texto")
        
        if st.button("Traduce tu voz"):
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown(f"## Tú audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
        
            if display_output_text:
                st.markdown(f"#### Texto de salida:")
                st.write(f" {output_text}")
        
        
        def remove_files(n):
            mp3_files = glob.glob("temp/*mp3")
            if len(mp3_files) != 0:
                now = time.time()
                n_days = n * 86400
                for f in mp3_files:
                    if os.stat(f).st_mtime < now - n_days:
                        os.remove(f)
                        print("Deleted ", f)
    
        remove_files(7)

        st.header('También puedes hacer un análisis de sentimiento')
        if text:
            if st.button("Analizar"):
                translation = translator.translate(text, src="es", dest="en")
                trans_text = translation.text
                blob = TextBlob(trans_text)
                st.write('Polarity: ', round(blob.sentiment.polarity,2))
                st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
                x=round(blob.sentiment.polarity,2)
                if x >= 0.5:
                    st.write( 'Es un sentimiento Positivo 😊')
                elif x <= -0.5:
                    st.write( 'Es un sentimiento Negativo 😔')
                else:
                    st.write( 'Es un sentimiento Neutral 😐')

elif selected_page == "Cámara":
    st.write("hello")
    
