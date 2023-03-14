import time
import tlesearch
import updatedb
import datalink
from datetime import datetime
import datetime
from math import *
import ephem

# Check the serial port
ser, comm = datalink.link_arduino()

# Wait for the Arduino to reset
time.sleep(2)

# Update satellite database
updatedb.askupdate()

# Get satellite TLE
groundcoord, tle = tlesearch.search()


class Tracker:
    # refer to "https://gist.github.com/andresv/920f7bbf03f91a5967ee"

    def __init__(self, satellite, groundstation=groundcoord):
        self.groundstation = ephem.Observer()
        self.groundstation.lat = groundstation[0]
        self.groundstation.lon = groundstation[1]
        self.groundstation.elevation = int(groundstation[2])
        self.satellite = ephem.readtle(satellite["name"], satellite["tle1"], satellite["tle2"])

    def set_epoch(self, epoch=time.time()):
        """ sets epoch when parameters are observed """

        self.groundstation.date = datetime.datetime.utcfromtimestamp(epoch)
        self.satellite.compute(self.groundstation)

    def azimuth(self):
        """ returns satellite azimuth in degrees """
        return degrees(self.satellite.az)

    def elevation(self):
        """ returns satellite elevation in degrees """
        return degrees(self.satellite.alt)

    def latitude(self):
        """ returns satellite latitude in degrees """
        return degrees(self.satellite.sublat)

    def longitude(self):
        """ returns satellite longitude in degrees """
        return degrees(self.satellite.sublong)

    def range(self):
        """ returns satellite range in meters """
        return self.satellite.range


tracker = Tracker(satellite=tle, groundstation=groundcoord)

while True:
    try:
        tracker.set_epoch(time.time())
        az = tracker.azimuth()
        el = tracker.elevation()
        data = f"{az},{el}\n".encode()
        if comm:
            ser.write(data)
        print("Azimuth: ", az)
        print("Elevation: ", el)
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nTracker paused")
        ser, comm = datalink.link_arduino()
        groundcoord, tle = tlesearch.search()
        tracker = Tracker(satellite=tle, groundstation=groundcoord)
        continue

"""
Arduino receives satellite position through serial port in the format shown above, then it must check the difference 
between where its antenna is pointing (int stepperaz int stepperel) and move each stepper the correct amount of steps
"""
