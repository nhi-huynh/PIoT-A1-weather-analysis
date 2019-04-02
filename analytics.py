from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTicker, FactorRange
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
        

    def prepareDataStraightPlot(self, dataDate = datetime.today().date()):
        # prepare some data
        self.time, self.temperature, self.humidity = self.database.getWeatherDataOn(dataDate)
        logging.debug('Time series: ')
        logging.debug(self.time)
        logging.debug('Temperature series: ')
        logging.debug(self.temperature)
        logging.debug('Humidity series: ')
        logging.debug(self.humidity)
        return dataDate
    
    def prepareDataBarPlot(self):
        self.date, self.avgTemperature, self.avgHumidity = self.database.getAverageWeatherData()
        logging.debug('Date series: ')
        logging.debug(self.date)
        logging.debug('Avg temperature series: ')
        logging.debug(self.avgTemperature)
        logging.debug('Avg humidity series: ')
        logging.debug(self.avgHumidity)

    def plotBarGraph(self, x_list, y_list, value, unit):
        output_file("{}Plot.html".format(value.capitalize().replace(' ', '')))
        figureTitle = "{} for {} to {}".format(value, x_list[0], x_list[-1])
        x_axis_label='Date'
        y_axis_label='{} ({})'.format(value, unit)
        p = figure(x_range=self.date, plot_width=600, plot_height=400, title= figureTitle, x_axis_label=x_axis_label, y_axis_label=y_axis_label, toolbar_location=None, tools="")
        #x_range=self.date, x_range=FactorRange(self.date)
        #p.xaxis.ticker = days
        p.vbar(x=x_list, top=y_list, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        if unit == "*C":
            p.y_range.end = 50
        else:
            p.y_range.end = 80
        show(p)


    def plotLineGraph(self, x_list, y_list, value, unit, prepareDataMethod):
        # data
        #df=pd.DataFrame({'x': x_list, 'y': y_list})

        # output to static HTML file
        output_file("{}Plot.html".format(value))

        # create a new plot with a title and axis labels
        date = prepareDataMethod()
        p = figure(plot_width=1200, plot_height=600, title="{} for {}".format(value, date.strftime(DATE_FORMAT)), x_axis_label='Time', y_axis_label='{} ({})'.format(value, unit), x_axis_type="datetime")

        # add a line renderer with legend and line thickness
        p.xaxis.ticker = DatetimeTicker(desired_num_ticks = 24)
        p.line(x_list, y_list, legend=value, line_width=2)

        # show the results
        show(p)

    def plotTemperature(self):
        self.plotLineGraph(self.time, self.temperature, "Temperature", "*C", self.prepareDataStraightPlot)

    def plotHumidity(self):
        self.plotLineGraph(self.time, self.humidity, "Humidity", "%", self.prepareDataStraightPlot)

    def plotAvgTemperature(self):
        self.plotBarGraph(self.date, self.avgTemperature, "Average temperature", "*C")

    def plotAvgHumidity(self):
        self.plotBarGraph(self.date, self.avgHumidity, "Average humidity", "%")


analytics = Analytics()

analytics.prepareDataStraightPlot()
analytics.plotTemperature()
analytics.plotHumidity()

analytics.prepareDataBarPlot()
analytics.plotAvgTemperature()
analytics.plotAvgHumidity()

