from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTicker
from database import Database
from datetime import datetime, date, timedelta
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"

ONE_DAY_DELTA = timedelta(days = 1)
ONE_HOUR_DELTA = timedelta(hours = 1)

logging.basicConfig(level = logging.DEBUG)

class Analytics:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)
        self.date = datetime.today().date()

    def prepareDataStraightPlot(self):
        # prepare some data
        self.time, self.temperature, self.humidity = self.database.getWeatherDataOn(self.date)
        logging.debug('Time series: ')
        logging.debug(self.time)
        logging.debug('Temperature series: ')
        logging.debug(self.temperature)
        logging.debug('Humidity series: ')
        logging.debug(self.humidity)

    def plotAgainstTime(self, x_list, y_list, value, unit):
        # data
        df=pd.DataFrame({'x': x_list, 'y': y_list})

        # output to static HTML file
        output_file("{}Plot.html".format(value))

        # create a new plot with a title and axis labels
        p = figure(plot_width=1200, plot_height=600, title="{} for {}".format(value, self.date.strftime(DATE_FORMAT)), x_axis_label='Time', y_axis_label='{} ({})'.format(value, unit), x_axis_type="datetime")

        # add a line renderer with legend and line thickness
        p.xaxis.ticker = DatetimeTicker(desired_num_ticks = 24)
        p.line(x_list, y_list, legend=value, line_width=2)

        # show the results
        show(p)

    def plotTemperature(self):
        self.plotAgainstTime(self.time, self.temperature, "Temperature", "*C")

    def plotHumidity(self):
        self.plotAgainstTime(self.time, self.humidity, "Humidity", "%")

analytics = Analytics()
analytics.prepareDataStraightPlot()
analytics.plotTemperature()
analytics.plotHumidity()

