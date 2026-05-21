import requests
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

TOKEN = "8906567819:AAGwMMU05H-YGk-hytlwTcvJol1grNxjfLE"
CHAT_ID = "6333716746"

tv = TvDatafeed()

xbank = tv.get_hist(
symbol='XBANK',
exchange='BIST',
interval=Interval.in_1_hour,
n_bars=700
)

isctr = tv.get_hist(
symbol='ISCTR1!',
exchange='BIST',
interval=Interval.in_1_hour,
n_bars=700
)

df = pd.DataFrame()

df['time'] = xbank.index
df['xbank_close'] = xbank['close'].values
df['xbank_volume'] = xbank['volume'].values

df['isctr_close'] = isctr['close'].values
df['isctr_volume'] = isctr['volume'].values

csv_file = "market_data.csv"

df.to_csv(csv_file, index=False)

url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

files = {
'document': open(csv_file, 'rb')
}

data = {
'chat_id': CHAT_ID
}

requests.post(
url,
files=files,
data=data
)
