"wind_speeds.py"
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':19})

def get_windspeed(latitude, perc, altitude, path="windspeeds/"):
    """
    Method to return windspeeds for different latitudes altitudes/percentiles
    Inputs
    ------
    latitude: latitude of the earth [deg]
    perc: percentile wind speed, only accepts [70, 75, 80, 95, 90, 95, 99]
    altitude: altitude [ft] (can be array or single value)
    path: terminal path to location of windspeed files

    Returns
    -------
    wind: wind speed [m/s] (array if altitude is array)
    """

    # pressure ranges for which there is data
    pressures = [5, 10, 30] + range(50, 1050, 50)
    pressures = np.array(pressures)
    filename = None

    if not hasattr(altitude, "__len__"):
        altitude = [altitude]

    wind = []
    for a in altitude:
        h = a*0.3048
        p = 101325.0/100*(1 - 2.25577e-5*h)**5.25588
        ind = np.abs(pressures-p).argmin()
        mb = [0]*2
        if ind == 0:
            mb[0] = pressures[0]
            mb[1] = pressures[1]
        elif pressures[ind] > p:
            mb[0] = pressures[ind-1]
            mb[1] = pressures[ind]
        else:
            mb[0] = pressures[ind]
            mb[1] = pressures[ind+1]

        w = []
        for m in mb:
            filename = "%swind%d.csv" % (path, m)
            df = pd.read_csv(filename)
            w.append(df[df["Latitude"] == latitude]["perc%d" % perc].item())

        wind.append(interpolate(mb, w, p))

    if len(wind) == 1:
        wind = wind[0]

    return wind

def interpolate(xs, ys, x):
    "interpolates between two points at some x location"
    y = ((ys[1]-ys[0])/(xs[1]-xs[0])*x +
         (ys[0]*xs[1] - ys[1]*xs[0])/(xs[1]-xs[0]))
    return y

if __name__ == "__main__":

    Fig, Ax = plt.subplots()
    for av in [80, 90, 95]:
        Wind = []
        for l in np.arange(0, 70, 1):
            Wind.append(get_windspeed(l, av, 16000))
        Ax.plot(Wind, np.arange(0, 70, 1))

    Ax.set_ylabel("Latitude [deg]")
    Ax.set_xlabel("Wind speed [m/s]")
    Ax.set_ylim([0, 70])
    Ax.grid()
    Ax.legend(["%d Percentile Winds" % b for b in [80, 90, 95]], loc=2,
              fontsize=15)
    Fig.savefig("latvswindh16.pdf", bbox_inches="tight")

    Fig, Ax = plt.subplots()
    for av in [80, 90, 95]:
        Wind = []
        for l in np.arange(0, 70, 1):
            Wind.append(get_windspeed(l, av, 50000))
        Ax.plot(Wind, np.arange(0, 70, 1))

    Ax.set_ylabel("Latitude [deg]")
    Ax.set_xlabel("Wind speed [m/s]")
    Ax.set_ylim([0, 70])
    Ax.grid()
    Ax.legend(["%d Percentile Winds" % b for b in [80, 90, 95]], loc=2,
              fontsize=15)
    Fig.savefig("latvswindh50.pdf", bbox_inches="tight")

    Fig, Ax = plt.subplots()
    Alt = range(1000, 80000, 1000)
    for av in [80, 90, 95]:
        Wind = []
        for h0 in Alt:
            Wind.append(get_windspeed(45, av, h0))
        Ax.plot(Wind, Alt)
    Ax.set_ylabel("Altitude [ft]")
    Ax.set_xlabel("Wind speed [m/s]")
    Ax.set_ylim([0, 100000])
    Ax.grid()
    Ax.legend(["%d Percentile Winds" % b for b in [80, 90, 95]], loc=1,
              fontsize=15)
    Fig.savefig("altvswindl45.pdf", bbox_inches="tight")

    Fig, Ax = plt.subplots()
    for av in [80, 90, 95]:
        Wind = []
        for h0 in Alt:
            Wind.append(get_windspeed(30, av, h0))
        Ax.plot(Wind, Alt)
    Ax.set_ylabel("Altitude [ft]")
    Ax.set_xlabel("Wind speed [m/s]")
    Ax.set_ylim([0, 100000])
    Ax.grid()
    Ax.legend(["%d Percentile Winds" % b for b in [80, 90, 95]], loc=1,
              fontsize=15)
    Fig.savefig("altvswindl30.pdf", bbox_inches="tight")