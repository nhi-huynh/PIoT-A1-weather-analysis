import logging
import sqlite3
import sys
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"
ONE_DAY_DELTA = timedelta(days = 1)

logging.basicConfig(level = logging.DEBUG)

class Database:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.openDatabase()
        self.createDataTable()
        self.createPushbulletTable()
        self.connection
        self.cursor
        
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

    def createDataTable(self):
        command = """CREATE TABLE sensehat_data(
            timestamp DATETIME, temperature NUMERIC, humidity NUMERIC)"""
        try:
            self.cursor.execute(command)           
        except Exception as e:
            logging.error('''Exception: {}.'''.format(str(e)))
        else: 
            logging.debug('Table successfull created.')
            
    def createPushbulletTable(self):
        command = """CREATE TABLE pushbullet_data 
        (date DATETIME, has_sent_notification integer)"""
        try:
            self.cursor.execute(command)           
        except Exception as e:
            logging.error('''Exception: {}.'''.format(str(e)))
        else: 
            logging.debug('Table successfull created.')

    
    def insertDataEntry(self, time, temperature, humidity):
        command = """INSERT INTO sensehat_data VALUES 
        (DATETIME('now', 'localtime'),'{}','{}')""".format(temperature, humidity)
        try:
            self.cursor.execute(command)
        except Exception as e:
            logging.error('''Writing data failed. 
            Command {}.
            Exception: {}.'''.format(command, str(e)))
            sys.exit()
        else: 
            self.connection.commit() 
            logging.debug('Data entry written to database')
    
    def populatePushbulletData(self):
        row = self.cursor.execute("SELECT DATE(MIN(timestamp)), DATE(MAX(timestamp)) FROM sensehat_data").fetchone()
        startDate = datetime.strptime(row[0], DATE_FORMAT)
        endDate = datetime.strptime(row[1], DATE_FORMAT)

        logging.debug("Populating Pushbullet data to database")
        logging.debug("Dates:")

        date = startDate
        while date <= endDate: 
            row = self.cursor.execute(
                """SELECT COUNT(*) FROM sensehat_data
                WHERE timestamp >= DATE(:date) AND timestamp < DATE(:date, '+1 day')""",
                { "date": date.strftime(DATE_FORMAT) }).fetchone()
            
            logging.debug(date.strftime(DATE_FORMAT) )
            
            date += ONE_DAY_DELTA
        
        command = """INSERT INTO pushbullet_data VALUES ({}, {})""".format(date.strftime(DATE_FORMAT), 0)
        try:
            self.cursor.execute("""INSERT INTO pushbullet_data VALUES (DATE(:date), :defaultValue)""",
                { "date": date.strftime(DATE_FORMAT), "defaultValue": 0 })
        except Exception as e:
            logging.error('''Writing pushbullet data failed. 
            Command {}.
            Exception: {}.'''.format(command, str(e)))
            sys.exit()
        else: 
            self.connection.commit() 
            logging.debug('Pushbullet data first populated to database')
    
    def readDataEntries(self):
        command = 'SELECT * FROM sensehat_data'
        try:
            entries = self.cursor.execute(command)
        except Exception as e:
            logging.error('''Reading entry failed. 
            Command {}.
            Exception: {}.'''.format(command, str(e)))
            sys.exit()
        else: 
            return entries

    def closeDatabase(self):
        self.connection.commit()
        self.connection.close()
        logging.debug('Database closed.')




