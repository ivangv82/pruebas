import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("Cierre al 30-abril-2025")

# 1) Define tus universos
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']
# Quita duplicados
TICKERS = list(dict.fromkeys(STOCKS + BONDS))

# 2) Función cacheada para descargar un único día
@st.cache_data
def fetch_close_for_date(tickers, date):
    start = date.strftime("%Y-%m-%d")
    end   = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    df = yf.download(
        tickers,
        start=start,
        end=end,
        interval="1d",
        progress=False,
        auto_adjust=False
    )["Close"]
    return df

# 3) Llama a la función
fecha_obj = datetime(2025, 4, 30)
df = fetch_close_for_date(TICKERS, fecha_obj)

# 4) Comprueba resultado y muestra
if df.empty:
    st.error("❌ No se descargaron datos para el 2025-04-30.")
else:
    # Puede que el índice no se llame exactamente "2025-04-30", así que cogemos la fila 0
    precios = df.iloc[0].round(4)
    st.write(f"📅 Cierre al {fecha_obj.strftime('%Y-%m-%d')}")
    st.dataframe(precios.to_frame("Close").T)
