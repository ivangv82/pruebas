from datetime import datetime, timedelta
import yfinance as yf
import streamlit as st  # <–– aquí

# ———————— 1. Define aquí tus universos ————————
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']

# ———————— 2. Ahora sí puedes combinarlos ————————
tickers = STOCKS + BONDS

# ———————— 3. Fechas y descarga ————————
last_month_end = datetime(2025, 4, 30)
start = last_month_end.strftime("%Y-%m-%d")
end   = (last_month_end + timedelta(days=1)).strftime("%Y-%m-%d")

df = yf.download(
    tickers,
    start=start,
    end=end,
    interval="1d",
    progress=False,
    auto_adjust=False
)["Close"]

if df.empty:
    st.error("No se descargaron datos para la fecha solicitada.")
else:
    # Toma el primer (y único) registro sin usar .loc
    precios = df.iloc[0]
    st.write("Precios al 2025-04-30:", precios.to_dict())
