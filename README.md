
# Algo-Trading System with ML & Automation 

A Python-driven trading system that connects with stock data, applies a trading strategy from a previous batch, and automatically stores and analyzes data in Google Sheets.

## Project Overview

### 1. Data Retrieval and Trading Strategy Logic:
Retrieving daily stock using the library YFinance (Yahoo Finance's API). Implementing *RSI<30* as a buy signal and confirming with *20-DMA* crossing above *50-DMA*. To understand the stock graph better, backtesting is done for the past 6 months.

### 2. ML and Google Sheets Automation:
Using a basic model of Logistic Regression, we can predict next-day movement using Open, High, Low, Close, Volume, RSI, Signal, and Position values to output the prediction accuracy. Storing trade signals in Google Sheets.

## Installation Instructions

#### Install the following libraries

    1. yfinance
    2. scikit-learn
    3. google-auth-oauthlib
    4. google-api-python-client
    

Just download the repository and install the libraries altogether from **requirements.txt** file which can be done with the following command.
```http
pip install -r requirements.txt
```

* #### API Reference

   *Note:* Input your API Key in **config.json** before running the program.

* #### SpreadSheet ID 
   | Parameter | Type     | Description                |
   | :-------- | :------- | :------------------------- |
   | `spreadsheet_ID` | `string` | **Required**: Your Google Sheet ID |
      
* #### Importing Service Account File
   Download your service_account.json file from the Google Cloud Console, which contains your credentials data.

