from database import Database
import logging
import json
import csv
import re

logging.basicConfig(level=logging.DEBUG)


class Report:

    def getReportName(self):
        validfilename = False
        print("What would you like to name the report file? \nEnter the name only, the file extension will be added automatically ")
        while validfilename is False:
            filename = input()
            # check file name contains no spaces or special characters
            regex = re.compile(' [@_!#$%^&*()<>?/\|}{~:] ')
            if regex.search(filename) is None and (' ' in filename) is False:
                reportfilename = filename + ".csv"
                print("Filename:", reportfilename)
                validfilename = True
                return reportfilename
            else:
                print("That filename is not valid, Please try again:")
                print("New file name: ")
                validfilename = False

    def __init__(self):
        self.configFilename = 'config.json'
        self.reportFilename = 'report.csv'  #self.getReportName()
        self.databaseName = 'VirtualSenseHat.db'

        self.database = Database(self.databaseName)
        self.reportData = [["Date", "Status"]]

    def initRange(self):
        with open(self.configFilename, "r") as file:
            self.range = json.load(file)

        self.minTemp = self.range["min_temperature"]
        self.maxTemp = self.range["max_temperature"]
        self.minHumidity = self.range["min_humidity"]
        self.maxHumidity = self.range["max_humidity"]         

    def evaluateStatus(self, value, min, max, unit):
        if value < min:
            different = round(min - value, 2) 
            status = "{}{} below minimum (Minimum is {} {})".format(str(different), unit, min, unit)

        elif value > max:
            different = round(value - max, 2)
            status = "{}{} above maximum (Maximum is {} {})".format(str(different), unit, max, unit)
        else:
            return ""
        return status

    def computeReportData(self):
        for entry in self.database.readSenseHatData():
            date = entry[0]
            temperature = entry[2]
            humidity = entry[3]

            temperatureStatus = ""
            humidityStatus = ""
            shortStatus = ""    # "OK" or "BAD"

            reportData = [date]

            logging.debug('Data read from database is as follows')
            logging.debug('Date: {}'.format(date))
            logging.debug('Temperature: {0:0.1f} *C'.format(temperature))
            logging.debug('Humidity: {0:0.0f} %'.format(humidity))

            temperatureStatus = self.evaluateStatus(float(temperature), self.minTemp, self.maxTemp, "*C")
            humidityStatus = self.evaluateStatus(float(humidity), self.minHumidity, self.maxHumidity, "%")

            if temperatureStatus or humidityStatus:
                shortStatus = "BAD"
            else:
                shortStatus = "OK"
            reportData.append(shortStatus)

            if temperatureStatus:
                reportData.append(temperatureStatus)
            if humidityStatus:
                reportData.append(humidityStatus)

            self.reportData.append(reportData)
            logging.debug(reportData)

    def writeFile(self):
        logging.debug("Full report data after evaluating: {}".format(self.reportData))
        with open(self.reportFilename, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(self.reportData)
        csvFile.close()
        logging.debug("All report data is written to {}".format(self.reportFilename))

    def printFile(self):     # for debugging
        with open(self.reportFilename, 'r') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                logging.debug(row)
        csvFile.close()

    def generateReport(self):
        self.initRange()
        self.computeReportData()
        self.writeFile()
        self.printFile()

report = Report()
report.generateReport()