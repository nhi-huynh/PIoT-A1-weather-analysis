from database import Database

class Notification:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)

        self.database.populatePushbulletData()

notification = Notification()

    