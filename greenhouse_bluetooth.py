# Create a python file called bluetooth.py3 using Bluetooth to detect
# nearby devices and when connected send an appropriate message stating the current
# temperature, humidity and if these fall within the configured temperature and humidityrange.
# Interaction with a particular bluetooth device(s).
# How do you handle this? What message have you sent to these devices?
# Is it user-friendly and makes sense? How did you automate the script bluetooth.py3?
# What is a sensible messaging scheme?

# from virtual_sense_hat import VirtualSenseHat
from sense_hat import SenseHat
import requests
import json
import os
import bluetooth
from pushbullet import Pushbullet

ACCESS_TOKEN = "o.PchdvXPmorRZFfWseRn65UcZ1mZAWdHt"


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
        print("min_temperature", self.minTemp)
        print("max_temperature", self.maxTemp)
        print("min_humidity", self.minHumidity)
        print("max_humidity", self.maxHumidity)

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
                title (str) : Title of text.
                body (str) : Body of text.
        """
        data = {"type": "note", "title": title, "body": body}
        response = requests.post("https://api.pushbullet.com/v2/pushes", data = json.dumps(data),
            headers = {"Authorization": "Bearer" + ACCESS_TOKEN, "Content-Type": "application/json"})
        print("Notification sent.")

    def get_cpu_temp(self):
        res = os.popen("vcgencmd measure_temp").readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))

    def get_smooth(self, x):
        if not hasattr(get_smooth, "t"):
            getsmooth.t = [x, x, x]
        get_smooth.t[2] = get_smooth.t[1]
        get_smooth.t[1] = get_smooth.t[0]
        get_smooth.t[0] = x
        return (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3

    def fixTemp(self):
        t1 = self.sense.get_temperature_from_humidity()
        t2 = self.sense.get_temperature_from_pressure()
        t_cpu = self.get_cpu_temp()
        h = self.sense.get_humidity()
        p = self.sense.get_pressure()
        # Calculates the real temperature compesating CPU heating.
        t = (t1 + t2) / 2
        t_corr = t - ((t_cpu - t) / 1.5)
        print("t_corr", t_corr)
        t_corr = self.get_smooth(t_corr)

    def evaluateStatus(self, item, value, min, max, unit):
        if value < min:
            status = item + " is below minimum ({} {})".format(min, unit)
        elif value > max:
            status = item + " is above maximum ({} {})".format(max, unit)
        else:
            return ""
        return status

    def main(self):
        temperature = self.sense.get_temperature()
        humidity = self.sense.get_humidity()
        print("humidity", humidity)
        print("temperature", temperature)
        # temperature = self.fixTemp()
        sendstatus = "All Good"
        # sendstatus = self.evaluate status
        # temperatureStatus = self.evaluateStatus("Temperature", int(temperature), self.minTemp, self.maxTemp, "*C")
        # humidityStatus = self.evaluateStatus("Humidity", int(humidity), self.minHumidity, self.maxHumidity, "%")
        # if temperatureStatus == "" and humidityStatus == "":
        # sendstatus = "All Good"
        # if temperatureStatus != "" and humidityStatus != "":
        # sendstatus = temperatureStatus + humidityStatus
        # if temperatureStatus != "" and humidityStatus == "":
        # sendstatus = temperatureStatus
        # if temperatureStatus == "" and humidityStatus != "":
        # sendstatus =  humidityStatus

        nearby_devices = bluetooth.discover_devices()
        print(self.pb.devices)
        for macAddress in nearby_devices:
            print("Found device with mac-address: " + macAddress)
            body = "Currently the temperature is {:.2f} *C and the humidity is {:.2f} % \n Status Report: {}" .format(temperature, humidity, sendstatus)
            self.send_notification_via_pushbullet("Update", body)

# Execute program
Greenhouse_Bluetooth = Greenhouse_Bluetooth()
Greenhouse_Bluetooth.initRange()
Greenhouse_Bluetooth.main()
