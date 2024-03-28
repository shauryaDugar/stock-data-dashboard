import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.express as px
import plotly.graph_objects as go

# title for the web app
st.title('Stock Dashboard')

# sidebar components - include a ticker, start and end date
ticker = st.sidebar.text_input('Ticker', value="AAPL")
start_date = st.sidebar.date_input('Start Date', value=datetime.datetime(2024, 1, 1))
end_date = st.sidebar.date_input('End Date')
# slider = st.sidebar.slider('NEW Slider')


# downloading stock data from yfinance into data (a pd dataframe)
data = yf.download(ticker, start=start_date, end=end_date)

# selector for the type of chart to display
chart_types = ('candlestick', 'ohlc', 'low', 'high')
chart_selector = st.selectbox(label='Chart Type', options=chart_types)
if chart_selector == 'candlestick':
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='green',
                decreasing_line_color='red'
                )], layout=go.Layout(title=ticker))
elif chart_selector == 'ohlc':
    fig = go.Figure(data=go.Ohlc(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close']),
                    layout=go.Layout(title=ticker))
elif chart_selector == 'low':
    fig = px.line(data, x=data.index, y=data['Low'], title=ticker)
elif chart_selector == 'high':
    fig = px.line(data, x=data.index, y=data['High'], title=ticker)

st.plotly_chart(fig)

# adding additional tabs to page
pricing_data, fundamental_data, news = st.tabs(['Pricing', 'Fundamentals', 'News'])

# pricing data tab - contains historical prices
with pricing_data:
    st.header('Price Movements')

    st.subheader('Historical Prices')
    st.write(data)

# fundamentals tab - contains fundamental details of stocks like the location, stock market, dividend yield, etc.
with fundamental_data:
    st.header('Fundamentals of Stock')

    # explore what other info is accessible thru yfinance
    info = yf.Ticker(ticker).info

    st.subheader('Company Information')
    st.write(f"**Name:** {info['longName']}")
    st.write(f"**Sector:** {info['sector']}")
    st.write(f"**Industry:** {info['industry']}")
    st.write(f"**Country:** {info['country']}")

    st.subheader('Key Metrics')
    st.write(f"**Market Cap:** {info['marketCap']}")
    st.write(f"**Forward P/E:** {info['forwardPE']}")
    st.write(f"**EPS (TTM):** {info['trailingEps']}")
    st.write(f"**Dividend Yield:** {info['dividendYield']}")

# stocknews library can be used to pick out most recent news for the ticker
from stocknews import StockNews

# news tab to display news title, summary, date, and sentiments
with news:
    st.title(f'News of {ticker}')  
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.markdown("---")  # Add a horizontal line between each news piece
        st.subheader(f'News {i+1}')
        st.write(f"**Published Date:** {df_news['published'][i]}")
        st.write(f"**Title:** {df_news['title'][i]}")
        st.write(f"**Summary:** {df_news['summary'][i]}")
        title_sentiment = df_news['sentiment_title'][i]
        news_sentiment = df_news['sentiment_summary'][i]
        # Adding color to sentiment based on positivity/negativity
        title_sentiment_text = "Positive" if title_sentiment > 0 else "Negative" if title_sentiment < 0 else "Neutral"
        news_sentiment_text = "Positive" if news_sentiment > 0 else "Negative" if news_sentiment < 0 else "Neutral"
        sentiment_color = "green" if title_sentiment > 0 else "red" if title_sentiment < 0 else "blue"
        st.write(f'**Title Sentiment:** <span style="color:{sentiment_color}">{title_sentiment_text}</span>', unsafe_allow_html=True)
        sentiment_color = "green" if news_sentiment > 0 else "red" if news_sentiment < 0 else "blue"
        st.write(f'**News Sentiment:** <span style="color:{sentiment_color}">{news_sentiment_text}</span>', unsafe_allow_html=True)
