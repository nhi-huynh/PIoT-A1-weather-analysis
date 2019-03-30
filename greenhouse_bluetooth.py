# How did you automate the script bluetooth.py3?
# What is a sensible messaging scheme?

# from virtual_sense_hat import VirtualSenseHat
from sense_hat import SenseHat
import requests
import json
import os
import bluetooth
from pushbullet import Pushbullet

ACCESS_TOKEN = "o.SED5fMSZb6RoIOAUX2tJtko1HoseOVbq"


class Greenhouse_Bluetooth:

    def __init__(self):
        self.configFilename = 'config.json'
        self.sense = SenseHat()
        self.pb = Pushbullet(ACCESS_TOKEN)
        # ACCESS_TOKEN = "o.PchdvXPmorRZFfWseRn65UcZ1mZAWdHt"

    def initRange(self):
        with open(self.configFilename, "r") as file:
            self.range = json.load(file)
        self.minTemp = self.range["min_temperature"]
        self.maxTemp = self.range["max_temperature"]
        self.minHumidity = self.range["min_humidity"]
        self.maxHumidity = self.range["max_humidity"]

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
               title (str) : Title of text.
               body (str) : Body of text.
        """
        data = {"type": "note", "title": title, "body": body}

        response = requests.post("https://api.pushbullet.com/v2/pushes", data=json.dumps(data), headers={"Authorization": "Bearer " + ACCESS_TOKEN, "Content-Type": "application/json"})
        print("Notification sent.")

    # Get CPU temperature.
    def get_cpu_temp(self):
        res = os.popen("vcgencmd measure_temp").readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))

    def fixTemp(self):
        t1 = self.sense.get_temperature_from_humidity()
        t2 = self.sense.get_temperature_from_pressure()
        t_cpu = self.get_cpu_temp()
        h = self.sense.get_humidity()
        p = self.sense.get_pressure()
        # Calculates the real temperature compesating CPU heating.
        t = (t1 + t2) / 2
        t_corr = t - ((t_cpu - t) / 1.5)
        return t_corr

    def evaluateStatus(self, item, value, min, max, unit):
        if value < min:
            status = item + " is below minimum ({} {})".format(min, unit)
        elif value > max:
            status = item + " is above maximum ({} {})".format(max, unit)
        else:
            return ""
        return status

    def main(self):
        humidity = self.sense.get_humidity()
        print("Humidity {:.2f}".format(humidity))
        temperature = self.fixTemp()
        print("Temperature {:.2f}".format(temperature))
        sendstatus = "All Good"
        temperatureStatus = self.evaluateStatus("Temperature", int(temperature), self.minTemp, self.maxTemp, "*C")
        humidityStatus = self.evaluateStatus("Humidity", int(humidity), self.minHumidity, self.maxHumidity, "%")
        if temperatureStatus == "" and humidityStatus == "":
            sendstatus = "All Good"
        elif temperatureStatus != "" and humidityStatus != "":
            sendstatus = temperatureStatus + " and " + humidityStatus
        elif temperatureStatus != "" and humidityStatus == "":
            sendstatus = temperatureStatus
        elif temperatureStatus == "" and humidityStatus != "":
            sendstatus = humidityStatus

        nearby_devices = bluetooth.discover_devices()
        print(sendstatus)
        for macAddress in nearby_devices:
            print("Found device with mac-address: " + macAddress)
            body = "Currently the temperature is {:.2f}*C and the humidity is {:.2f}% \nStatus Report: {}" .format(temperature, humidity, sendstatus)
            self.send_notification_via_pushbullet("Update", body)

# Execute program
Greenhouse_Bluetooth = Greenhouse_Bluetooth()
Greenhouse_Bluetooth.initRange()
Greenhouse_Bluetooth.main()
