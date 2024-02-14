from datetime import datetime
import RPi.GPIO as gpio


class Wheel:
    """Class to keep track of a wheel's rotation and calculate the speed"""

    def __init__(self, pin):
        print("init")
        self.HALLPIN = pin
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)
        gpio.setup(self.HALLPIN, gpio.IN)
        self._detect = False
        self._counter = 0
        self._times = [None, None]
        self.speed = 0

# Calculate the MPH given the time to complete one wheel rotation, in seconds
    def getMPH(self, rotation_time):
        rpm = 60 / rotation_time
        wheelCir = 1.701696  # GET REAL VALUE!!!
        wheelRevPerMile = 5280/wheelCir
        speedPerMin = rpm / wheelRevPerMile
        mph = speedPerMin * 60
        return mph

# Method to be called in the main loop to check for a magnet
    def checkStatus(self):
        if (gpio.input(self.HALLPIN) == False):
            if self._detect == False:
                self._detect = True
                if self._counter == 0:
                    self._times[0] = datetime.now()  # Log time when magnet is detected
                    print("detected")
                    self._counter += 1
                elif self._counter == 1:
                    # Log the second time the magnet is detected (thus a full loop of the wheel)
                    self._times[1] = datetime.now()
                    delta = self._times[1] - self._times[0]  # Calculate the difference in times
                    sec = delta.total_seconds()  # Amount of time for one rotation of the wheel
                    self.speed = "%.2f" % self.getMPH(sec)  # Truncates the decimals
                    self._counter -= 1
        else:
            if self._detect == True:
                self._detect = False
