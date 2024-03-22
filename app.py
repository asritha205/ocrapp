# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:54:17 2024

@author: LENOVO
"""

import streamlit as st
import numpy as np
import pytesseract
import cv2
from googletrans import Translator
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

language_mapping = {
    'tel': 'te',  # Telugu
    'hin': 'hi',  # Hindi
    'tam': 'ta',  # Tamil
    'ben': 'bn',  # Bengali
    'kan': 'kn',  # Kannada
    'mal': 'ml',  # Malayalam
    'mar': 'mr',  # Marathi
    'guj': 'gu',  # Gujarati
    'pan': 'pa',  # Punjabi
    'urd': 'ur',  # Urdu
    'san': 'sa',  # Sanskrit
    'asm': 'as',  # Assamese
    'nep': 'ne',  # Nepali
    'snd': 'sd',  # Sindhi
    'kok': 'kok',  # Konkani
    'doi': 'doi',  # Dogri
    'mni': 'mni',  # Manipuri
    'kas': 'ks',  # Kashmiri
    'brx': 'brx',  # Bodo
    'eng': 'en', #english
    'mai': 'mai',  # Maithili
    'fra': 'fr',  # French
    'spa': 'es',  # Spanish
    'deu': 'de',  # German
    'zho': 'zh-CN',  # Chinese (Simplified)
    'jpn': 'ja',  # Japanese
    'ara': 'ar',  # Arabic
    'rus': 'ru',  # Russian
    'por': 'pt',  # Portuguese
    'ita': 'it',  # Italian
    'kor': 'ko',  # Korean
    'dut': 'nl',  # Dutch
    'swe': 'sv',  # Swedish
    'tur': 'tr',  # Turkish
    'pol': 'pl',  # Polish
    'vie': 'vi',  # Vietnamese
    'gre': 'el',  # Greek
    'tha': 'th',  # Thai
    'ind': 'id',  # Indonesian
    'may': 'ms',  # Malay
    'fil': 'fil',  # Filipino
}

st.title("OCR Based Multi Lingual Text Extraction and Machine Translation")
st.text("Developed by Batch - 11")

def save_captured_image(img_bytes):
  img_arr = np.frombuffer(img_bytes, np.uint8)
  img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
  cv2.imwrite("captured_image.jpg", img)

def preprocess(img):
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(gray, 100, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)[1]
    return img

def text_extract(img, lan, slang, dlang):
    # Load the image
    gray = preprocess(img)
    text = pytesseract.image_to_string(img, lang=lan)
    if not text:
        return "Text not found"
    translator = Translator()
    try:
        translated = translator.translate(text, src=slang, dest=dlang)
        translated_text = translated.text
    except Exception as e:
        print("Translation error:", e)
        translated_text = "Translation error occurred"
    
    return translated_text
    

uploaded_file = st.file_uploader("Choose a file")
picture = st.camera_input("Take a Picture")
option1 = st.selectbox('Source Language' , ('tel', 'hin', 'tam', 'ben', 'kan', 'mal', 'mar', 'guj', 'pan', 'urd', 'san', 'asm', 'nep', 'snd', 'kok', 'doi', 'mni', 'kas', 'brx', 'eng', 'mai', 'fra', 'spa', 'deu', 'zho', 'jpn', 'ara', 'rus', 'por', 'ita', 'kor', 'dut', 'swe', 'tur', 'pol', 'vie', 'gre', 'tha', 'ind', 'may', 'fil'))
option2 = st.selectbox('Desired Language' , ('tel', 'hin', 'tam', 'ben', 'kan', 'mal', 'mar', 'guj', 'pan', 'urd', 'san', 'asm', 'nep', 'snd', 'kok', 'doi', 'mni', 'kas', 'brx', 'eng', 'mai', 'fra', 'spa', 'deu', 'zho', 'jpn', 'ara', 'rus', 'por', 'ita', 'kor', 'dut', 'swe', 'tur', 'pol', 'vie', 'gre', 'tha', 'ind', 'may', 'fil'))
slang = language_mapping.get(option1)
dlang = language_mapping.get(option2)
if picture:
  save_captured_image(picture.read())
  st.success("Image saved as captured_image.jpg")
  img = cv2.imread('captured_image.jpg')
  text = text_extract(img, option1, slang, dlang)
  st.write(text)
elif uploaded_file:
    img = Image.open(uploaded_file)
    text = text_extract(img, option1, slang, dlang)
    st.write(text)
