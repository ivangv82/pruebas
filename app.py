import streamlit as st
from datetime import datetime
import yfinance as yf

# 1. Definir universos
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']
tickers = list(dict.fromkeys(STOCKS + BONDS))

# 2. Descargar 36 meses de datos diarios
closes_daily = yf.download(
    tickers,
    period="36mo",
    interval="1d",
    progress=False,
    auto_adjust=False
)["Close"]

# 3. Remuestrear a fin de mes y coger la última fila
closes_eom = closes_daily.resample('M').last()

# 4. Fechas y salida
fecha_ult = closes_eom.index[-1].strftime("%Y-%m-%d")  # debería ser "2025-04-30"
precios_ult = closes_eom.iloc[-1]

st.write(f"Precios al cierre de {fecha_ult}")
st.dataframe(precios_ult.to_frame("Close").T)
