# -*- coding: utf-8 -*-

# import grovepi
import time
import math
import sys
from grove.adc import ADC
from grove.i2c import Bus
import csv
from datetime import datetime

'''
## License

The MIT License (MIT)

Grove 8 channels 12 bit ADC Hat for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
ADC_DEFAULT_IIC_ADDR = 0X04

ADC_CHAN_NUM = 8

REG_RAW_DATA_START = 0X10
REG_VOL_START = 0X20
REG_RTO_START = 0X30

REG_SET_ADDR = 0XC0


class Pi_hat_adc():
    def __init__(self,bus_num=1,addr=ADC_DEFAULT_IIC_ADDR):
        self.bus=Bus(bus_num)
        self.addr=addr

    
    #get all raw adc data,THe max value is 4095,cause it is 12 Bit ADC
    def get_all_adc_raw_data(self):
        array = []
        for i in range(ADC_CHAN_NUM):  
            data=self.bus.read_i2c_block_data(self.addr,REG_RAW_DATA_START+i,2)
            val=data[1]<<8|data[0]
            array.append(val)
        return array
    
    def get_nchan_adc_raw_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,REG_RAW_DATA_START+n,2)
        val =data[1]<<8|data[0]
        return val
    #get all data with unit mv.
    def get_all_vol_milli_data(self):
        array = []
        for i in range(ADC_CHAN_NUM):  
            data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+i,2)
            val=data[1]<<8|data[0]
            array.append(val)
        return array
    
    def get_nchan_vol_milli_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
        val =data[1]<<8|data[0]
        return val

    #get all data ratio,unit is 0.1%
    def get_all_ratio_0_1_data(self):
        array = []
        for i in range(ADC_CHAN_NUM):  
            data=self.bus.read_i2c_block_data(self.addr,REG_RTO_START+i,2)
            val=data[1]<<8|data[0]
            array.append(val)
        return array
    
    def get_nchan_ratio_0_1_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,REG_RTO_START+n,2)
        val =data[1]<<8|data[0]
        return val

AADC = Pi_hat_adc()

def frank():
    raw_data=AADC.get_all_adc_raw_data()
    vol_data=AADC.get_all_vol_milli_data()
    ratio_data=AADC.get_all_ratio_0_1_data()
    print("raw data for each channel:(1-8chan)(12 bit-max=4096):")
    print(raw_data)
    print("voltage for each channel:(unit:mv,max=3300mv):")
    print(vol_data)
    print ("ratio for each channel(unit 0.1%,max=100.0%):")
    print(ratio_data)

    print(" ")
    print("NOTICE!!!:")
    print("The default setting of ADC PIN is floating_input.")
    print(" ")

# this function reads the peak value of an analog pin 
# time_window specifies for how long the function reads data
def getPeakValue(time_window, analog_port):
    global adc
    current_time = time.time()

    peak_value = 0
    while time.time() - current_time <= time_window:
        # new_value = grovepi.analogRead(analog_port)
        new_value = adc.read(analog_port)
        if new_value > peak_value:
            peak_value = new_value

        time.sleep(0.001)

    return peak_value

# this function calculates the peak current value
def getAmplitude(analog_port):
    grove_vcc = 3.3
    read_period = 1
    sensor_value = getPeakValue(read_period, analog_port)

    print 'sensor value = ' , sensor_value

    # taken from the datasheet
    # the lowest effective current it can read is 6mA -> 1.3Wh at 220 VAC 
    amplitude_current = float(sensor_value) / 1024 * grove_vcc / 800 * 2000000 # taken from the datasheet
    
    return amplitude_current

# calculates the effective current we're interested in
def getEffectiveCurrent(analog_port):
    current_amplitude = getAmplitude(analog_port)

    effective_current = current_amplitude / math.sqrt(2)

    print("The amplitude of the current = {} mA".format(current_amplitude))

    return effective_current

analog_port = 2 # connected to analog port A2
adc = ADC()

try:
    with open('report.csv', mode='w') as file:
        fieldnames = ['Timestamp', 'Value']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            #minimum_current = 1 / 1024 * grove_vcc / 800 * 2000000 / 1.414 = 5.696(mA)
            # Only for sinusoidal alternating current
            now = datetime.now()
            effective_current = getEffectiveCurrent(analog_port)
            writer.writerow({'Timestamp': now.strftime("%Y-%m-%d %H:%M:%S"), 'Value': effective_current })
            print("effective current = {} mA".format(effective_current))

            # frank()
            # time.sleep(1)

# in case the user ends the program by pressing CTRL-C        
except KeyboardInterrupt:
    sys.exit(0)

# in case there's an error while communicating with the GrovePi    
except IOError:
    print('[IO Error]')
    sys.exit(0)