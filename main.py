import numpy as np
import json
import csv
import io
import yfinance as yf
from sklearn.linear_model import LogisticRegression
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Collecting log data's using yfinance library
# The trading data is collected from IBM
data = yf.download('IBM', start='2025-02-13', end='2025-08-13', group_by='ticker')['IBM']
# The collected data is converted to csv format
data_to_csv = data.to_csv()
csv_file_object = io.StringIO(data_to_csv)
csv_reader = csv.reader(csv_file_object)
# Later the data in csv format is converted to list
list_of_csv = list(csv_reader)


# Calculating for the RSI(Relative Strength Index)
def calculate_rsi(series, period=20):
    delta = series.diff()
    gain  = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0,0).rolling(window=period).mean()
    rs = gain/loss
    return (100 - (100/(1+rs)))

data['RSI'] = calculate_rsi(data['Close'])

data['Signal'] = 0
data.loc[data['RSI'] < 30, 'Signal'] = 1 # Buy
data.loc[data['RSI'] > 50, 'Signal'] = -1 # Sell
data['Position'] = data['Signal'].shift()

data = data.dropna()

data_to_csv_1 = data.to_csv()
csv_file_object_1 = io.StringIO(data_to_csv_1)
csv_reader_1 = csv.reader(csv_file_object_1)
list_of_csv_1 = list(csv_reader_1)

#Splitting the Dataset
feature_colns = ['Open', 'High', 'Low', 'Close', 'Volume', 'RSI', 'Signal', 'Position']
X = data[feature_colns]
y = data.Signal

split = int(0.65*len(data))
X_train, X_test, y_train, y_test = X[:split], X[split:], y[:split], y[split:]

model = LogisticRegression()
model = model.fit(X_train, y_train)

a = list(zip(X.columns, np.transpose(model.coef_)))

l2 = []
for i in a:
    l2.append(str(i[1]))
print(l2)    
values = [feature_colns, l2]    
print(values)

# Load credentials (replacing with the service account file)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('D:\H_to_H_Internship_Assignment\service_account.json', scopes=SCOPES)

# Building the service
service = build('sheets', 'v4', credentials=creds)

with open('config.json', 'r') as f:
    data = json.load(f)

API_KEY = data["API_KEY"]
body = {
    'values': values
}
result = service.spreadsheets().values().update(
    spreadsheetId='1S5YWUuUhLxS6sbZIe0gZPJFU3k9ornCNfFyggeYOgsQ',
    range='Sheet1!A1',
    valueInputOption='RAW', 
    body=body
).execute()

API_KEY = data["API_KEY"]
body = {
    'values': list_of_csv
}
result = service.spreadsheets().values().update(
    spreadsheetId='1S5YWUuUhLxS6sbZIe0gZPJFU3k9ornCNfFyggeYOgsQ',
    range= 'Sheet2!A1',
    valueInputOption='RAW',
    body=body
).execute()

API_KEY = data["API_KEY"]
body = {
    'values': list_of_csv_1
}
result = service.spreadsheets().values().update(
    spreadsheetId='1S5YWUuUhLxS6sbZIe0gZPJFU3k9ornCNfFyggeYOgsQ',
    range= 'Sheet3!A1',
    valueInputOption='RAW',
    body=body
).execute()