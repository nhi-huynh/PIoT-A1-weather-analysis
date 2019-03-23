import logging
import sqlite3
import sys
import time
from datetime import datetime

logging.basicConfig(level = logging.DEBUG)

class Database:

    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.openDatabase()
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

    def createTable(self):
        command = """CREATE TABLE sensehat_data 
        (datetime text, temperature real, humidity real)"""
        try:
            self.cursor.execute(command)           
        except Exception as e:
            logging.error('''Exception: {}.'''.format(str(e)))
        else: 
            logging.debug('Table successfull created.')
            

    def insertEntry(self, time, temperature, humidity):
        command = """INSERT INTO sensehat_data VALUES 
        ('{}','{}','{}')""".format(time, temperature, humidity)
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
        
    def readEntries(self):
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
        logging.debug('Closing database...')




