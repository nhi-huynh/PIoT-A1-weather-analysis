from database import Database

class Notification:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)

        self.database.pre_populatePushbullet()
        self.database.hasSentNotification() #check if notification is sent for today yet

    def prepareTable(self):
        self.database.re_populatePushbullet()

    
notification = Notification()

    