################################################################################
# VIPER IoT Notes Printer
#
# Created by VIPER Team 2015 CC
# Authors: G. Baldi, D. Mazzei
################################################################################

# import everything needed
import streams
from drivers.thermalprinter import thermalprinter
from wireless import wifi
from drivers.wifi.cc3000 import cc3000_tiny as cc3000
# and also import the viperapp module
from libs.apps import viperapp
p = thermalprinter.ThermalPrinter(SERIAL1,19200)

s=streams.serial()

# save the template.html in the board flash with new_resource
new_resource("template.html")

# connect to a wifi network
try:
    cc3000.auto_init()

    print("Establishing Link...")
    wifi.link("SSID_WiFi",wifi.WIFI_WPA2,"PWD_WiFi")
    print("Ok!")        
except Exception as e:
    print(e)

def printMessage(msg):
    p.print_text("VIPER\n",justification="c", style="b")
    p.print_text("www.viperize.it\n\n",justification="c", style="b")
    p.print_text("Take me!\n",justification="c", style="b")
    p.print_text(msg)
    p.print_text("\n"*2+"*"*20+"\n"*3,justification="c")    
    
#### ViperApp Setup    
    
# :: Javascript to Python ::
# the following function will be called when the template button is pressed
def show_message(msg):
    print(msg)
    printMessage(msg)

# configure the viper app with a name, a descripton and the template url
vp = viperapp.ViperApp("Viper IoT Notes Printer","Print your message!","resource://template.html")

# everytime Javascript generates the event "showmsg" the function show_message is called
vp.on("showmsg",show_message)

# run the ViperApp!
vp.run()
# since vp.run starts a new thread, you can do whatever else you want down here!

