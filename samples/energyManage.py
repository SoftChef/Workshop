#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from grove.adc import ADC
from controller import BpiController
from nodes import Buzzer

bpiController = BpiController()
bpiController.mqttConnect()
buzzer = Buzzer()
adc = ADC()

sensor = 2

# Vcc of the grove interface is normally 3.3v (Grove Base Hat)
grove_vcc = 3.3

# Function: Sample for 1000ms and get the maximum value from the SIG pin
def getPeak():
    global adc
    # store max value here
    max_value = 0
    current_time = time.time()

    while time.time() - current_time <= 3:
        new_value = adc.read(sensor)
        if new_value > max_value:
            max_value = new_value

        time.sleep(0.001)

    return max_value


total_power = 0
while True:
  try:
      # Get sensor value
      sensor_value = getPeak()
      # Calculate amplitude current (mA)
      amplitude_current = round((((sensor_value * grove_vcc)/ 1024) / 800) * 2000000, 3)

      # Calculate effective value (mA)
      effective_value = round(amplitude_current / 1.414, 3)

      # Calculate Power
      power_value = round((effective_value / 1000) * 110, 3)

      # Calculate total total_power
      total_power = total_power + power_value

      # Calculate Co2e
      # kgCo2e to gCo2e , hour to seconds , w to kw
      # (0.623 * 1000) / 3600000 (gCo2e/watt/second) = 0.00017
      gCo2e = total_power * 0.00017

      print "有效電流 : %s A" % (effective_value / 1000)
      print "消耗功率 : %s W" % (power_value)
      print "總用電功率 : %s W" % (total_power)
      print "排碳量: %s gCo2e" % (gCo2e)

      # 補充
      if gCo2e >= 0.5:
          errorMessage = '總排碳量超過(%s) gCo2e ' % (gCo2e)
          buzzer.on()
          time.sleep(1)
          buzzer.off()
      else:
          errorMessage = ''
          buzzer.off()

      if total_power > 1500:
          errorMessage2 = '總消耗功率超過(%s) W' % (total_power)
          buzzer.on()
          time.sleep(1)
          buzzer.off()
      else:
          errorMessage2 = ''
          buzzer.off()

      bpiController.shadowUpdate({
          'energyManagement': {
              'reportInterval': 3,
              'current': effective_value,
              'gCo2e': gCo2e,
              'total_power': total_power,
              'error': errorMessage + errorMessage2
          }
      })
      # Report to sensor.live History DDB
      bpiController.reportHistory({
          'energyManagement': {
              'current': effective_value,
              'gCo2e': gCo2e,
              'total_power': total_power
          }
      })


  except IOError:
      print ("Error")