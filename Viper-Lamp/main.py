################################################################################
# Viper Lamp 
#
# Created by VIPER Team 2015 CC
# Authors: G. Baldi, D. Mazzei
###############################################################################

import streams
from libs.apps import viperapp
from drivers.wifi.bcm43362 import bcm43362 as bcm
from wireless import wifi
import animation
from drivers.toishield  import toishield

streams.serial()

bcm.auto_init()
for retry in range(10):
    try:
        print("Establishing link...")
        wifi.link("Wi-Fi_SSID", wifi.WIFI_WPA2, "Wi-Fi_PWD")
        print("OK")
        break
    except Exception as e:
        print(e)

if not wifi.linked:
    print("Can't establish link!")
    pinMode(LED0, OUTPUT)
    while True:
        pinToggle(LED0)
        sleep(500)

# save the template.html in the board flash with new_resource
new_resource("template.html")

#### ViperApp Setup

# :: Javascript to Python ::
# the following functions will be called when buttons are pressed
def change_color(r, g, b):
    animation.setup_color(r, g, b)

def change_animation(n):
    animation.setup_anim(n)

def change_speed(n):
    animation.setup_anim_speed(n)

# configure the viper app with a name, a descripton and the template url
vp = viperapp.ViperApp("Viper Lamp", "Try me!", "resource://template.html")

# everytime Javascript generates events the corresponding functions are called
vp.on("change_color", change_color)
vp.on("change_animation", change_animation)
vp.on("change_speed", change_speed)

# run the ViperApp!
vp.run()

# since vp.run starts a new thread, you can do whatever else you want down here!
# let's control leds

animation.start(D6, 24)
