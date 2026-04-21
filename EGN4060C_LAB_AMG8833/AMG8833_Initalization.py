# Code derived from Joshua Hrisko's code for the AMG8833 on Maker Portal
import time
import sys
sys.path.append('../') # Appends a directory to find local files
# load AMG8833 module from directory
import amg8833_i2c # Local file
import numpy as np

class Thermal_Camera():
    def __init__(self, sensor):
        self.sensor = []

    # Initialization of Sensor
    def Thermal_Init():
        t0 = time.time()
        while (time.time()-t0)<1: # wait 1sec for sensor to start
            try:
                # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
                sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
            except:
                sensor = amg8833_i2c.AMG8833(addr=0x68)
            finally:
                pass
        time.sleep(0.1) # wait for sensor to settle

        # If no device is found, exit the script
        if sensor==[]:
            print("No AMG8833 Found - Check Your Wiring")
            sys.exit(); # exit the app if AMG88xx is not found 

    # Function to read AMG8833 data
    def Thermal_Read(self):
        pix_res = (8,8) # pixel resolution
        zz = np.zeros(pix_res) # set array with zeros first
        pix_to_read = 64 # read all 64 pixels
        while True:
            status,pixels = self.sensor.read_temp(pix_to_read) # read pixels with status
            if status: # if error in pixel, re-enter loop and try again
                continue
    
            # T_thermistor = sensor.read_thermistor() # read thermistor temp
            reshaped_arr = np.reshape(pixels, pix_res)
            # print("Thermistor Temperature: {0:2.2f}".format(T_thermistor)) # print thermistor temp
            return reshaped_arr
    