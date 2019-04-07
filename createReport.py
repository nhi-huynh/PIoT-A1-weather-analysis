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
        maxDeviationTemperature, maxDeviationHumidity = self.database.getMaxMinDataPerDay()

        for date in maxDeviationTemperature.keys():
            reportRow = [date]
            temperatureStatus = [self.evaluateStatus(temperature, self.minTemp, self.maxTemp, "*C") for temperature in maxDeviationTemperature[date]]
            humidityStatus = [self.evaluateStatus(humidity, self.minHumidity, self.maxHumidity, "%") for humidity in maxDeviationHumidity[date]]

            if temperatureStatus != ["", ""] or humidityStatus != ["", ""]:
                shortStatus = "BAD"
            else:
                shortStatus = "OK"
            
            reportRow.append(shortStatus)

            if temperatureStatus != ["", ""]:
                reportRow += temperatureStatus
            if humidityStatus != ["", ""]:
                reportRow += humidityStatus
                
            self.reportData.append(reportRow)
            logging.debug(reportRow)
        
        

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