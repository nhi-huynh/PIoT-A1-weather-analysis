from virtual_sense_hat import VirtualSenseHat
# from sense_hat import SenseHat use this when we test on Pi
from databaseClass import Database
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
ACCESS_TOKEN = "o.SED5fMSZb6RoIOAUX2tJtko1HoseOVbq"


class Monitor:

    def __init__(self, databaseName='VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.pushDatabaseName = 'PushNotification.db'
        self.configFilename = 'config.json'
        self.database = Database(self.databaseName)
        self.sense = VirtualSenseHat.getSenseHat()
        # self.sense = SenseHat.getSenseHat() #use this when we test on Pi

    def initRange(self):
        with open(self.configFilename, "r") as file:
            self.range = json.load(file)

        self.minTemp = self.range["min_temperature"]
        self.maxTemp = self.range["max_temperature"]
        self.minHumidity = self.range["min_humidity"]
        self.maxHumidity = self.range["max_humidity"]

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

    def CheckDatabase(self):
        cursor = mySQLconnection .cursor()
        cursor.rowcount
        cursor.execute("SELECT * FROM table ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
                title (str) : Title of text.
                body (str) : Body of text.
        """
        data = {"type": "note", "title": title, "body": body}

        response = requests.post("https://api.pushbullet.com/v2/pushes", data=json.dumps(data), headers={"Authorization": "Bearer " + ACCESS_TOKEN, "Content-Type": "application/json"})
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

        # This code is for assignment submission
        # while (True): forever loop
        # self.readSenseHatData()
        # self.database.insertEntry(self.time, self.temperature, self.humidity)

        # if self.CheckDatabase() == False:
        # sendstatus = "All Good"
        # temperatureStatus = self.evaluateStatus("Temperature", int(self.temperature), self.minTemp, self.maxTemp, "*C")
        # humidityStatus = self.evaluateStatus("Humidity", int(self.humidity), self.minHumidity, self.maxHumidity, "%")
        # if temperatureStatus == "" and humidityStatus == "":
            # sendstatus = "All Good"
        # elif temperatureStatus != "" and humidityStatus != "":
            # sendstatus = temperatureStatus + " and " + humidityStatus
        # elif temperatureStatus != "" and humidityStatus == "":
            # sendstatus = temperatureStatus
        # elif temperatureStatus == "" and humidityStatus != "":
            # sendstatus = humidityStatus
            # send_notification_via_pushbullet("Weather Update", notification)

        # logging.debug('\nWaiting for 1 minute...\n')
        # time.sleep(60)

        # debugging only:Read SenseHat data every 5s for 10 times
        for i in range(10):
            self.readSenseHatData()
            self.database.insertEntry(self.time, self.temperature, self.humidity)
            logging.debug('Waiting for 1 minute...\n')
            # time.sleep(60)

    def stopMonitoring(self):
        logging.debug('Stop monitoring...\nStop writing to the database...')
        self.database.closeDatabase()

monitor = Monitor()
monitor.initRange()
monitor.startMonitoring()
