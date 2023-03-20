# Complete project details at https://RandomNerdTutorials.com
import network
import machine
from time import sleep
from machine import Pin, I2C
import dht
#import dht
#import ftplib2
import onewire
import ntptime
import time
import os
import ds18x20
#from urllib.urequest import urlopen
import BME280
import utime
import urequests

bbb =0
ccc =0

p0 = Pin(16, Pin.IN)
pulse =0
i2c = I2C(scl=Pin(2), sda=Pin(15), freq=10000)
p2 = Pin(12, Pin.IN)
HTTP_HEADERS = {'Content-Type': 'application/json'} 

#from ftpadvanced import AdvancedFTP
#from ftpupload import upload




from umqtt.simple import MQTTClient
try:
    import usocket as socket
except:
    import socket
import ussl as ssl



#sensor = dht.DHT22(Pin(14))
#sensor = dht.DHT11(Pin(14))

def getDHT():
    sensor = dht.DHT11(machine.Pin(4))
    try:
            
        sensor.measure()
        temp2 = sensor.temperature()
        hum2 = sensor.humidity()
        print (temp2,hum2)
            
    except:
        temp2 = 40
        hum2 =0
        print("Failed to read temperature or humidity")
    return temp2,hum2

def webSpeakLoad(field,temp):
    
    
  #  try:    
        print("sending  webaddress")
        xaddress ="https://api.thingspeak.com/update?api_key=SKKMTPV6WBE3ULID&field"+str(field)+"=" + str(temp)
        print (xaddress)
        request = urequests.post( xaddress )
        request.close() 
    
   # except:
      #  print("sending  webaddress failed")
        


def startlan():
     
     sta_if = network.WLAN(network.STA_IF)
     if sta_if.isconnected():
         print('WLAN already connected')
     else:
         print("No  WLAN try again")
         sta_if.active(True)
         try:
             sta_if.connect("Tenda", "borrisbig")
         except:
             print("failed first attempt")
         sleep(5)
         if sta_if.isconnected():
             print('WLAN connection succeeded! Tenda')
         else:
             print('No  WLAN connection Tenda_____ failed!')
            
             sta_if.connect("ImagineLTE_31AB7A", "18000244")
             sleep(5)
             sta_if.connect("ImagineLTE_31AB7A", "18000244")
             sleep(5)
                 
             if sta_if.isconnected():
                print('WLAN connection succeeded! Imagine')
             else:
                sta_if.connect("Tenda", "borrisbig")
                if sta_if.isconnected():
                     print('WLAN connection succeeded! Tenda')
                else:
                     sta_if.connect("Tenda02", "borrisbig")
                        if sta_if.isconnected():
                             print('WLAN connection succeeded! Tenda02')
                        else:
                             sleep(5)
                             sta_if.connect("Tenda02", "borrisbig")
                             if sta_if.isconnected():
                                 print('WLAN connection succeeded! Tenda02')
                             else:
                                 print('No  WLAN connection Tenda02_____ failed!')
                         
def gettemp():
      temp = 40
      ds_pin = machine.Pin(2)
      ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
      print (ds_sensor)
      roms = ds_sensor.scan()
      print(roms)
      
      try:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        for rom in roms:
            print(rom)
            temp = ds_sensor.read_temp(rom)
            print(temp)
            print('Temperature: %3.1f C' %temp)
          
      except OSError as e:
        print('Failed to read sensor.')
      return temp

def sendFTP(fname):    
    PORT = 21
    print("Sarting FTP")
    
    ftp = AdvancedFTP('192.168.15.184', PORT)
    ftp.login('megan', 'Shania01')
    print (ftp)
    
    ftp.cwd("GreenHouse")
    upload(ftp, fname, blocksize=2048)
    ftp.close
    print ("File uploaded")
  #  file = open(fname,'rb')                  # file to send
  #  session.storbinary('fname', file)     # send the file
  #  file.close()                                    # close file and FTP
  #  session.quit()
  #  print (fname & " file sent")
    
def NTPtime():
    ntptime.settime()
    rtc = machine.RTC()
    #utc_shift = 3

    tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc.datetime(tm)
    print (tm)
    
def deep_sleep(msecs):
    #configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
    print(msecs)
    
    rtc.alarm(rtc.ALARM0, msecs)
    #put the device to sleep
    machine.deepsleep()
def sendThingSpeak(temp):
    THINGSPEAK_POST_TEMPLATE = """
POST /update HTTP/1.1
Host: api.thingspeak.com
Connection: close
X-THINGSPEAKAPIKEY: %s
Content-Type: application/x-www-form-urlencoded
Content-Length: %d
%s
"""
    try:
    
        API_THINGSPEAK_HOST = 'api.thingspeak.com'
        API_THINGSPEAK_PORT = 443
        #THINGSPEAK_WRITE_KEY = 'FYI0TA6HIRMSOS71' # put your key here
        THINGSPEAK_WRITE_KEY = 'FYI0TA6HIRMSOS71' # put your key here        
        print('send data to ThingSpeak')
        s = socket.socket()
        ai = socket.getaddrinfo(API_THINGSPEAK_HOST, API_THINGSPEAK_PORT)
        addr = ai[0][-1]
        s.connect(addr)
        s = ssl.wrap_socket(s)
        data = 'field1=%.2f' % (temp)

        
        http_data = THINGSPEAK_POST_TEMPLATE % (THINGSPEAK_WRITE_KEY, len(data), data)
        print(http_data)
        
        s.write(http_data.encode())
        s.close()
        
    except:
        print("Failed socket")
def increase_pulse(Pin):           #defining interrupt connect to rain guage
    global pulse,bbb
    aaa= time.ticks_ms()
    if aaa-bbb>200:
      pulse=pulse +1
      print("Rain  ", pulse)
      bbb=aaa
      
def manual_load(Pin2):		#defining interrupt connect to manually load data
    global ccc,BME280
    ccc= time.ticks_ms()
    if aaa-ccc>200:
        startlan()
        temp = bme.temperature
        hum=bme.humidity
        press=bme.pressure
        rain = pulse/pulsetomm
        daypulse=daypulse+pulse
     #   webSpeakLoad(1,temp)
        sleep(2)
        webSpeakLoad(2,hum)
        sleep(2)
        webSpeakLoad(3,press)
        sleep(10)
        webSpeakLoad(4,rain)
        ccc= aaa

def main():
    global pulse
    pulse =0
    c=0
    pulsetomm = 2
    daypulse=0
    i = True
    try :
        startlan()
    except:
        print("Faild to connect to WLAN_1")
    try :
        startlan()
    except:
        print("Faild to connect to WLAN_2")
        
    try:
        NTPtime()
        print("Time update")
    except:
        print("time not updated")
    print(time.gmtime())
    while i:
        a= time.gmtime()
    
        b=a[4]
        if c != b:    
            print (a,b)
            c=b
        try:
            if b ==1 or b ==31:          
                startlan()
                for x in range(3):
                   sleep(1)
                   print(x)

                #a = True

                temp = bme.temperature
                hum= bme.humidity
                press= bme.pressure
                rain = pulse/pulsetomm
                daypulse=daypulse+pulse
                
                
                
                bme_readings = {'field1':temp, 'field2':hum, 'field3':press, 'field4':rain} 
                request = urequests.post( 'http://api.thingspeak.com/update?api_key=SKKMTPV6WBE3ULID', json = bme_readings, headers = HTTP_HEADERS )
                pulse = 0
                request.close() 
                print(bme_readings)
                
                
                
                
                pulse=0
            #    webSpeakLoad(1,temp)
            #    sleep(10)
            #    webSpeakLoad(2,hum)
            #    sleep(10)
            #    webSpeakLoad(3,press)
            #    sleep(10)
            #    webSpeakLoad(4,rain)
                
                c= a[3]
                sleep(65)
                if c==23:
                    e=daypulse/pulsetomm
                    webSpeakLoad(5,e)
                    e=0
                    try:
                        NTPtime()
                        print("Time has been updated")
                    except:
                        print("time has not been updated")
                NTPtime()
        except:
            print("Failed to connect to cloud")
            
#p2.irq(trigger=Pin.IRQ_FALLING, handler=manual_load)
p0.irq(trigger=Pin.IRQ_FALLING, handler=increase_pulse)
bme = BME280.BME280(i2c=i2c)
main()
