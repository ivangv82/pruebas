import time
import streamlit as st
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

# ————— Configuración Streamlit —————
st.set_page_config(page_title="Cierre 30-abril-2025 (AlphaVantage)", layout="wide")
st.title("📅 Cierre al 30-abril-2025 con Alpha Vantage")

# ————— Lee tu API Key desde secrets —————
API_KEY = "JH2RHP5ZMYIIT21N" #st.secrets["alpha_vantage"]["key"]
ts = TimeSeries(key=API_KEY, output_format="pandas", indexing_type="date")

# ————— Universo de tickers —————
STOCKS = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS  = ['IEF','LQD','SHY','BIL']
TICKERS = list(dict.fromkeys(STOCKS + BONDS))

fecha_obj = datetime(2025, 4, 30).date()

# ————— Botón de descarga —————
if st.button("▶️ Descargar precios (AlphaVantage)"):
    precios = {}
    with st.spinner("Descargando…"):
        for tk in TICKERS:
            try:
                # Llama al endpoint diario ajustado
                data, _ = ts.get_daily_adjusted(symbol=tk, outputsize="full")
                # data.index es DatetimeIndex
                if fecha_obj in data.index.date:
                    precios[tk] = data.loc[str(fecha_obj), "4. close"]
                else:
                    # fallback: toma el cierre más reciente antes de fecha_obj
                    df = data[data.index.date < fecha_obj]
                    if not df.empty:
                        precios[tk] = df["4. close"].iloc[0]
                    else:
                        st.warning(f"No hay datos antes de {fecha_obj} para {tk}")
            except Exception as e:
                st.warning(f"Error con {tk}: {e}")
            time.sleep(1)  # Alpha Vantage limita 5 llamadas/minuto

    if precios:
        df_out = pd.Series(precios, name="Close").to_frame().T.round(4)
        st.success(f"✅ Precios al cierre de {fecha_obj}")
        st.dataframe(df_out, use_container_width=True)
    else:
        st.error("❌ No se obtuvieron precios.")
