from datetime import datetime, timedelta
import yfinance as yf

STOCKS     = ['GLD','SPY','QQQ','IYR','VGK','GSG','HYG','EEM','TLT','IWM','EWJ','LQD']
BONDS      = ['IEF','LQD','SHY','BIL']

# Fecha del último día de mes a extraer
last_month_end = datetime(2025, 4, 30)  # o calcula dinámicamente
start = last_month_end.strftime("%Y-%m-%d")
end   = (last_month_end + timedelta(days=1)).strftime("%Y-%m-%d")

# Descarga diaria sólo para ese día
precios = yf.download(
    STOCKS + BONDS,
    start=start,
    end=end,
    interval="1d",
    progress=False,
    auto_adjust=False
)["Close"].loc[start]

print(precios)
