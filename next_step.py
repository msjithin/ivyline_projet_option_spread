import pandas as pd
import pandas_datareader.data as web
import numpy as np
import streamlit as st
import requests, time, re, pickle
import config 

instrument_url = 'https://api.tdameritrade.com/v1/instruments'
option_url = 'https://api.tdameritrade.com/v1/marketdata/chains'

symbols = ['AAPL', 'FB']


def get_fundamentals(ticker=""):
    start, end = 0, 500
    
    payload = {'apikey':st.secrets.td_credentials.ameritrade_key,
            'symbol':ticker,
            'projection':'fundamental'
            }
    results = requests.get(instrument_url, params=payload)
    data = results.json()
    return data
       
def get_option_data(ticker=""):
    start, end = 0, 500
    
    payload = {'apikey':ameritrade_key,
            'symbol':ticker,
            'contractType' : 'CALL',
            'strikeCount' : 2,
            'includeQuotes' : True,
            'strategy' :'ANALYTICAL'
            }
    results = requests.get(option_url, params=payload)
    data = results.json()
    return data

def check_nested_dict(d):
    return any(isinstance(i,dict) for i in d.values())

def write_on_page():
    pass
def fundamental(stock_name=""):
    if stock_name is None:
        return
    option_data = get_fundamentals(stock_name)
    
    for key, value in option_data.items():
        if type(value)!=dict or check_nested_dict(value)==False :
            st.markdown("{}  :  {} ".format(key, value))    
        else:
            st.markdown("{}".format(key))
            for k, v in value.items():
                st.markdown("{}  :  {} ".format(k, v))  


def option_data(stock_name=""):
    if stock_name is None:
        return
    option_data = get_option_data(stock_name)
    
    for key, value in option_data.items():
        if type(value)!=dict or check_nested_dict(value)==False :
            st.markdown("{}  :  {} ".format(key, value))    
        else:
            st.markdown("{}".format(key))
            for k, v in value.items():
                if type(value)!=dict or check_nested_dict(value)==False :
                    st.markdown("{}  :  {} ".format(k, v))  
                else:
                    st.markdown("{}".format(k))
                    for ki, vi in v.items():
                        st.markdown("{}  :  {} ".format(ki, vi))   
def app():
    st.title("Stock informaton")
    stock_name = st.text_input("Ticker symbol", 'AAPL')
    data_type = st.radio("What do you want to see? ", ('Fundamentals', 'Option data'))
    if data_type == 'Fundamentals':
        fundamental(stock_name)
    else:
        option_data(stock_name)