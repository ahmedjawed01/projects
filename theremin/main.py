################################################################################
# Multithreaded Blinking Theremin - main.py
#
# Created by VIPER Team 2015 CC
# Authors: L.F. Cerfeda, L. Cominelli
################################################################################

import adc        # import the adc driver
import pwm        # import the pwm module
import helpers    # import the helpers module

# Define the pins where input sensors and output is attached to
pot_pin = A2          # Analog input from a potentiometer. Tested values range from 0 to about 4000
prox_pin = A5         # Analog Input from a proximity sensor. Tested values range from 250 to about 3800
buzzer = D7.PWM       # Use pin D7 of Arduino DUE or ST Nucleo F401RE as PWM. If you use Spark Core choose A4
led_green = D6
led_red = D8          # If you use Spark Core choose D7

# Set the LED pins as outputs
pinMode(led_red,OUTPUT)
pinMode(led_green,OUTPUT)

# Create a dictionary for storing values of the input variables to be used in the threads
input_val= {'prox_val':1, 'pot_val':1}

# Define an analog sensor sampling function that acquires the raw data and 
# normalizes it through the function map_range() definited in the helpers.py
# adc.read is the correct way to use adc in VIPER. It is similar at analogRead in Arduino Wiring, but sounds better
def sampling():
    global input_val
    while True:
        input_val['pot_val'] = helpers.map_range(adc.read(pot_pin),0,4000,1,1000)      
        input_val['prox_val'] = helpers.map_range(adc.read(prox_pin),300,3800,1,1000)
        sleep(50)

# Define the 'buzz' function
def buzz(input_for_period,input_for_length,buzzer_pin):
    while True:
        # Typical piezoelectric buzzer frequencies range from 500-4000Hz, so period has to range from 250 us to 2000 us
        period = helpers.map_range(input_val[input_for_period],1,1000,250,2000)
        # Set the period of the buzzer and the duty to 50% of the period through pwm.write
        # pwm.write is the correct way to use pwm in VIPER. It is similar at analogWrite in Arduino Wiring, but sounds better
        # Note that in pwm.write we will use MICROS so every sec is 1000000 micros
        # // is the int division, pwm.write period doesn't accept floats
        pwm.write(buzzer_pin,period,period//2,MICROS)
        # Set the length of the sleep to create a "beat" effect (from 1 to 300 ms). The default time unit of sleep function is MILLIS
        length = helpers.map_range(input_val[input_for_length],1,1000,1,300)
        sleep(length)
        
# Define the 'blink' function
def blink(input_for_delay,led_pin):
    while True:
        # Set the delay from 1 to 500 ms
        delay = helpers.map_range(input_val[input_for_delay],1,1000,1,500) 
        digitalWrite(led_pin,HIGH)      # turn the LED ON by making the voltage HIGH
        sleep(delay)                    # wait for 'delay' ms
        digitalWrite(led_pin,LOW)       # turn the LED OFF by making the voltage LOW
        sleep(delay)                    # wait for 'delay' ms

# Create the threads that execute instances of the functions with different parameters 
thread(sampling)
thread(buzz,'prox_val','pot_val',buzzer)
thread(blink,'prox_val',led_red)
thread(blink,'pot_val',led_green)