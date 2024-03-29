#!/usr/bin/env python3

from sense_hat import SenseHat
from database import Database
import logging
import json
import time
import sqlite3
from datetime import datetime, timedelta
from pushbullet import Pushbullet
from defineTimezone import *
from adjustTemp import *

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ONE_DAY_DELTA = timedelta(days=1)
ONE_HOUR_DELTA = timedelta(hours=1)

logging.basicConfig(level=logging.DEBUG)
ACCESS_TOKEN = "o.SED5fMSZb6RoIOAUX2tJtko1HoseOVbq"


class Monitor:

    def __init__(self, databaseName='VirtualSenseHat.db'):
        self.sense = SenseHat()
        self.pb = Pushbullet(ACCESS_TOKEN)
        self.databaseName = databaseName
        self.database = Database(self.databaseName)
        self.connection = sqlite3.connect(databaseName)
        self.cursor = self.connection.cursor()
        self.configFilename = 'config.json'
        self.startTime = datetime.now(timezone)
        self.fakeTime = self.startTime

    def initRange(self):
        with open(self.configFilename, "r") as file:
            self.range = json.load(file)

        self.minTemp = self.range["min_temperature"]
        self.maxTemp = self.range["max_temperature"]
        self.minHumidity = self.range["min_humidity"]
        self.maxHumidity = self.range["max_humidity"]

    def readSenseHatData(self):
        self.timestamp = datetime.now(timezone)
        self.date = self.timestamp.date()
        time = self.timestamp.time()
        self.temperature = self.sense.get_temperature()
        self.humidity = self.sense.get_humidity()

        if self.temperature == 0 or self.humidity <= 0:
            self.readSenseHatData()

    def CheckDatabase(self):
        self.cursor.execute("""SELECT * FROM pushbullet_data ORDER BY
                            date DESC LIMIT 1""")
        result = self.cursor.fetchone()[0]
        strdate = self.date.strftime(DATE_FORMAT)
        if result == strdate:
            return True
        else:
            return False

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
                title (str) : Title of text.
                body (str) : Body of text.
        """
        data = {"type": "note", "title": title, "body": body}

        response = requests.post(
            "https://api.pushbullet.com/v2/pushes", data=json.dumps(data),
            headers={
                "Authorization": "Bearer " +
                ACCESS_TOKEN, "Content-Type": "application/json"})
        print("Notification sent.")

    def evaluateStatus(self, item, value, min, max, unit):
        if value < min:
            status = item + " is below minimum ({} {})".format(min, unit)
        elif value > max:
            status = item + " is above maximum ({} {})".format(max, unit)
        else:
            return ""
        return status

    def startMonitoring(self):
        logging.debug('Start monitoring...')
        while (True):
            self.readSenseHatData()
            t1 = self.sense.get_temperature_from_humidity()
            t2 = self.sense.get_temperature_from_pressure()
            t_cpu = get_cpu_temp()
            h = self.sense.get_humidity()
            p = self.sense.get_pressure()
            # Calculates the real temperature compesating CPU heating.
            t = (t1 + t2) / 2
            t_corr = t - ((t_cpu - t) / 1.5)
            t_corr = get_smooth(t_corr)
            self.temperature = t_corr

            self.database.insertSenseHatData(
                self.timestamp.date(), self.timestamp.time(),
                self.temperature, self.humidity)

            if self.CheckDatabase() is False:
                sendstatus = "All Good"
                temperatureStatus = self.evaluateStatus(
                    "Temperature", int(self.temperature), self.minTemp,
                    self.maxTemp, "*C")
                humidityStatus = self.evaluateStatus(
                    "Humidity", int(self.humidity), self.minHumidity,
                    self.maxHumidity, "%")
                if temperatureStatus == "" and humidityStatus == "":
                    sendstatus = "All Good"
                elif temperatureStatus != "" and humidityStatus != "":
                    sendstatus = temperatureStatus + " and " + humidityStatus
                elif temperatureStatus != "" and humidityStatus == "":
                    sendstatus = temperatureStatus
                elif temperatureStatus == "" and humidityStatus != "":
                    sendstatus = humidityStatus

                body = """Currently the temperature is {:.2f}*C and the
                        humidity is {:.2f}% \nStatus Report: {}""" .format(
                            self.temperature, self.humidity, sendstatus)
                printDevice = self.pb.devices[0]
                self.database.insertPushbulletData(
                    self.date.strftime(DATE_FORMAT))
                push = printDevice.push_note("Weather Update", body)

            logging.debug('\nWaiting for 1 minute...\n')
            time.sleep(60)

    def stopMonitoring(self):
        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.database.closeDatabase()


monitor = Monitor()
monitor.initRange()
monitor.startMonitoring()
