from virtual_sense_hat import VirtualSenseHat
#from sense_hat import SenseHat #use this when we test on Pi
from database import Database
import logging
import time
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ONE_DAY_DELTA = timedelta(days = 1)
ONE_HOUR_DELTA = timedelta(hours = 1)

logging.basicConfig(level = logging.DEBUG)

class Monitor:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)
        self.sense = VirtualSenseHat.getSenseHat()
        #self.sense = SenseHat.getSenseHat() #use this when we test on Pi
        self.startTime = datetime.now()

        self.fakeTime = self.startTime

    def readSenseHatData(self):
        self.timestamp = datetime.now()
        date = self.timestamp.date()
        time = self.timestamp.time()
        self.humidity = self.sense.get_humidity()

        if self.temperature == 0 or self.humidity == 0:
            logging.error('Data discarded: Temperature or humidity is zero.')
            self.readSenseHatData()
        else:
            logging.debug('Date: {}'.format(date))
            logging.debug('Time: {}'.format(time))
            logging.debug('Temperature: {0:0.1f} *C'.format(self.temperature))
            logging.debug('Humidity: {0:0.0f}%'.format(self.humidity))
       
    def readFakeSenseHatData(self):
        #### Only for debugging!
        self.fakeTime += ONE_HOUR_DELTA
        date = self.fakeTime.date()
        time = self.fakeTime.time()
        self.temperature = self.sense.get_temperature()
        self.humidity = self.sense.get_humidity()

        if self.temperature == 0 or self.humidity == 0:
            logging.error('Data discarded: Temperature or humidity is zero.')
            self.readSenseHatData()
        else:
            logging.debug('Date: {}'.format(date))
            logging.debug('Time: {}'.format(time))
            logging.debug('Temperature: {0:0.1f} *C'.format(self.temperature))
            logging.debug('Humidity: {0:0.0f}%'.format(self.humidity))

    def startMonitoring(self):
        logging.debug('Start monitoring...')

        ###This code is for assignment submission
        while (True):   #forever loop
            self.readSenseHatData()
            self.database.insertSenseHatData(self.timestamp.date(), self.timestamp.time(), self.temperature, self.humidity)   
            logging.debug('\nWaiting for 1 minute...\n')
            time.sleep(60)  

    def debugMonitoring(self):
        #This code is for debugging only:Read SenseHat data every 5s for 10 times 
        #Then repeat that process for everyday to simulate a one-week progress
        for i in range(24*7):   
            self.readFakeSenseHatData()
            self.database.insertSenseHatData(self.fakeTime.date(), self.fakeTime.time(), self.temperature, self.humidity)   
            #time.sleep(1)
            logging.debug('Waiting for 1 minute...\n')
                
            
    def stopMonitoring(self):
        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.database.closeDatabase()

monitor = Monitor()
#monitor.startMonitoring()
monitor.debugMonitoring()
