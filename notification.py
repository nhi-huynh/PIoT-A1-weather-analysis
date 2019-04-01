from database import Database
from datetime import date

class Notification:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)

        self.database.pre_populatePushbullet()  #inseart default data to pushbullet_data table

    def prepareTable(self):
        self.database.re_populatePushbullet()   #call this everytime 
        self.database.hasSentNotification() #check if notification is sent for today yet

        self.database.updateSentStatus(date.today())

    

    
notification = Notification()
notification.prepareTable()


    