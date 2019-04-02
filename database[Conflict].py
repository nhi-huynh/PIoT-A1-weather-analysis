import logging
import sqlite3
import sys
from datetime import datetime, timedelta
import pandas as pd

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"

ONE_DAY_DELTA = timedelta(days = 1)
ONE_HOUR_DELTA = timedelta(hours = 1)

logging.basicConfig(level = logging.DEBUG)

class Database:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.openDatabase()
        self.createSenseHatTable()
        self.createPushbulletTable()
        self.connection
        self.cursor

 #Basic database setup       
    def openDatabase(self):
        try:
            connection = sqlite3.connect(self.databaseName, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        except Exception as e:
            logging.error('Open database failed. {}'.format(str(e)))
            sys.exit()
        else:
            logging.debug('Sucessfully open database')
            self.connection = connection
            self.cursor = connection.cursor()

    def runCommand(self, command, action):
        """
        Run a SQLite database command
        """
        try:
            self.cursor.execute(command)
        except Exception as e:
            logging.error('''{} failed. 
            Command {}.
            Exception: {}.'''.format(action, command, str(e)))
            sys.exit()
        else: 
            self.connection.commit() 
            logging.debug('{} successful.'.format(action))
    
    def getValue(self, command, value):
        """
        Get a value from the database and return the result
        """
        try:
            result = self.cursor.execute(command).fetchone()[0]
        except Exception as e:
            logging.error('''Reading {} failed. 
            Command {}.
            Exception: {}.'''.format(value, command, str(e)))
            sys.exit()
        else: 
            logging.debug('{} is {}.'.format(value, result))
            return result

    def getAllValue(self, command, value):
        """
        Get a value from the database and return the result
        """
        try:
            result = self.cursor.execute(command)
        except Exception as e:
            logging.error('''Reading {} failed. 
            Command {}.
            Exception: {}.'''.format(value, command, str(e)))
            sys.exit()
        else: 
            logging.debug('{} is {}.'.format(value, result))
            return result
    
    def createTable(self, tableName, columns):
        """
        Create a table in the database
        """
        command = """CREATE TABLE IF NOT EXISTS {} ({})""".format(tableName, columns)
        action = "Creating {}".format(tableName)
        self.runCommand(command, action)

    def closeDatabase(self):
        self.connection.commit()
        self.connection.close()
        logging.debug('Database closed.')

### Functions specifically for sensehat_data table
    def createSenseHatTable(self):
        self.createTable('sensehat_data', 'date DATE, time TIME, temperature NUMERIC, humidity NUMERIC')

    def insertSenseHatData(self, date, time, temperature, humidity):
        
        command = """INSERT INTO sensehat_data VALUES 
        ('{}', '{}', '{}','{}')""".format(date, time, temperature, humidity)
        action = 'Writing sensehatdata'
        self.runCommand(command, action)

    def readSenseHatData(self):
        command = 'SELECT * FROM sensehat_data'
        value = "all SenseHat data"
        entries = self.getAllValue(command, value)
        return entries

### Functions neccessary for analytics.py
    def getWeatherDataOn(self, date):     
        """
        Receive a date object e.g. datetime(year, month, day). 
        If no date received, default date is today. 
        Return all temperature and humidity recorded and time for that day in a form of two dictionaries
        """

        command = """SELECT time, temperature, humidity FROM sensehat_data WHERE date = '{}'""".format(date)
        value = "Weather data for date {}".format(date)
        weatherData =  self.getAllValue(command, value)

        time = []
        temperature = []
        humidity = []

        for entry in weatherData:
            time.append(pd.to_datetime(entry[0]))
            temperature.append(round(float(entry[1]), 2))
            humidity.append(round(float(entry[2]), 2))
        
        return time, temperature, humidity

    def getAverageWeatherData(self, startDate = None, endDate= None):   
        """
        Receive a date object e.g. datetime(year, month, day). 
        If no date received, default date is today. 
        Return all temperature and humidity recorded and time for that day in a form of two dictionaries
        """
        if startDate == None or endDate == None:
            startDate, endDate = self.getAllValue("SELECT MIN(date), MAX(date) from sensehat_data", "minimum date in sensehat_data").fetchone()
            logging.debug("Start date is: {}".format(startDate))
            logging.debug("End date is: ".format(endDate))

        command = """SELECT date, AVG(temperature), AVG(humidity) FROM sensehat_data WHERE date BETWEEN {} AND {} GROUP BY date""".format(startDate, endDate)
        value = "Average weather data from {} to {}".format(startDate, endDate)
        avgWeatherData =  self.getAllValue(command, value)

        date = []
        avgTemperature = []
        avgHumidity = []

        for entry in avgWeatherData:
            date.append(pd.to_datetime(entry[0]))
            avgTemperature.append(round(float(entry[1]), 2))
            avgHumidity.append(round(float(entry[2]), 2))
        
        return date, avgTemperature, avgHumidity

### Functions specifically for pushbullet_data table
    def insertPushbulletData(self, date = datetime.now()):
        command = """INSERT INTO pushbullet_data VALUES (DATE('now'))"""
        action = "Inserting Pushbullet data"
        self.runCommand(command, action)

    def createPushbulletTable(self):
        self.createTable('pushbullet_data', 'date DATETIME')

		
