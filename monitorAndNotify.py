from virtual_sense_hat import VirtualSenseHat
#from sense_hat import SenseHat #use this when we test on Pi
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
        self.sense = VirtualSenseHat.getSenseHat()
        #self.sense = SenseHat.getSenseHat() #use this when we test on Pi
        
    def readSenseHatData(self):
        self.time = datetime.now().__str__()
        self.temperature = self.sense.get_temperature()
        self.humidity = self.sense.get_humidity()

        if self.temperature == 0 or self.humidity == 0:
            logging.error('Data discarded: Temperature or humidity is zero.')
            self.readSenseHatData()
        else:
            logging.debug('Time: {}'.format(self.time))
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
            logging.error('''Exception: {}.'''.format(str(e)))
        else: 
            logging.debug('Table successfull created.')
            

    def insertEntry(self):
        command = """INSERT INTO sensehat_data VALUES 
        ('{}','{}','{}')""".format(self.time, self.temperature, self.humidity)
        try:
            self.cursor.execute(command)
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
            logging.debug('\nWaiting for 1 minute...\n')
            time.sleep(10)  #10s for debugging. 60s for assignment submission 
            
        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.connection.close()

monitor = Monitor()
monitor.startMonitoring()


