#for database
import mysql.connector

#for env variables
import os
from dotenv import find_dotenv, load_dotenv

#for api data key
from polygon import RESTClient
import pandas as pd
import time

#for dates
from datetime import date
from dateutil.relativedelta import relativedelta

#************can create a parent class where optionInsert and InsertData are childs too where the init and connection and disconnect class are the same but have an abstract class for retrieve data and insert data where the children have to implement it

class optionInsert:

    def __init__(self) -> None:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        self.bars = []
        self._dataFrame = pd.DataFrame(self.bars) #just a place holder variable
        self.OPTION_MAX = 1_000

        self.client = RESTClient(api_key=os.getenv("APIKEY"))

        #self.cursor = None
        self.db = None

    def createConnection(self) -> bool:
        """ Method connects to MySQL database and intials db and cursor """
        # have a print statement for when connecting and complete
        load_dotenv(find_dotenv())
        
        try:
            self.db = mysql.connector.connect(
                host=os.getenv("HOST"),
                port=os.getenv("PORT"),
                user=os.getenv("SERVERUSER"),
                password=os.getenv("PASSWORD"),
                database="stock_data"
            )

            #self.cursor = self.db.cursor()
            return True
        except:
            return False
        
    def closeConnection(self) -> bool:
        """ Method closes connection to MySQL database """
        # figure out why returned false after LMT
        if self.db.is_connected():
            self.db.close()
            #self.cursor.close()

            return True
        else:
            return False
        
    #******start here now for section 4
    def _optionListCall(self, lst: list) -> None:
        #print('worked') 
        #print(lst[0:5])
        weekNb = 1
        ticker = ''
        exp = ''
        high = 0
        low = 0
        start_date = ''
        for week in lst:

            print(f"week {weekNb}: \n\texpired date of week = {week[0]}\n\thigh of week = {week[1]}\n\tlow of week = {week[2]}")
            for day in week[3:]:
                if day != None:
                    print(f"\tstart of week = {day[0]}")
                    ticker = day[1]
                    start_date = day[0]
                    break

            if weekNb == 7:
                exp = week[0]
                high = week[1]
                low = week[2]
                break
            else:
                weekNb += 1

        print(ticker, exp, start_date, high, low)
        bars = [] # add to self.whatever after only for testing
        #need to adjust low and high to get contracts a little out of the range
        for bar in self.client.list_options_contracts(
            underlying_ticker=ticker,
            contract_type=None,
            expiration_date=exp,
            as_of=start_date,
            strike_price_lte=float(high),
            strike_price_gte=float(low),
            expired=True,
            limit=self.OPTION_MAX
            ):
            print(bar, "here")
            print('here')
            bars.append(bar)
            if len(bars) == (5*self.OPTION_MAX):
                print("sleeping for 1 minute")
                time.sleep(60)

        print(bars)


    def retrieveData(self, ticker: str) -> None:

        data = []
        maxDate = date.today() - relativedelta(years=2)

        if self.createConnection():
           
            cursor = self.db.cursor()

            sql = "SELECT date, ticker, high, low FROM stock_agg WHERE ticker=" + "'" + ticker + "'" + " AND date > " + "'" + str(maxDate) + "'" + " ORDER BY date ASC"
            sql_check = "SELECT DISTINCT ticker FROM stock_agg"
            
            #call database to get distinct tickers from database 
            cursor.execute(sql_check)
            data = cursor.fetchall()

            data_agg  = [] #[[exp, high, low, monday, tuesday, wednesday, thursday, friday],...]

            for i in range(len(data)): #formating data recieved
                data[i] = str(data[i]).strip(")(',")

            if ticker in data: #executes fetch script from stock_agg database
                cursor.execute(sql)
                data = cursor.fetchall()
                
                #data_agg  = [] #[[exp, high, low, monday, tuesday, wednesday, thursday, friday],...]
                arr = [None] * 8

                for data_point in data: #formating for the API

                    #print(data_point[0].strftime('%A')) #prints string date like Monday
                    
                    if data_point[0].weekday() == 4: #.weekday() 4 == friday, 0 == Monday
                        arr[7] = data_point
                        arr[0] = data_point[0] #for exp date as friday for most recent contracts (end of the week)
                        
                        #iterating through single week to find the high and low (global)
                        high = data_point[2]
                        low = data_point[3]
                        for tup in arr[3:]:
                            if tup != None:
                                if tup[2] > high: #finding global high
                                    high = tup[2]

                                if tup[3] < low: #finding global low
                                    low = tup[3]

                        #putting global max and low in array
                        arr[1] = high
                        arr[2] = low   
                        
                        data_agg.append(arr)
                        arr = [None] * 8
                    else:
                        arr[data_point[0].weekday() + 3] = data_point         
                #****** ensure to remember that some weeks might be None just incase any future errors    
                #print(data_agg[1])

                self._optionListCall(data_agg)

            else: #ticker not in database
                raise ValueError(f"ticker {ticker} not in database")
            

        

    
            


        

if __name__ == '__main__':
    
    x = optionInsert()
    x.retrieveData("BA")
    
