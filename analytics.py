from bokeh.plotting import figure, output_file, show
from bokeh.models import DatetimeTicker, FactorRange

from database import Database
from defineTimezone import *
import logging

import matplotlib.pyplot as plt
import matplotlib.axes
import seaborn as sns
import numpy as np
import pandas as pd




logging.basicConfig(level = logging.DEBUG)

class Analytics:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):  # "fakeData.db"
        self.databaseName = databaseName
        self.database = Database(self.databaseName) 
        self.currentDate = datetime.today().date() - ONE_DAY_DELTA

    def prepareDataLinePlot(self, dataDate = None):
        # prepare some data
        if dataDate == None:
            dataDate = self.currentDate
        self.time, self.temperature, self.humidity = self.database.getWeatherDataOn(dataDate)
        logging.debug('Time series: ')
        logging.debug(self.time)
        logging.debug('Temperature series: ')
        logging.debug(self.temperature)
        logging.debug('Humidity series: ')
        logging.debug(self.humidity)
        self.dataDate = dataDate
    
    def prepareDataBarPlot(self):
        self.date, self.avgTemperature, self.avgHumidity = self.database.getAverageWeatherData(endDate = self.currentDate)
        logging.debug('Date series: ')
        logging.debug(self.date)
        logging.debug('Avg temperature series: ')
        logging.debug(self.avgTemperature)
        logging.debug('Avg humidity series: ')
        logging.debug(self.avgHumidity)

    def plotLineGraph(self, x_list, y_list, value, unit):
        # data
        #df=pd.DataFrame({'x': x_list, 'y': y_list})

        # output to static HTML file
        output_file("{}Plot.html".format(value))
        figureTitle = "{} for {}".format(value, self.dataDate.strftime(DATE_FORMAT))
        x_axis_label= 'Time'
        y_axis_label= '{} ({})'.format(value, unit)

        # create a new plot with a title and axis labels
        p = figure(plot_width=1200, plot_height=600, title=figureTitle, x_axis_label=x_axis_label, y_axis_label=y_axis_label, x_axis_type="datetime")

        # add a line renderer with legend and line thickness
        p.xaxis.ticker = DatetimeTicker(desired_num_ticks = 24)
        p.line(x_list, y_list, legend=value, line_width=2)

        # show the results
        show(p)

    def plotBarGraph(self, x_list, y_list, value, unit):
        output_file = "{}Plot.html".format(value.title().replace(' ', ''))
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
            p.y_range.end = 70
        else:
            p.y_range.end = 70
        show(p)


    def plotTemperature(self):
        self.plotLineGraph(self.time, self.temperature, "Temperature", "*C")

    def plotHumidity(self):
        self.plotLineGraph(self.time, self.humidity, "Humidity", "%")

    def plotAvgTemperature(self):
        self.plotBarGraph(self.date, self.avgTemperature, "Average temperature", "*C")

    def plotAvgHumidity(self):
        self.plotBarGraph(self.date, self.avgHumidity, "Average humidity", "%")


    def plotLineMatplotlib(self, x_list, y_list, value, unit):
        output_file = "{}Plot.png".format(value.title().replace(' ', ''))
        df=pd.DataFrame({'time': x_list, value : y_list})
 
        # plot
        figure, axes = plt.subplots(figsize=(16,6))
        axes.plot('time', value, data=df, marker='o', color='mediumvioletred')
        plt.title("{} for {}".format(value, self.dataDate.strftime(DATE_FORMAT)))
        plt.xlabel("Time")
        plt.ylabel('{} ({})'.format(value, unit))

        plt.legend()
        plt.grid(True)

        plt.xticks([i.strftime("%H:%M") for i in x_list])
        logging.debug(plt.xticks())
        if unit == "*C":
            plt.ylim(0,70)
        else:
            plt.ylim(0,70)

        plt.savefig(output_file)
        plt.show()

    def plotBarMatplotlib(self, x_list, y_list, value, unit):
        output_file = "{}Plot.png".format(value.title().replace(' ', ''))
        figureTitle = "{} for {} to {}".format(value, x_list[0], x_list[-1])

        df=pd.DataFrame({'date': x_list, value : y_list})
 
        # plot
        figure, axes = plt.subplots(figsize=(16,6))
        axes.bar('date', value, data=df, color='mediumvioletred')
        plt.title("{} for {}".format(value, self.dataDate.strftime(DATE_FORMAT)))
        plt.xlabel('Date')
        plt.ylabel('{} ({})'.format(value, unit))

        plt.legend()
        plt.grid(axis = 'y')

        plt.xticks(self.date)
        logging.debug(plt.xticks())
        if unit == "*C":
            plt.ylim(0,50)
        else:
            plt.ylim(0,80)

        plt.savefig(output_file)
        plt.show()

    def plotTemperatureMatplotlib(self):
        self.plotLineMatplotlib(self.time, self.temperature, "Temperature", "*C")

    def plotHumidityMatplotlib(self):
        self.plotLineMatplotlib(self.time, self.humidity, "Humidity", "%")

    def plotAvgTemperatureMatplotlib(self):
        self.plotBarMatplotlib(self.date, self.avgTemperature, "Average temperature", "*C")

    def plotAvgHumidityMatplotlib(self):
        self.plotBarMatplotlib(self.date, self.avgHumidity, "Average humidity", "%")

analytics = Analytics()

# analytics.prepareDataLinePlot()
# analytics.plotTemperature()       #Using Bokeh
# analytics.plotHumidity()          #Using Bokeh
# analytics.plotTemperatureMatplotlib()   
# analytics.plotHumidityMatplotlib()


analytics.prepareDataBarPlot()
analytics.plotAvgTemperature()    #Using Bokeh
analytics.plotAvgHumidity()       #Using Bokeh
analytics.plotAvgTemperatureMatplotlib()
analytics.plotAvgHumidityMatplotlib()
