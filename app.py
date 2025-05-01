import time
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# ———————————— Configuración Streamlit ————————————
st.set_page_config(
    page_title="Cierre al 30-abril-2025",
    layout="wide"
)
st.title("📅 Cierre al 30-abril-2025 — Descarga Uno a Uno")

# ———————————— Universos ————————————
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']
TICKERS = list(dict.fromkeys(STOCKS + BONDS))  # quita duplicados

# ———————————— Fecha fija ————————————
# Aquí pones la fecha que quieras; en tu caso 2025-04-30  
fecha_obj = datetime(2025, 4, 30)

# ———————————— Función de descarga uno a uno ————————————
def fetch_close_one_by_one(tickers, date):
    start = date.strftime("%Y-%m-%d")
    end   = (date + timedelta(days=1)).strftime("%Y-%m-%d")
    closes = {}
    for tk in tickers:
        try:
            df = yf.download(
                tk,
                start=start,
                end=end,
                interval="1d",
                progress=False,
                auto_adjust=False,
                threads=False        # fuerza descarga secuencial
            )["Close"]
            if not df.empty:
                closes[tk] = df.iloc[0]
            else:
                st.warning(f"No data para {tk} en {start}")
        except Exception as e:
            st.warning(f"Error descargando {tk}: {e}")
        time.sleep(0.5)  # pausa medio segundo entre peticiones
    return pd.Series(closes)

# ———————————— Botón de descarga ————————————
if st.button("▶️ Descargar precios uno a uno"):
    with st.spinner("Descargando…"):
        precios = fetch_close_one_by_one(TICKERS, fecha_obj)

    if precios.empty:
        st.error("❌ No se obtuvieron precios para ninguna ticker.")
    else:
        # Convertimos a DataFrame para mostrar en forma de tabla
        precios_df = precios.to_frame("Close").T.round(4)
        st.success(f"Precios al {fecha_obj.strftime('%Y-%m-%d')}")
        st.dataframe(precios_df, use_container_width=True)
