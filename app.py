import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from googletrans import Translator

# 번역기 초기화
translator = Translator()

def get_news(ticker, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    url = f"https://www.marketwatch.com/investing/stock/{ticker}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        news_items = soup.find_all('div', class_='article__content')
        
        filtered_news = []
        for item in news_items[:5]:  # 최대 5개의 뉴스 항목만 가져옵니다
            title = item.find('a', class_='link').text.strip()
            summary = item.find('p', class_='article__summary').text.strip()
            filtered_news.append({"title": title, "summary": summary})
        
        return filtered_news
    except requests.RequestException as e:
        st.error(f"뉴스를 가져오는 중 오류가 발생했습니다: {str(e)}")
        return []

def summarize_news(articles):
    summaries = []
    for article in articles:
        title = article['title']
        summary = article['summary']
        full_summary = f"{title}\n{summary}"
        summaries.append(full_summary)
    return "\n\n".join(summaries)

def translate_to_korean(text):
    try:
        return translator.translate(text, dest='ko').text
    except Exception as e:
        st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
        return text

# Streamlit 앱
st.title('주식 뉴스 요약 앱')

ticker = st.text_input('주식 티커 입력 (예: AAPL)')
period = st.selectbox('기간 선택', ['1일', '1주일', '1달'])

if st.button('뉴스 가져오기'):
    if ticker:
        days = {'1일': 1, '1주일': 7, '1달': 30}[period]
        with st.spinner('뉴스를 가져오는 중...'):
            news = get_news(ticker, days)
        if news:
            summary = summarize_news(news)
            with st.spinner('뉴스를 번역하는 중...'):
                translated_summary = translate_to_korean(summary)
            st.write(translated_summary)
        else:
            st.warning('뉴스를 찾을 수 없습니다. 다른 티커를 입력해 보세요.')
    else:
        st.warning('티커를 입력해주세요.')
