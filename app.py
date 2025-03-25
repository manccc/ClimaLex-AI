#Import all the necessary libraries
import requests
from bs4 import BeautifulSoup
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import google.generativeai as genai
import streamlit as st
import time
import os
from dotenv import load_dotenv
import asyncio
import PyPDF2
import io

# try:
#     asyncio.get_running_loop()
# except RuntimeError:
#     asyncio.set_event_loop(asyncio.new_event_loop())


load_dotenv()
# Load API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
genai.configure(api_key=GEMINI_API_KEY)

# Load Embedding Model
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def search_articles_google(query):
    start_time = time.time()
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_CSE_ID,
        "q": query,
        "num": 5
    }
    response = requests.get(url, params=params)
    latency = time.time() - start_time
    if response.status_code == 200:
        articles = [(result['link'], result['title']) for result in response.json().get("items", [])]
        return articles, latency
    return [], latency
def extract_article_text(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200:
            return ""

        
        if url.endswith(".pdf") or "application/pdf" in response.headers.get("Content-Type", ""):
            return extract_text_from_pdf(response.content)

        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = [p.text for p in soup.find_all('p')]
        return ' '.join(paragraphs)[:3000] 
    
    except Exception as e:
        return f"Error extracting content: {e}"

def extract_text_from_pdf(pdf_content):
    try:
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text[:3000]  
    except Exception as e:
        return f"Error extracting PDF text: {e}"


def summarize_text_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(f"Summarize this article: {text}")
        if hasattr(response, 'text'):
            return response.text.strip()
        return "No summary generated."
    except Exception as e:
        return f"Error: {e}"

def main():
    st.set_page_config(page_title="Insurance & Climate Risk News", page_icon="🌍", layout="wide")
    
    st.markdown(
        """
        <style>
            .main {background-color: #f0f2f6;}
            .stTitle {color: #2c3e50; text-align: center;}
            .stButton button {background-color: #3498db; color: white; font-size: 16px;}
            .stSelectbox div {font-size: 16px;}
        </style>
        """, unsafe_allow_html=True)
    
    st.title("📢 ClimaLex AI ")
    
    with st.sidebar:
        st.header("🔍 Select a News Category")
        categories = {
            "🌱 Climate Risk": "Latest trends in climate risk for insurance",
            "🚀 InsurTech": "Emerging InsurTech innovations and disruptions",
            "📜 Policies & Regulations": "New insurance regulations and climate policies",
            "⚠️ Impactful Events": "Major events affecting insurance and reinsurance",
            "📄 TNFD Reports": "Recent TNFD reports on climate and nature-related risks"
        }
        selected_category = st.selectbox("Choose a category:", list(categories.keys()))
    
    if st.button("📡 Fetch Latest News"):
        st.write(f"### 📰 Fetching articles for **{selected_category}**...")
        
        articles, latency = search_articles_google(categories[selected_category])
        
        if not articles:
            st.warning("⚠️ No relevant articles found. Try a different category.")
            return
        
        st.subheader("📌 Summarized Insights")
        for i, (link, title) in enumerate(articles):
            text = extract_article_text(link)
            summary = summarize_text_gemini(text)
            with st.container():
                st.markdown(f"#### 📄 {title}")
                st.info(summary)
                st.markdown(f"🔗 [Read full article]({link})", unsafe_allow_html=True)
                st.divider()
        
        # KPI Metrics
        st.sidebar.subheader("📊 KPI Metrics")
        st.sidebar.write(f"🔹 Search Latency: {latency:.2f} sec")
        st.sidebar.write(f"🔹 Articles Found: {len(articles)}")
        avg_summary_length = np.mean([len(summarize_text_gemini(extract_article_text(a[0]))) for a in articles])
        st.sidebar.write(f"🔹 Avg. Summary Length: {avg_summary_length:.2f} words")
        feedback = st.sidebar.radio("Was this information useful?", ("Yes", "No"))
        if feedback == "No":
            st.sidebar.text_input("What can be improved?")

if __name__ == "__main__":
    main()
