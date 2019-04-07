# Author: Matthew Bolger
# Can be used and/or edited for any purpose (including the assignment).

import logging
import random

try:
    from sense_hat import SenseHat
except ImportError:
    pass

class VirtualSenseHat:
    @staticmethod
    def getSenseHat(logError = True):
        try:
            return SenseHat()
        except Exception as e:
            #if(logError):
                #logging.error("Falling back to VirtualSenseHat because: " + str(e))
            return VirtualSenseHat()

    def get_temperature(self, min = 1000, max = 3000):
        return random.randint(min, max) / 100

    def get_humidity(self, min = 5000, max = 6000):
        return random.randint(min, max) / 100

    def show_message(self, text_string,
        scroll_speed = 0.1, text_colour = [255, 255, 255], back_colour = [0, 0, 0]):
        print(text_string)

    def clear(self):
        pass
