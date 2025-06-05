
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
        ticker='O:SPY251219C00650000',
        multiplier=1,
        timespan='day',
        from_='2025-02-26',
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
    
#apiKeyTest()

def apiTest2():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    APIKEY = os.getenv("APIKEY")
    client = RESTClient(api_key=APIKEY)

    #contract = client.get_options_contract("O:TSLA250314C00207500")
    #print(contract)
    conditions = []
    for c in client.list_quotes("O:BA250321C00182500", limit=1000):
        conditions.append(c)

    df = pd.DataFrame(conditions)
    print(df.head())
    print(list(df.columns.values))
    

def optionsTest():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    APIKEY = os.getenv("APIKEY")
    client = RESTClient(api_key=APIKEY)

    MAX_LIMIT = 50_000

    print(help(client.list_options_contracts))

optionsTest()