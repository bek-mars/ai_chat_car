import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import streamlit as st
import json
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))

def load_data():
    path = "info_data.json"
    if not os.path.exists(path):
        st.error(" Файл базы знаний не найден! Убедитесь, что 'info_data.json' существует.")
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    processed_tokens = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            lemma = lemmatizer.lemmatize(token)
            processed_tokens.append(lemma)
    return processed_tokens

def find_answer(question, knowledge_base):
    processed_question = preprocess_text(question)
    best_match = None
    max_score = 0

    for category, subcategories in knowledge_base.items():
        for subcategory, data in subcategories.items():
            keywords = data.get("keywords", [])
            score = sum(1 for keyword in keywords if keyword in processed_question)

            if score > max_score:
                max_score = score
                best_match = data.get("response")

    return best_match if max_score > 0 else " Извините, я не смог найти информацию об этой машине."

st.set_page_config(page_title="Car Info Bot ", page_icon="🚘")

st.title("Информационный бот о машинах")
st.markdown("Введите название автомобиля, чтобы получить его характеристики:")

knowledge_base = load_data()

prompt = st.text_input("Например: Toyota Camry, BMW X5, Tesla Model 3...")

if prompt:
    response = find_answer(prompt, knowledge_base)
    st.markdown("###  Результат:")
    st.info(response)

st.markdown("---")

