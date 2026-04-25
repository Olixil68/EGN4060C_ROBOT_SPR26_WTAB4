#######################################################
# Thermal camera Plotter with AMG8833 Infrared Array
#
# by Joshua Hrisko
#    Copyright 2021 | Maker Portal LLC
#
#######################################################
#
import time,sys
sys.path.append('../')
# load AMG8833 module
import amg8833_i2c
import numpy as np
#
#####################################
# Initialization of Sensor
#####################################
#
t0 = time.time()
sensor = []
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
#
#####################################
# Start and Format Figure 
#####################################
#
pix_res = (8,8) # pixel resolution
zz = np.zeros(pix_res) # set array with zeros first
#
#####################################
# Plot AMG8833 temps in real-time
#####################################
#
pix_to_read = 64 # read all 64 pixels
while True:
    status,pixels = sensor.read_temp(pix_to_read) # read pixels with status
    if status: # if error in pixel, re-enter loop and try again
        continue
    
    T_thermistor = sensor.read_thermistor() # read thermistor temp
    cam_res = np.reshape(pixels,pix_res) # update grid with new temp
    print(cam_res)
    time.sleep(2)
    print("Thermistor Temperature: {0:2.2f}".format(T_thermistor)) # print thermistor temp
    