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

#possibly create a test file just for resume shits and giggles and you will need for future anyways

class InsertData:

    def __init__(self) -> None:
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        self.bars = []
        self._dataFrame = pd.DataFrame(self.bars) #just a place holder variable
        self.MAX_LIMIT = 50_000

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


    def retrieveData(self, ticker: str, start: str, end: str) -> None:
        """ Method grabs stock data from api and puts it in dataFram attribute """
        maxDate = date.today() - relativedelta(years=2)
        startComp = date(int(start[:4]), int(start[5:7]), int(start[8:]))
        endComp = date(int(end[:4]), int(end[5:7]), int(end[8:]))

        #check with gpt if should be raising valueerror here
        if startComp < maxDate:
            raise ValueError(f"Invalid start date max date is {maxDate} following format of YYYY-MM-DD")
        
        if date.today() < endComp:
            raise ValueError(f"Invalid end date max date is {date.today()} following format of YYYY-MM-DD")
        
        if startComp > endComp:
            raise ValueError(f"Invalid dates start date has to be lower than end date")
       
        for bar in self.client.list_aggs(
            ticker=ticker.upper(),
            multiplier=1,
            timespan='day',
            from_=start,
            to=end,
            limit=self.MAX_LIMIT
            ):
            
           
            self.bars.append({"Timestamp":bar.timestamp, "ticker":ticker.upper(), "Open":bar.open, "Close":bar.close, "High":bar.high, "Low":bar.low, "Volume":bar.volume, "Transactions":bar.transactions, "Vwap":bar.vwap})

            if len(self.bars) == (5*self.MAX_LIMIT): #free api tier requirement
                print("sleeping for 1 minute")
                time.sleep(60)


        
        #possibly could do here is create dataFrame headers already and then just do a append here too or get rid of append for loop and append right into dataframe so not making two big list
        self._dataFrame = pd.DataFrame(self.bars)
        self._dataFrame['Timestamp'] = pd.to_datetime(self._dataFrame["Timestamp"], unit='ms').dt.strftime('%Y-%m-%d')

    def showData(self) -> None:
        """ Method prints out head of dataFrame """
        print(self._dataFrame.head())

    def insertToDatabase(self):
        """ Method used after retrieveData to insert data into MySQL server, closes connection after insertion """
        
        
        #probably will need to create a method to insert what into what tables correctly and verify that its the right one before
        if self.createConnection():

            cursor = self.db.cursor()
            sql = "INSERT IGNORE INTO stock_agg (date, ticker, open, close, high, low, volume, transactions, vwap) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            
            data = [x[1:] for x in self._dataFrame.itertuples()]

            # Execute batch insert
            cursor.executemany(sql, data)
            

            
            
            self.db.commit()
        
        #close connection and reset attributes
        self.bars = []
        self._dataFrame = pd.DataFrame(self.bars)
        print(self.closeConnection())
        



    

if __name__ == '__main__':
    x = InsertData()
    #print(x.createConnection())
    
    #x.retrieveData("LMT", "2023-05-31", "2025-05-30")
    #x.insertToDatabase()


    #print(x.closeConnection()) // already closing connection after inserting data
    #x.showData()