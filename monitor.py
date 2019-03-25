from virtual_sense_hat import VirtualSenseHat
#from sense_hat import SenseHat #use this when we test on Pi
from database import Database
import logging
import time
from datetime import datetime

logging.basicConfig(level = logging.DEBUG)

class Monitor:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)
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
       

    def startMonitoring(self):
        logging.debug('Start monitoring...')

        #This code is for assignment submission
        # while (True):   #forever loop
        #     self.readSenseHatData()
        #     self.database.insertEntry(self.time, self.temperature, self.humidity)   
        #     logging.debug('\nWaiting for 1 minute...\n')
        #     time.sleep(60)  

        #This code is for debugging only:Read SenseHat data every 5s for 10 times 
        for i in range(10):   
            self.readSenseHatData()
            self.database.insertEntry(self.time, self.temperature, self.humidity)   
            logging.debug('Waiting for 1 minute...\n')
            #time.sleep(60)    
            
    def stopMonitoring(self):
        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.database.closeDatabase()