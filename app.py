import streamlit as st
import pytesseract
from googletrans import Translator
from PIL import Image
from gtts import gTTS
import base64
import time

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def translate_text(word, dest_language='he'):
    translator = Translator()
    translated = translator.translate(word, dest=dest_language)
    return translated.text

def text_to_audio(word):
    tts = gTTS(text=word, lang='en')
    audio_file = f"{word}.mp3"
    tts.save(audio_file)
    return audio_file

def get_audio_player_html(audio_file):
    with open(audio_file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        return f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """

def main():
    st.set_page_config(page_title="Text Extraction and Translation", layout="wide")
    st.title("עפרי פלדמן תרגומים")
    st.write("זרקי פה תמונה ואני אתרגם לך מילים מאנגלית לעברית!")

    uploaded_file = st.file_uploader("תבחרי תמונה...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', width=500)  # Set a fixed width for the image
        st.write("מחלץ מילים, לפעמים לא הולך הכי טוב אבל זה מה יש")
        with st.spinner('מפעיל את כוח המחשבה'):
            time.sleep(1)
            extracted_text = extract_text_from_image(image)
            words = extracted_text.split()
            if words:
                st.write("נתרגם קצת מילים לעברית:")
                for word in words:
                    if word.isalpha() and word.isascii() and not word.isupper():
                        hebrew_translation = translate_text(word)
                        audio_file = text_to_audio(word)
                        audio_html = get_audio_player_html(audio_file)
                        if word.lower() == hebrew_translation.lower():
                            continue
                        st.write(f"{word} -> {hebrew_translation}")
                        st.markdown(audio_html, unsafe_allow_html=True)
            else:
                st.write("No words detected in the image.")

if __name__ == "__main__":
    main()
