#for database
import mysql.connector

#for env variables
import os
from dotenv import find_dotenv, load_dotenv

#for api data key
from polygon import RESTClient
import pandas as pd
import time

def apiKeyTest():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    APIKEY = os.getenv("APIKEY")
    client = RESTClient(api_key=APIKEY)

    #2023-02-28 is like the max range i can get from a free api key

    bars = []
    MAX_LIMIT = 50_000
    for bar in client.list_aggs(
        ticker='BA',
        multiplier=1,
        timespan='day',
        from_='2024-02-28',
        to='2025-02-28',
        limit=MAX_LIMIT
    ):
        bars.append(bar)
        if len(bars) == (5*MAX_LIMIT):
            print("sleeping for 1 minute")
            time.sleep(60)

    df = pd.DataFrame(bars)
    df['timestamp'] = pd.to_datetime(df["timestamp"], unit='ms').dt.strftime('%Y-%m-%d')
    print(df.head())
    


    #works
    """
    # List Aggregates (Bars)
    aggs = []
    for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-01-01", to="2023-06-13", limit=50000):
        aggs.append(a)

    print(aggs)

    # Get Last Trade
    trade = client.get_last_trade(ticker=ticker)
    print(trade)

    # List Trades
    trades = client.list_trades(ticker=ticker, timestamp="2022-01-04")
    for trade in trades:
        print(trade)

    # Get Last Quote
    quote = client.get_last_quote(ticker=ticker)
    print(quote)

    # List Quotes
    quotes = client.list_quotes(ticker=ticker, timestamp="2022-01-04")
    for quote in quotes:
        print(quote)
        
     """   
        
apiKeyTest()

def databaseConnect():
    #####loading sensitive data from env
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    SERVERUSER = os.getenv("SERVERUSER")
    PASSWORD = os.getenv("PASSWORD")
    ########

    db = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=SERVERUSER,
        password=PASSWORD,
    )
    #setup a vs code variable for password and username in future

    cursor = db.cursor()

    #cursor.execute("show databases") // showed databases in server

    cursor.execute("use stock_data")
    #cursor.execute("show tables")
    cursor.execute("SHOW columns FROM beoing_trading_days") # use this to get datatypes of columns so like a double(4,4) so can make sure to format data based on what it is and datatype is [1] index

    for x in cursor:
        print(x)
        
    # future plans are to create a class that allows for inserting and querrying, currently i want to create a class that allows for insert data in sql server first and formost
    # need to change root and user password for server"


