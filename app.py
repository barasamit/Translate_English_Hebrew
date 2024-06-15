import streamlit as st
import pytesseract
from googletrans import Translator
from PIL import Image
from gtts import gTTS
import io

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def translate_text(word, dest_language='he'):
    translator = Translator()
    translated = translator.translate(word, dest=dest_language)
    return translated.text

def text_to_audio(word):
    tts = gTTS(text=word, lang='en')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

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
            extracted_text = extract_text_from_image(image)
            words = extracted_text.split()
            if words:
                st.write("נתרגם קצת מילים לעברית:")
                for word in words:
                    if word.isalpha() and word.isascii() and not word.isupper():
                        hebrew_translation = translate_text(word)
                        audio_buffer = text_to_audio(word)
                        if word.lower() == hebrew_translation.lower():
                            continue
                        st.write(f"{word} -> {hebrew_translation}")
                        st.audio(audio_buffer, format='audio/mp3')
            else:
                st.write("No words detected in the image.")

if __name__ == "__main__":
    main()
