import requests
import urllib.request
import time
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
import nltk
import pandas
import streamlit as st
from streamlit_lottie import st_lottie

nltk.download('punkt')

def get_lowest_ask(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_range = soup.find_all("meta", property='og:price:amount')[0]['content']
    lowest_ask = float(nltk.word_tokenize(price_range)[2])
    return(lowest_ask)

def pnl(purchase, curr):
    if purchase==0:
        return 0
    else:
        return (curr-purchase)

def pct_chge(chng, purchase):
    if purchase==0:
        return 0
    else:
        return (chng/purchase*100)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_url = "https://assets5.lottiefiles.com/packages/lf20_oKu1nU.json"
lottie_json = load_lottieurl(lottie_url)

# st.header('Live Price Check')

# # player_url = 'https://www.nbatopshot.com/listings/p2p/122b048d-585e-4c63-8275-c23949576fd6+d7a764a7-a397-4c5e-98a3-0a69c9406011'

# player_url = st.text_input('player url', 'https://www.nbatopshot.com/listings/p2p/122b048d-585e-4c63-8275-c23949576fd6+d7a764a7-a397-4c5e-98a3-0a69c9406011')
# if st.button('Get Price'):
#     st.write('Current price: ', get_lowest_ask(player_url))

st.header('Seeing Stars 2')

df = pd.read_excel('LeBron_SS.xlsx', header=1, engine='openpyxl').loc[:11]
df = df[df.columns[:-3]]

df['live_price'] = df.apply(lambda x:  get_lowest_ask(x['Topshot']), axis=1)
df['price change'] = df.apply(lambda x: pnl(x['Purchase  price'], x['live_price']), axis=1)
df['% change'] = df.apply(lambda x: pct_chge(x['price change'], x['Purchase  price']), axis=1)
#
st.write('Current live PNL ($): ', df['price change'].sum())
#
df[['Player', 'Purchase  price', 'live_price']]

st_lottie(lottie_json)
