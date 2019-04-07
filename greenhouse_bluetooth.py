#!/usr/bin/env python3
from sense_hat import SenseHat
import requests
import json
import subprocess as sp
import os
import bluetooth
import time
from datetime import datetime, timedelta
from defineTimezone import *
from adjustTemp import *

ACCESS_TOKEN = "o.SED5fMSZb6RoIOAUX2tJtko1HoseOVbq"
TIME_FORMAT = "%H:%M:%S"


class Greenhouse_Bluetooth:

    def __init__(self):
        self.sense = SenseHat()
        self.configFilename = 'config.json'
        self.list = []

    def initRange(self):
        with open(self.configFilename, "r") as file:
            self.range = json.load(file)
        self.minTemp = self.range["min_temperature"]
        self.maxTemp = self.range["max_temperature"]
        self.minHumidity = self.range["min_humidity"]
        self.maxHumidity = self.range["max_humidity"]

    def initPairedDevices(self):
        p = sp.Popen(
            ["bt-device", "--list"],
            stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        (stdout, stdin) = (p.stdout, p.stdin)
        data = stdout.readlines()
        for binary in data:
            string1 = binary.decode('ascii')
            start = string1.find('(')
            if start != -1:
                start += 1
                end = string1.index(')')
                length = end - start
                String = string1[start: start + length]
                self.list.append(String)

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
               title (str) : Title of text.
               body (str) : Body of text.
        """
        data = {"type": "note", "title": title, "body": body}

        response = requests.post(
            "https://api.pushbullet.com/v2/pushes",
            data=json.dumps(data),
            headers={"Authorization": "Bearer " + ACCESS_TOKEN,
                     "Content-Type": "application/json"})
        print("Notification sent.")

    def evaluateStatus(self, item, value, min, max, unit):
        if value < min:
            status = item + " is below minimum ({} {})".format(min, unit)
        elif value > max:
            status = item + " is above maximum ({} {})".format(max, unit)
        else:
            return ""
        return status

    def main(self):
        time1 = datetime.now(timezone)
        time3 = datetime.now(timezone)
        print("Starting up please wait a moment...")
        while True:
            time.sleep(60)
            time1 = datetime.now(timezone)
            humidity = self.sense.get_humidity()

            t1 = self.sense.get_temperature_from_humidity()
            t2 = self.sense.get_temperature_from_pressure()
            t_cpu = get_cpu_temp()
            h = self.sense.get_humidity()
            p = self.sense.get_pressure()
            # Calculates the real temperature compesating CPU heating.
            t = (t1 + t2) / 2
            t_corr = t - ((t_cpu - t) / 1.5)
            t_corr = get_smooth(t_corr)
            temperature = t_corr

            sendstatus = "All Good"
            temperatureStatus = self.evaluateStatus(
                "Temperature",
                int(temperature),
                self.minTemp,
                self.maxTemp,
                "*C")
            humidityStatus = self.evaluateStatus(
                "Humidity",
                int(humidity),
                self.minHumidity,
                self.maxHumidity,
                "%")
            if temperatureStatus == "" and humidityStatus == "":
                sendstatus = "All Good"
            elif temperatureStatus != "" and humidityStatus != "":
                sendstatus = temperatureStatus + " and " + humidityStatus
            elif temperatureStatus != "" and humidityStatus == "":
                sendstatus = temperatureStatus
            elif temperatureStatus == "" and humidityStatus != "":
                sendstatus = humidityStatus

            nearby_devices = bluetooth.discover_devices()
            minute1 = time1.strftime("%M")
            time_1 = int(minute1)
            for macAddress in nearby_devices:
                print("Found device with mac-address: " + macAddress)
                if macAddress in self.list:
                    minute3 = time3.strftime("%M")
                    time_3 = int(minute3)
                    if ((time_1-time_3) >= 2) or ((time_1-time_3) <= (-50)):
                        body = """Currently the temperature is {:.2f}*C and the
                        humidity is {:.2f}% \nStatus Report: {}""" .format(
                            temperature, humidity, sendstatus)
                        self.send_notification_via_pushbullet("Update", body)
                        time3 = datetime.now(timezone)
            print("Waiting for 1 minute...")


# Execute program
Greenhouse_Bluetooth = Greenhouse_Bluetooth()
Greenhouse_Bluetooth.initRange()
Greenhouse_Bluetooth.initPairedDevices()
Greenhouse_Bluetooth.main()
