from datetime import datetime, timedelta
import yfinance as yf

# Parámetros
tickers = STOCKS + BONDS
last_month_end = datetime(2025, 4, 30)
start = last_month_end.strftime("%Y-%m-%d")
end   = (last_month_end + timedelta(days=1)).strftime("%Y-%m-%d")

# Descarga diaria para ese día
df = yf.download(
    tickers,
    start=start,
    end=end,
    interval="1d",
    progress=False,
    auto_adjust=False
)["Close"]

# Debug: verifica el índice real
print("Fechas descargadas:", df.index)

# En lugar de .loc[start], toma directamente el primer registro:
if not df.empty:
    precios = df.iloc[0]   # aquí tienes un Series con el Close de cada ticker
    print(precios)
else:
    print("No se descargó ningún dato para ese rango.")
