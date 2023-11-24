from machine import Pin
import time
import select
import sys

# setup poll to read USB port
poll_object = select.poll()
poll_object.register(sys.stdin,1)

def turnOn(i):
    i = int(i)
    # i: led number (0,1,2)
    Pin(11, Pin.OUT).value((i)%3==0)
    Pin(12, Pin.OUT).value((i)%3==1)
    Pin(13, Pin.OUT).value((i)%3==2)
       
while True:
    # check usb input
    if poll_object.poll(0):
       #read as character
       ch = sys.stdin.read(1)
       turnOn(ch)
       #print (ch,"hello from the pico")
