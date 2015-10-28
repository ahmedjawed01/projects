################################################################################
# Smart Halloween Pumpkin Lamp
#
# Created: 2015-10-10 16:39:58.483065
#
################################################################################
 
import streams
from drivers.neopixel import ledstrips as neo
import rtttl
from drivers.toishield import toishield
import threading
 
 
def blink():
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
    sleep(1000)
    thread(playHalloween)
    thread(blink)
 
 
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
 
 
streams.serial()
 
# semaphore initialized to 0 -> red: if a thread tries to acquire the semaphore
# it blocks if the semaphore has not been turned 'green' (released)
semaphore = threading.Semaphore(0)
toishield.microphone.detectionEnabled = True
toishield.microphone.activePumpkin = False
hsong = rtttl.tune('Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#')
toishield.microphone.staticMin = 4096
toishield.microphone.staticMax = -4096
toishield.microphone.resetMinMaxCounter = 0
 
leds = neo.ledstrip(toishield.led_pin, 16)
leds.setall(0,0,0)
leds.on()
toishield.microphone.doEverySample(detectSound)
# 20Hz-1kHz
toishield.microphone.startSampling(1,50,"raw")
