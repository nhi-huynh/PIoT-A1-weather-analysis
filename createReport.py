from database import Database
import logging
import json
import csv

logging.basicConfig(level = logging.DEBUG)

class Report:

    def __init__(self):
        self.configFilename = 'config.json'
        self.reportFilename = 'report.csv'
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
            different = min - value
            status = "{}{} below minimum (Minimum is {} {})".format(different, unit, min, unit)
        elif value > max:
            different = value - max
            status = "{}{} above maximum (Maximum is {} {})".format(str(different), unit, max, unit)
        else:
            return ""
        return status

    def computeReportData(self):
        for entry in self.database.readDataEntries():
            date = entry[0][:10]
            temperature = entry[1]
            humidity = entry[2]

            temperatureStatus = ""
            humidityStatus = ""
            shortStatus = ""    #"OK" or "BAD"

            reportData = [date]

            logging.debug('Data read from database is as follows')
            logging.debug('Date: {}'.format(date))
            logging.debug('Temperature: {0:0.1f} *C'.format(temperature))
            logging.debug('Humidity: {0:0.0f} %'.format(humidity))

            temperatureStatus = self.evaluateStatus(int(temperature), self.minTemp, self.maxTemp, "*C")
            humidityStatus = self.evaluateStatus(int(humidity), self.minHumidity, self.maxHumidity, "%")

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

    def printFile(self):     #for debugging
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


# #Does the report contain all of the requisite data?
# #How neat and professional is the display?
# #Have appropriate labels (OK v/s BAD) been appended to each of the rows?
# #Have you handled file related exceptions in your code?
# #What type of data validation rules have you implemented?
# #Consider the user input angle.

# import datetime
# import re

# Min_Temperature = 20
# Max_Temperature = 30
# Min_Humidity = 50
# Max_Humidity = 60

# validfilename = False
# print("What would you like to name the report file? \nEnter the name only, the file extension will be added automatically ")
# while validfilename == False:
#     filename = input()
#     #check file name contains no spaces or special characters
#     regex = re.compile(' [@_!#$%^&*()<>?/\|}{~:] ')
#     if regex.search(filename) == None and (' ' in filename) == False:
#         reportfilename = filename + ".csv"
#         print("Filename:", reportfilename)
#         validfilename = True
#     else: 
#         print("That filename is not valid, Please try again:")
#         print("New file name: ")
#         validfilename = False

# f = open(reportfilename, "w+")

# #Have you handled file related exceptions in your code?
# f.write("Date, Status \n")

# validresponse = False
# while(validresponse == False):
#     print("Would you like to enter a new range for the temperature and humidity")
#     print("Min Temperature:", Min_Temperature)
#     print("Max Temperature:", Max_Temperature)
#     print("Min Humidity:", Min_Humidity)
#     print("Max Humidity:", Max_Humidity)
#     print("Enter: Yes or No")
#     adjustrangeanswer = input()

#     if adjustrangeanswer.lower() == "yes":
#         validMinT = False
#         validMaxT = False
#         validMinH = False
#         validMaxH = False
#         while (validMinT == False):
#             print("Enter new Min Temperature value:")
#             Min_Temperature = input()
#             if Min_Temperature.isdigit():
#                 validMinT = True
#             else:
#                 print("That is not a valid temperature value")
        
#         while (validMaxT == False):
#             print("Enter new Max Temperature value:")
#             Max_Temperature = input()
#             if Max_Temperature.isdigit():
#                 validMaxT = True
#             else:
#                 print("That is not a valid temperature value")

#         while (validMinH == False):
#             print("Enter new Min Humidity value:")
#             Min_Humidity = input()
#             if Min_Humidity.isdigit():
#                 validMinH = True
#             else:
#                 print("That is not a valid temperature value") 

#         while (validMaxH == False):
#             print("Enter new Max Humidity value:")
#             Max_Humidity = input()
#             if Max_Humidity.isdigit():
#                 validMaxH = True
#             else:
#                 print("That is not a valid temperature value")  
        
#         print("Values have been change")
#         validresponse = True
#     elif adjustrangeanswer.lower() == "no":
#         print("Values shall not be change")
#         validresponse = True
#     else :
#         print("That response was not valid \n")
#         validresponse = False



# #loop through daily data
# for i in range(2):
#     x = datetime.datetime.now()
#     #'%Y-%m-%d'
    
#     #check days reading in data base
#     #if within range OK
#     #else status BAD
#     status = "BAD:"




# #Have you handled file related exceptions in your code?
#     f.write(x.strftime('%d/%m/%Y,'))
#     f.write(status)
#     f.write("\n")