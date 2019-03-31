from bokeh.plotting import figure, output_file, show
from database import Database
from datetime import datetime, date
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

class Analytics:
    def __init__(self, databaseName = 'VirtualSenseHat.db'):
        self.databaseName = databaseName
        self.database = Database(self.databaseName)
        self.date = date.today()

    def prepareDataStraightPlot(self):
        self.time, self.temperature, self.humidity = self.database.getWeatherDataOn(self.date)

    def plotTemperature(self):

        x = self.time
        y = self.temperature

        # output to static HTML file
        output_file("TemperaturePlot.html")

        # create a new plot with a title and axis labels
        p = figure(title="Temperature for {}".format(date), x_axis_label='Time', y_axis_label='Temperature (*C)')

        # add a line renderer with legend and line thickness
        p.line(x, y, legend="Temp.", line_width=2)

        # show the results
        show(p)

analytics = Analytics()
analytics.prepareDataStraightPlot()
analytics.plotTemperature()
# # prepare some data
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]





 
# # data
# df=pd.DataFrame({'x': range(1,10), 'y': np.random.randn(9)*80+range(1,10) })
 
# # plot
# plt.plot( 'x', 'y', data=df, linestyle='-', marker='o')
# plt.show()
