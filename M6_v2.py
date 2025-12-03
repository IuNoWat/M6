import sys
import random
import time
from threading import Thread

import spidev as SPI
from PIL import Image,ImageDraw,ImageFont
import pygame
import gpiozero as gpio
import rpi_ws281x as rpi
import serial

#from lib import LCD_1inch28
#import buzzer_zero as buzzer

#CONSTANTS
FPS = 30
DIR="/home/pi/Desktop/"
#Define DEBUG
try :
    if sys.argv[1]=="debug" :
        DEBUG=True
except IndexError :
    DEBUG=False



gpio_btn_server = "BOARD35"
btn_server = gpio.Button(gpio_btn_server)

fan = gpio.OutputDevice("BOARD37")

gpio_led_camera = "BOARD33"
camera_led = gpio.LED(gpio_led_camera)
counter_camera = 0

#LEDSTRIP HANDLER
range_led = 95
strip = rpi.PixelStrip(range_led,10)
strip.begin()

led_server = [
    [1,2,3],
    [10,11,12],
    [20,21,22],
    [29,30,31],
    [39,40,41]
]

possible_values = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    5,
    10
]

led_streaming = range(44,95)

possible_color = [
    #rpi.Color(0,0,0),
    rpi.Color(255,0,0),
    rpi.Color(0,255,0),
    rpi.Color(0,0,255),
    #rpi.Color(255,255,0),
    #rpi.Color(255,0,255),
    #rpi.Color(0,255,255),
    #rpi.Color(255,255,255)
]

index_anim_streaming = 0

def anim_streaming() :
    global index_anim_streaming
    color = random.choice(possible_color)
    for i,led in enumerate(led_streaming) :
        strip.setPixelColor(led,color)
    strip.show()

def anim_server() :
    for server in led_server :
        for led in server :
            value = random.choice(possible_values)
            strip.setPixelColor(led,rpi.Color(value,value,value))

while True :
    anim_streaming()
    anim_server()

    if btn_server.is_pressed :
        fan.off()
    else :
        fan.on()
    
    counter_camera+=1
    if counter_camera>5 :
        camera_led.toggle()
        counter_camera=0

    time.sleep(0.1)



