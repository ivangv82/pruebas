import streamlit as st
import yfinance as yf

st.write("Versions:", yf.__version__)
df = yf.download("SPY", period="5d", interval="1d", progress=False, auto_adjust=False)["Close"]
if df.empty:
    st.error("No data")
else:
    st.dataframe(df)
