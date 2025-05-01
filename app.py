import time
import streamlit as st
import pandas as pd
import yfinance as yf

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

# ———————————— Botón de descarga ————————————
if st.button("▶️ Descargar precios uno a uno"):
    precios = {}
    with st.spinner("Descargando…"):
        for tk in TICKERS:
            try:
                df = yf.download(
                    tk,
                    period="1d",          # <-- sólo pide el último día
                    interval="1d",
                    progress=False,
                    auto_adjust=False,
                    threads=False         # <-- fuerza secuencial
                )["Close"]
                if not df.empty:
                    precios[tk] = df.iloc[-1]
                else:
                    st.warning(f"No data para {tk}")
            except Exception as e:
                st.warning(f"Error {tk}: {e}")
            time.sleep(0.5)            # <-- evita rate-limit

    serie = pd.Series(precios)
    if serie.empty:
        st.error("❌ No se obtuvieron precios de cierre.")
    else:
        # Muestro en tabla (una fila con todos los cierres)
        df_out = serie.to_frame("Close").T.round(4)
        st.success("✅ Precios descargados:")
        st.dataframe(df_out, use_container_width=True)
