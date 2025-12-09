import rpi_ws281x as rpi
import time

range_led = 10
frame = 0.2

strip = rpi.PixelStrip(range_led,10)

strip.begin()

while True :
    for i in range(0,range_led) :
        for j in range(0,range_led) :
            strip.setPixelColor(j,rpi.Color(0,0,0))
        strip.setPixelColor(i-2,rpi.Color(255,0,0))
        strip.setPixelColor(i-1,rpi.Color(0,255,0))
        strip.setPixelColor(i,rpi.Color(0,0,255))
        strip.setPixelColor(i+1,rpi.Color(255,255,255))
        #strip.setPixelColor(i+2,rpi.Color(150,150,150))
        strip.show()
        time.sleep(frame)
    for i in range(0,range_led) :
        for j in range(0,range_led) :
            strip.setPixelColor(range_led-j,rpi.Color(0,0,0))
        strip.setPixelColor(range_led-i-2,rpi.Color(255,0,0))
        strip.setPixelColor(range_led-i-1,rpi.Color(0,255,0))
        strip.setPixelColor(range_led-i,rpi.Color(0,0,255))
        strip.setPixelColor(range_led-i+1,rpi.Color(255,255,255))
        #strip.setPixelColor(range_led-i+2,rpi.Color(150,150,150))
        strip.show()
        time.sleep(frame)
    print("done")