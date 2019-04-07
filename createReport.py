from database import Database
import logging
import json
import csv
import re

logging.basicConfig(level=logging.DEBUG)


class Report:

    def getReportName(self):
        validfilename = False
        print("What would you like to name the report file?")
        print("Enter a name only, the file extension will be added")
        while validfilename is False:
            filename = input()
            # check file name contains no spaces or special characters
            regex = re.compile(' [@_!#$%^&*()<>?/\|}{~:] ')
            if regex.search(filename) is None and (' ' in filename) is False:
                reportfilename = filename + ".csv"
                validfilename = True
                return reportfilename
            else:
                print("That filename is not valid, Please try again:")
                print("New file name: ")
                validfilename = False

    def __init__(self):
        self.configFilename = 'config.json'
        self.reportFilename = self.getReportName()
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

    def evaluateStatus(self, value, unit, min=None, max=None):
        if unit == "*C":
            item = "temperature"
        else:
            item = "humidity"
        if max is None:
            if value < min:
                different = round(min - value, 2)
                status = "{}{} below minimum {} (Minimum is {} {})".format(
                    str(different), unit, item, min, unit)
            else:
                return ""
        if min is None:
            if value > max:
                different = round(value - max, 2)
                status = "{}{} above maximum {} (Maximum is {} {})".format(
                    str(different), unit, item, max, unit)
            else:
                return ""
        return status

    def computeReportData(self):
        maxDevTemperature, maxDevHumidity = self.database.getMaxMinDataPerDay()

        for date in maxDevTemperature.keys():
            temperatureStatus = []
            humidityStatus = []
            reportRow = [date]

            temperatureStatus.append(
            self.evaluateStatus(
                maxDevTemperature[date][0], "*C", max=self.maxTemp))
            temperatureStatus.append(
            self.evaluateStatus(
                maxDevTemperature[date][1], "*C", min=self.minTemp))
            humidityStatus.append(
                self.evaluateStatus(
                    maxDevHumidity[date][0], "%", max=self.maxHumidity))
            humidityStatus.append(
                self.evaluateStatus(
                    maxDevHumidity[date][1], "%", min=self.minHumidity))

            if temperatureStatus != ["", ""] or humidityStatus != ["", ""]:
                shortStatus = "BAD"
            else:
                shortStatus = "OK"

            reportRow.append(shortStatus)

            reportRow += [
                status for status in temperatureStatus if status != ""]
            reportRow += [
                status for status in humidityStatus if status != ""]

            self.reportData.append(reportRow)

    def writeFile(self):
        with open(self.reportFilename, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(self.reportData)
        csvFile.close()
        logging.debug("All report data is written to {}".format(
            self.reportFilename))

    def generateReport(self):
        self.initRange()
        self.computeReportData()
        self.writeFile()

report = Report()
report.generateReport()
