import streamlit as st
import feedparser
from datetime import datetime, timedelta
from googletrans import Translator

# 번역기 초기화
translator = Translator()

def get_news(ticker, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Google News RSS 피드 URL
    url = f"https://news.google.com/rss/search?q={ticker}+when:{start_date.strftime('%Y-%m-%d')}:{end_date.strftime('%Y-%m-%d')}&hl=en-US&gl=US&ceid=US:en"
    
    # RSS 피드 파싱
    feed = feedparser.parse(url)
    
    # 최대 5개의 뉴스 항목 반환
    return feed.entries[:5]

def summarize_news(articles):
    summaries = []
    for article in articles:
        title = article.title
        summary = article.summary
        full_summary = f"{title}\n{summary}"
        summaries.append(full_summary)
    return "\n\n".join(summaries)

def translate_to_korean(text):
    return translator.translate(text, dest='ko').text

# Streamlit 앱
st.title('주식 뉴스 요약 앱')

ticker = st.text_input('주식 티커 입력 (예: AAPL)')
period = st.selectbox('기간 선택', ['1일', '1주일', '1달'])

if st.button('뉴스 가져오기'):
    if ticker:
        days = {'1일': 1, '1주일': 7, '1달': 30}[period]
        news = get_news(ticker, days)
        if news:
            summary = summarize_news(news)
            translated_summary = translate_to_korean(summary)
            st.write(translated_summary)
        else:
            st.write('뉴스를 찾을 수 없습니다.')
    else:
        st.write('티커를 입력해주세요.')
