#Does the report contain all of the requisite data?
#How neat and professional is the display?
#Have appropriate labels (OK v/s BAD) been appended to each of the rows?
#Have you handled file related exceptions in your code?
#What type of data validation rules have you implemented?
#Consider the user input angle.

import datetime
import re

Min_Temperature = 20
Max_Temperature = 30
Min_Humidity = 50
Max_Humidity = 60

validfilename = False
print("What would you like to name the report file? \nEnter the name only, the file extension will be added automatically ")
while validfilename == False:
    filename = input()
    #check file name contains no spaces or special characters
    regex = re.compile(' [@_!#$%^&*()<>?/\|}{~:] ')
    if regex.search(filename) == None and (' ' in filename) == False:
        reportfilename = filename + ".csv"
        print("Filename:", reportfilename)
        validfilename = True
    else: 
        print("That filename is not valid, Please try again:")
        print("New file name: ")
        validfilename = False

f = open(reportfilename, "w+")

#Have you handled file related exceptions in your code?
f.write("Date, Status \n")

validresponse = False
while(validresponse == False):
    print("Would you like to enter a new range for the temperature and humidity")
    print("Min Temperature:", Min_Temperature)
    print("Max Temperature:", Max_Temperature)
    print("Min Humidity:", Min_Humidity)
    print("Max Humidity:", Max_Humidity)
    print("Enter: Yes or No")
    adjustrangeanswer = input()

    if adjustrangeanswer.lower() == "yes":
        validMinT = False
        validMaxT = False
        validMinH = False
        validMaxH = False
        while (validMinT == False):
            print("Enter new Min Temperature value:")
            Min_Temperature = input()
            if Min_Temperature.isdigit():
                validMinT = True
            else:
                print("That is not a valid temperature value")
        
        while (validMaxT == False):
            print("Enter new Max Temperature value:")
            Max_Temperature = input()
            if Max_Temperature.isdigit():
                validMaxT = True
            else:
                print("That is not a valid temperature value")

        while (validMinH == False):
            print("Enter new Min Humidity value:")
            Min_Humidity = input()
            if Min_Humidity.isdigit():
                validMinH = True
            else:
                print("That is not a valid temperature value") 

        while (validMaxH == False):
            print("Enter new Max Humidity value:")
            Max_Humidity = input()
            if Max_Humidity.isdigit():
                validMaxH = True
            else:
                print("That is not a valid temperature value")  
        
        print("Values have been change")
        validresponse = True
    elif adjustrangeanswer.lower() == "no":
        print("Values shall not be change")
        validresponse = True
    else :
        print("That response was not valid \n")
        validresponse = False



#loop through daily data
for i in range(2):
    x = datetime.datetime.now()
    #'%Y-%m-%d'
    
    #check days reading in data base
    #if within range OK
    #else status BAD
    status = "BAD:"




#Have you handled file related exceptions in your code?
    f.write(x.strftime('%d/%m/%Y,'))
    f.write(status)
    f.write("\n")