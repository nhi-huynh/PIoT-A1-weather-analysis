from virtual_sense_hat import VirtualSenseHat
#from sense_hat import SenseHat
import logging
import sqlite3
import sys
import time
from datetime import datetime

logging.basicConfig(level = logging.DEBUG)

class Monitor:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName

        self.openDatabase()
        

        #self.createTable()

        self.sense = VirtualSenseHat.getSenseHat()
        #self.sense = SenseHat.getSenseHat()
        
    
    def readSenseHatData(self):
        self.time = datetime.now().__str__()
        self.temperature = self.sense.get_temperature()
        self.humidity = self.sense.get_humidity()

        if self.temperature == 0 or self.humidity == 0:
            self.readSenseHatData()
        else:
            logging.debug('\nTime: {}'.format(self.time))
            logging.debug('Temperature: {0:0.1f} *C'.format(self.temperature))
            logging.debug('Humidity: {0:0.0f}%'.format(self.humidity))

        
    def openDatabase(self):
        try:
            connection = sqlite3.connect(self.databaseName)
            
        except Exception as e:
            logging.error('Open database failed. {}'.format(str(e)))
            sys.exit()
        else:
            logging.debug('Sucessfully open database')
            self.connection = connection
            self.cursor = connection.cursor()

    def createTable(self):
        command = """CREATE TABLE sensehat_data 
        (datetime text, temperature real, humidity real)"""
        try:
            self.cursor.execute(command)           
        except Exception as e:
            logging.error('''Creating table failed. 
            Command {}.
            Exception: {}.'''.format(command, str(e)))
            sys.exit()
        else: 
            logging.debug('Table successfull created.')
            

    def insertEntry(self):
        command = """INSERT INTO sensehat_data VALUES 
        ('{}','{}','{}')""".format(self.time, self.temperature, self.humidity)
        try:
            self.cursor.execute(command)
        #"INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)"
        except Exception as e:
            logging.error('''Writing entry failed. 
            Command {}.
            Exception: {}.'''.format(command, str(e)))
            sys.exit()
        else: 
            self.connection.commit() 
            logging.debug('Entry written to database')
        

    def startMonitoring(self):
        logging.debug('Start monitoring...')
        self.createTable()

        while (True):
            self.readSenseHatData()
            self.insertEntry()   
            time.sleep(15) 
            

        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.connection.close()

monitor = Monitor()
monitor.startMonitoring()


