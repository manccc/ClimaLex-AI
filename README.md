# ClimaLex-AI
### _Overview_
This project is a news aggregation and summarization tool that fetches and summarizes the latest articles related to climate risk, InsurTech, policies, and impactful events in the insurance and reinsurance sector. The system extracts relevant insights from legitimate online sources and presents them in a structured report format.

## _Features_:
* Web Scraping: Uses Google Custom Search API and BeautifulSoup to extract news articles.
* Text Summarization: Utilizes Google Gemini API for AI-driven article summarization.
* UI with Streamlit: A visually appealing dashboard for easy navigation.
* KPI Metrics: Displays relevant performance metrics like search latency, article count, and average summary length.

## _Technologies Used_:
* Python
* Streamlit (UI Framework)
* BeautifulSoup (Web Scraping)
* Google Custom Search API (Article discovery)
* Google Gemini API (Summarization)
* FAISS (Vector Search for embedding-based similarity)
* Sentence Transformers (Text embedding)

### _Installation_

Clone the repository:
```bash
git clone https://github.com/manccc/ClimaLex-AI
cd ClimaLex-AI
```
Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### _Install dependencies_:
```bash
pip install -r requirements.txt
```
Create a .env file and add your API keys:
```bash
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_CSE_ID=your_google_cse_id
```
Usage
Run the Streamlit application:
```bash
streamlit run app.py
```
### _How It Works_:
1. User selects a category (Climate Risk, InsurTech, Policies, Impactful Events).
2. Google Custom Search API fetches the latest articles.
3. BeautifulSoup extracts the article text.
4. Gemini API summarizes the content.
5. Summaries and article links are displayed in the UI.
6. KPI Metrics provide insights into model performance.

### Key Performance Indicators (KPIs)
* Search Latency: Time taken to fetch articles.
* Number of Articles Retrieved.
* Average Summary Length.
* User Feedback on Summary Quality.

### Outputs and Reports
* The tool generates a structured report with article summaries and links to full sources.
* If the article is in PDF format, it extracts the text and summarizes it.
* Reports can be exported in JSON or CSV format for further analysis.

### Future Enhancements
* Improved PDF Parsing: Handling complex PDF layouts.
* Multilingual Support.
* Integration with News APIs beyond Google Custom Search.
