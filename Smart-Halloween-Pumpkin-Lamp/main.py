################################################################################
# Smart Halloween Pumpkin Lamp
#
# Created by VIPER Team 2015 CC
# Author: L. Rizzello
################################################################################
 
import streams
import rtttl
import threading
# import toishield module
from drivers.toishield import toishield
# import neopixel module
from drivers.neopixel import ledstrips as neo
 
streams.serial()
 
# set detection enabled and pumpkin inactive by default
toishield.microphone.detectionEnabled = True
toishield.microphone.activePumpkin = False
# set some variable for sound detection
toishield.microphone.staticMin = 4096
toishield.microphone.staticMax = -4096
toishield.microphone.resetMinMaxCounter = 0
 
# declare leds to blink! (http://doc.viperize.it/0.2.0.0007/ex_Neopixel_LED_Strips.html)
leds = neo.ledstrip(toishield.led_pin, 16)
leds.setall(0,0,0)
leds.on()
 
# semaphore initialized to 0 -> red: if a thread tries to acquire the semaphore
# it blocks if the semaphore has not been turned 'green' (released)
semaphore = threading.Semaphore(0)
 
# define a RTTTL Halloween melody to be played by passing it the RTTTL string.
# find more songs at http://ez4mobile.com/nokiatone/rtttf.htm and many other websites
hsong = rtttl.tune('Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#')
 
# If you use Particle Photon uncomment the following line and short-circuit the Buzzer and Aux2 pins
# toishield.buzzer_pin=D9.PWM
 
def blink():
    # blink while the pumpkin is active
    while toishield.microphone.activePumpkin:
        leds.setall(255,0,0)
        leds.on()
        sleep(500)
        leds.setall(255,140,0)
        leds.on()
        sleep(500)
    leds.setall(0,0,0)
    leds.on()
    semaphore.release()

def playHalloween():
    # plays halloween song two times, then disables pumpkin, but also waits
    # at the semaphore to synchronize with blinking thread
    for i in range(2):
        hsong.play(toishield.buzzer_pin)
    toishield.microphone.activePumpkin = False
    semaphore.acquire()
    sleep(1000)
    print("enabled again")
    toishield.microphone.detectionEnabled = True

def scare():
    # this is called when the sound exceeds the threshold, waits one second
    # and starts scaring!
    sleep(1000)
    thread(playHalloween)
    thread(blink)

# define a function that takes a sensor object as parameter and checks the
# maximum peak to peak extension of the signal in a preset window
# look at this (http://doc.viperize.it/0.2.0.0007/ex_Microphone_Peak_Detector.html)
# example for details on how the sound detector works
def detectSound(obj):
    if (obj.resetMinMaxCounter == obj._observationWindowN):
        extension = obj.staticMax - obj.staticMin
        if (extension > 1000):
            if obj.detectionEnabled:
                obj.detectionEnabled = False
                obj.activePumpkin = True
                thread(scare)
        obj.staticMax, obj.staticMin = -4096, 4096
        obj.resetMinMaxCounter = 0
    else:
        c = obj.currentSample()
        if (c > obj.staticMax):
            obj.staticMax = c
        elif (c < obj.staticMin):
            obj.staticMin = c
        obj.resetMinMaxCounter += 1

# set 'detectSound' as the function to be applied to the object at every sampling step    
toishield.microphone.doEverySample(detectSound)
# start sampling at 1 millisecond (1 kHZ) with a window length of 50 so that
# the lowest detectable frequency is 20 Hz
toishield.microphone.startSampling(1,50,"raw")
