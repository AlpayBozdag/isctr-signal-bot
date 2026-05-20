import yfinance as yf
import pandas as pd
import requests
from datetime import datetime

# TELEGRAM
BOT_TOKEN = "8906567819:AAGwMMU05H-YGk-hytlwTcvJol1grNxjfLE"
CHAT_ID = "6333716746"

# HİSSE
ticker = "ISCTR.IS"

# VERİ ÇEK
df = yf.download(ticker, period="2d", interval="15m")
python
df["Close"] = df["Close"].squeeze()
df["Volume"] = df["Volume"].squeeze()



# EMA
df["EMA20"] = df["Close"].ewm(span=20).mean()

# RSI
delta = df["Close"].diff()

gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()

rs = gain / loss
df["RSI"] = 100 - (100 / (1 + rs))

# SON VERİ
last = df.iloc[-1]
prev = df.iloc[-2]

python
price = round(last["Close"], 2)

change = round(((last["Close"] - prev["Close"]) / prev["Close"]) * 100, 2)
rsi = round(float(last["RSI"]), 2)
ema = round(float(last["EMA20"]), 2)

# HACİM
volume_status = "NORMAL"

if last["Volume"] > df["Volume"].rolling(10).mean().iloc[-1]:
    volume_status = "HIGH"

# YORUM
signal = "NEUTRAL"
emoji = "🟡"

if price > ema and rsi > 55:
    signal = "BULLISH"
    emoji = "🟢"

elif price < ema and rsi < 45:
    signal = "BEARISH"
    emoji = "🔴"

# MESAJ
message = f"""
{emoji} ISCTR SIGNAL

⏰ {datetime.now().strftime('%H:%M')}

💰 Price: {price}
📈 Change: %{change}
📊 RSI: {rsi}
📉 EMA20: {round(ema,2)}
📦 Volume: {volume_status}

Signal: {signal}
"""

# TELEGRAM GÖNDER
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": message
})

print(message)
