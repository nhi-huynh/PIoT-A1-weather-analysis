# Reference: https://raspberrypi.stackexchange.com/questions/61524/how
# to-approximate-room-temperature-in-a-better-way
import os
import time


# Get CPU temperature.
def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))


# Use moving average to smooth readings.
def get_smooth(x):
    if not hasattr(get_smooth, "t"):
        get_smooth.t = [x, x, x]

    get_smooth.t[2] = get_smooth.t[1]
    get_smooth.t[1] = get_smooth.t[0]
    get_smooth.t[0] = x

    return (get_smooth.t[0] + get_smooth.t[1] + get_smooth.t[2]) / 3
