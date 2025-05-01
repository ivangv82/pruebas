import time
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# ———————————— Streamlit config ————————————
st.set_page_config(page_title="Cierre al 30-abril-2025", layout="wide")
st.title("📅 Cierre al 30-abril-2025 — Descarga Uno a Uno")

# ———————————— Universo de tickers ————————————
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']
TICKERS = list(dict.fromkeys(STOCKS + BONDS))

# ———————————— Fecha objetivo ————————————
fecha_obj = datetime(2025, 4, 30)

# ———————————— Botón para lanzar la descarga ————————————
if st.button("▶️ Descargar precios uno a uno"):
    precios = {}
    with st.spinner("Descargando precios…"):
        for tk in TICKERS:
            try:
                df = yf.download(
                    tk,
                    period="2d",          # trae los últimos 2 días hábiles
                    interval="1d",
                    progress=False,
                    auto_adjust=False,
                    threads=False         # serializa las peticiones
                )["Close"]
                if df.empty:
                    st.warning(f"No data para {tk}")
                else:
                    # extrayendo el dato de fecha_obj si existe
                    mask = df.index.date == fecha_obj.date()
                    if mask.any():
                        precio = df.loc[mask].iloc[0]
                    else:
                        precio = df.iloc[-1]  # fallback al más reciente
                    precios[tk] = precio
            except Exception as e:
                st.warning(f"Error descargando {tk}: {e}")
            time.sleep(0.5)  # medio segundo de pausa entre calls

    # ———————————— Mostrar resultado ————————————
    if precios:
        df_out = pd.Series(precios, name="Close").to_frame().T.round(4)
        st.success(f"Precios al cierre de {fecha_obj.strftime('%Y-%m-%d')}")
        st.dataframe(df_out, use_container_width=True)
    else:
        st.error("❌ No se obtuvieron precios de cierre.")
