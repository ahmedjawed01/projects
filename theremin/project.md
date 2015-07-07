################################################################################
# Multithreaded Blinking Theremin - project.md
#
# Created by VIPER Team 2015 CC
# Authors: L.F. Cerfeda, L. Cominelli
################################################################################

The script is implemented using 4 threads that run in parallel. 
One thread is used for acquiring and normalize the analog signals acquired through 
a potentiometer and a IR proximity sensor. The other three threads are used to instantiate 
a generic blink() function that drives two LEDs at different frequencies and a generic buzz() function 
that drives a buzzer at different frequency e length of the sleep (to create a "beat" effect), 
calculated on the basis of the acquired analog signals.