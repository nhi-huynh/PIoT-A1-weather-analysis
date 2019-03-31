import logging
import sqlite3
import sys
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
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
        """Run a SQLite database command"""
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
        """Get a value from the database and return the result"""
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
        """Create a table in the database"""
        command = """CREATE TABLE IF NOT EXISTS {} ({})""".format(tableName, columns)
        action = "Creating {}".format(tableName)
        self.runCommand(command, action)

    def closeDatabase(self):
        self.connection.commit()
        self.connection.close()
        logging.debug('Database closed.')

### Functions specifically for sensehat_data table
    def createSenseHatTable(self):
        self.createTable('sensehat_data', 'timestamp DATETIME, temperature NUMERIC, humidity NUMERIC')

    # def insertSenseHatData(self, datetime, temperature, humidity):
    #     command = """INSERT INTO sensehat_data VALUES 
    #     (DATETIME('now', 'localtime'),'{}','{}')""".format(temperature, humidity)
    #     action = 'Writing sensehatdata'
    #     self.runCommand(command, action)

    def insertSenseHatData(self, time, temperature, humidity):
        
        command = """INSERT INTO sensehat_data VALUES 
        ('{}','{}','{}')""".format(time, temperature, humidity)
        action = 'Writing sensehatdata'
        self.runCommand(command, action)

    def readSenseHatData(self):
        command = 'SELECT * FROM sensehat_data'
        value = "all SenseHat data"
        entries = self.getValue(command, value)
        return entries


### Functions specifically for pushbullet_data table
    def createPushbulletTable(self):
        self.createTable('pushbullet_data', 'date DATETIME, has_sent_notification integer')

    def populatePushbulletData(self, startDate, endDate, defaultValue = 0):
        """Populating Pushbullet data to database starting on startDate and ending on endDate"""

        formattedStartDate = startDate.strftime(DATE_FORMAT)
        formattedEndDate = endDate.strftime(DATE_FORMAT)

        logging.debug("Populating Pushbullet data from {} to {}.".format(formattedStartDate, formattedEndDate))

        date = startDate
        command = """INSERT INTO pushbullet_data VALUES ({}, {})""".format(date.strftime(DATE_FORMAT), 0)

        while date <= endDate:     
            formattedDate = date.strftime(DATE_FORMAT)        
            logging.debug("Date: " + formattedDate)

            command = """INSERT INTO pushbullet_data VALUES (DATE({}), {})""".format(formattedDate, defaultValue)
            action = 'Writing pushbullet data'

            self.runCommand(command, action)
            date += ONE_DAY_DELTA

    def pre_populatePushbullet(self):
        """First time just after creating the table"""
        earliestDate = self.getValue("SELECT DATE(MIN(timestamp)) FROM sensehat_data", "Getting min date from sensehat_data")
        startDate = datetime.strptime(earliestDate, DATE_FORMAT)
        endDate = datetime.strptime(datetime.now(), DATE_FORMAT)
        self.populatePushbulletData(startDate, endDate)
        
    def re_populatePushbullet(self):
        """Every time after the first time populating pushbullet_data table"""
        latestDate = self.getValue("SELECT DATE(MAX(timestamp)) FROM pushbullet_data", "Getting max date from pushbullet_data")
        startDate = datetime.strptime(latestDate, DATE_FORMAT)
        endDate = datetime.strptime(datetime.now(), DATE_FORMAT)
        self.populatePushbulletData(startDate, endDate)
        
    def insertPushbulletData(self, date):
        command = """INSERT INTO pushbullet_data VALUES 
        (DATE('now', 'localtime'), {})""".format(0)
        action = "Inserting Pushbullet data"
        self.runCommand(command, action)

    def hasSentNotification(self, date = datetime.now()):
        """Receive a date object e.g. datetime(year, month, day). 
        If no date received, default date is today. 
        Return how many notification has sent for that day"""

        formattedDate = date.strftime(DATE_FORMAT)
        command = """SELECT has_sent_notification FROM pushbullet_data WHERE date = {}""".format(formattedDate)
        value = "Notification(s) sent for date {}".format(formattedDate)
        num_notification_sent = self.getValue(command, value)
        return num_notification_sent

    def hasSentNotification(self, formattedDate):
        """Receive a date object e.g. datetime(year, month, day). 
        If no date received, default date is today. 
        Return how many notification has sent for that day"""

        command = """SELECT has_sent_notification FROM pushbullet_data WHERE date = {}""".format(formattedDate)
        value = "Notification(s) sent for date {}".format(formattedDate)
        num_notification_sent = self.getValue(command, value)
        return num_notification_sent

    def updateSentStatus(self, date = datetime.now()):
        formattedDate = date.strftime(DATE_FORMAT)
        command = """UPDATE pushbullet_data 
        SET has_sent_notification = 1 
        WHERE date = {}""".format(formattedDate)
        action = 'Updating notification status for date {}'.format(formattedDate)
        self.runCommand(command, action)



    




