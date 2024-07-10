import streamlit as st
import os
import random
import pandas as pd
import requests
import base64
import json

st.title('Automatic Stock Trader Bot 🧐')
st.subheader('Your One Stop Stock Trading Analysis Bot')

with st.sidebar:
    st.markdown('### Credits')
    st.markdown('- Muneeb A. (Backend Design)')
    st.markdown('- Hurr Shah (Frontend Design)')
    st.markdown('- Adil Usmani (Middleware Design)')

    st.markdown('### Backend Technology')
    st.markdown('- `backtesting` NYSE Top Signals Pick')
    st.markdown('- `fastapi` for Backend Design')
    st.markdown('- `streamlit` for Frontend Design')

    st.markdown('### smaCross (Brief Introduction)')
    introduction = """The SMA (Simple Moving Average) Cross Strategy is a popular and straightforward trading approach utilized in financial markets. This strategy leverages the crossing points of two different SMAs, typically a short-term and a long-term average, to identify potential buy and sell signals. When the short-term SMA crosses above the long-term SMA, it generates a bullish signal, indicating a potential upward trend and a buying opportunity. Conversely, when the short-term SMA crosses below the long-term SMA, it generates a bearish signal, suggesting a potential downward trend and a selling opportunity. This technique helps traders to filter out market noise and make more informed decisions based on the trends indicated by these moving averages. Its simplicity and effectiveness make it a widely used tool among both novice and experienced traders."""
    st.markdown(introduction)

# now we are going to take the stock ticker input

selected_stock = st.selectbox('Select Your Stock Ticker', options=['GOOG', 'APPL', 'TSLA'])
selected_strategy = st.selectbox('Select Your Strategy', options=['smaCross'])

# now we are going to create a slider 

initial_trading_amount = st.slider('Select Your Initial Balance', min_value=500, max_value=1000000)
brokerage_commission = st.slider('Select Your Banks Comission', min_value=2, max_value=5, help='Multiply by 1/100')
is_exclusive = st.checkbox('Order Exclusive', help='Your Orders will be processed instantly instead of a delay.')

st.json(
    {'selected_stock': selected_stock,
    'selected_strategy': selected_strategy,
    'initial_trading_amount': initial_trading_amount,
    'is_exclusive': is_exclusive},

    expanded=False

)

# sending the correct POST request to the server

url = 'https://carter-dense-writing-maintains.trycloudflare.com/'

headers = {
    'accept': 'text/html',
    'Content-Type': 'application/json'
}

data = {
    "symbol": "GOOG",
    "strategy": "SmaCross",
    "commission": brokerage_commission/1000,
    "exclusive_orders": is_exclusive,
    "cash": initial_trading_amount
}

response = requests.put(url, headers=headers, data=json.dumps(data))

file_path = '/home/ubuntu/final/fastapi-demo/templates/SmaCross_plot.html'

# Read the file content
with open(file_path, 'rb') as file:
    file_data = file.read()

# Create a download button
if st.download_button(
    label='Download Report',
    data=file_data,
    file_name='SmaCross_plot.html',
    mime='text/html',
    use_container_width=True
):

    # sending the POST request to the server

    url = 'https://carter-dense-writing-maintains.trycloudflare.com/trade_summary'
    headers = {
        'accept': 'text/html',
        'Content-Type': 'application/json'
    }
    data = {
        "symbol": "GOOG",
        "strategy": "SmaCross",
        "commission": brokerage_commission/1000,
        "exclusive_orders": is_exclusive,
        "cash": initial_trading_amount
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))

    with st.chat_message(name='Goku Super Sayin', avatar='assistant'):
        st.text(response.text.replace('\n', '\t \n'))