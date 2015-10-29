################################################################################
# Viper Lamp 
#
# Created by VIPER Team 2015 CC
# Authors: G. Baldi, D. Mazzei
###############################################################################

#Lamp animation functions

from drivers.neopixel import ledstrips as neo
import threading

lock = threading.Lock()

# the Viper color :)
color = [0x54,0x9a,0x97]
anim = 0
anim_speed = 50
leds = None
layer0 = None
layer1 = None
layer2 = None
npins =0 
stopped=False
stopcolor = [0xff,0xff,0xff]

# create all the needed layers

# let's define some coefficients for smooth animation (half a sinus wave)
animation_coefficients = [
    0,
    0.2588190451,
    0.5,
    0.7071067812,
    0.8660254038,
    0.9659258263,
    1,
    0.9659258263,
    0.8660254038,
    0.7071067812,
    0.5,
    0.2588190451]

rainbow = [
    (0xff,0x00,0x00),
    (0xff,0x7f,0x00),
    (0xff,0xff,0x00),
    (0x00,0xff,0x00),
    (0x00,0x00,0xff),
    (0x4b,0x00,0x82),
    (0x8f,0x00,0xff)
]

def setup_anim(n):
    global layer0,layer1,layer2,anim

    # fill layers with their initial values
    lock.acquire()
    leds.clear()
    layer2.clear()
    layer0.clear()
    layer1.clear()
    n=n%4
    if n==0:
        layer0[0]=(100,0,0)
        layer0[1]=(100,0,0)
        layer0[2]=(100,0,0)
        layer1[0]=(0,100,0)
        layer1[1]=(0,100,0)
        layer1[2]=(0,100,0)    
    elif n==1:
        for x in range(npins//2):
            layer0[x]=(100//(2*x+1),0,0)
            layer1[npins-x-1]=(0,100//(2*x+1),0)
        layer2.clear()
    elif n==2:
        layer1.clear()
        pstep=0
        for x in range(npins):
            step = x*len(rainbow)/npins
            rx = (rainbow[int(step)][0]+rainbow[int(pstep)][0])//4
            gx = (rainbow[int(step)][1]+rainbow[int(pstep)][1])//4
            bx = (rainbow[int(step)][2]+rainbow[int(pstep)][2])//4
            layer0[x]=(rx,gx,bx)
            pstep=step
    elif n==3:
        layer0.clear()
        layer1.clear()
    anim=n
    lock.release()
    
def setup_anim_speed(n):
    global anim_speed
    anim_speed=n
    
def setup_color(r,g,b):
    global color
    #print("Color:",r,g,b)
    color[0]=r
    color[1]=g
    color[2]=b

# Create a function to handle background animation
def animate_background(delay):
    global color
    step=0
    while True:
        if (anim==3 or anim==0) and not stopped:
            lock.acquire()
            layer2.setall(int(color[0]*animation_coefficients[step]/2),int(color[1]*animation_coefficients[step]/2),int(color[2]*animation_coefficients[step]/2))
            lock.release()
            step += 1
            if step >= len(animation_coefficients):
                step=0
        else:
            lock.acquire()
            layer2.clear();
            layer2.setall(stopcolor[0],stopcolor[1],stopcolor[2])
            lock.release()
        sleep(delay+500-5*anim_speed)

def animate_foreground(delay):
    while True:
        if not stopped:
            lock.acquire()
            if anim == 0:
                layer0.lshift()
                layer1.rshift()
            elif anim == 1:
                layer0.rshift()
                layer1.rshift()
            elif anim == 2:
                layer0.rshift()
                layer1.rshift()
            elif anim == 3:
                layer0.lshift()
                layer1.lshift()
            lock.release()
        else:
            lock.acquire()
            layer0.clear()
            layer1.clear()
            lock.release()
        sleep(delay+100-anim_speed)

def start(pin,numpins):
    global leds,layer0,layer1,layer2,npins
    npins=numpins
    leds = neo.ledstrip(pin,numpins)
    layer0 = neo.ledstrip(pin,numpins)
    layer1 = neo.ledstrip(pin,numpins)
    layer2 = neo.ledstrip(pin,numpins)
    setup_anim(0)
    setup_anim_speed(50)
    
    # start the background animation thread
    thread(animate_background,500)
    
    # start the foreground animation thread
    thread(animate_foreground,50)
    while True:
        # clear leds
        leds.clear()
        # now, acquire the lock
        lock.acquire()
        # merge the first and second layer
        leds.merge(layer0)
        leds.merge(layer1)
        # merge the background layer only where leds is transparent (0,0,0) 
        leds.merge(layer2,neo.first_color)
        # release the lock
        lock.release()
        # and light it up!
        leds.on()
        sleep(50)

def stop(r,g,b):
    global stopped
    global stopcolor
    stopcolor[0]=r
    stopcolor[1]=g
    stopcolor[2]=b
    stopped=True
    
def resume():
    global stopped
    stopped = False
    setup_anim(anim)
