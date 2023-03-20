import machine
from machine import Pin
from time import sleep
import time

pulse = 0
bbb=0
#pin = machine.Pin(0)
p0 = Pin(16, Pin.IN)

def callbackdown(p):
    global pulse,bbb

    aaa= time.ticks_ms()
    if aaa-bbb>200:
        pulse = pulse+1
        print('pin change down', p,pulse,aaa)
        bbb =aaa
  #  print("_",pulse)
    


p0.irq(trigger=Pin.IRQ_FALLING, handler=callbackdown)
while(ss):
    
    ww=1
    