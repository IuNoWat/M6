import sys
import random
import time

import spidev as SPI
from PIL import Image,ImageDraw,ImageFont
import pygame
import gpiozero as gpio
import rpi_ws281x as rpi

from lib import LCD_1inch28
import buzzer_zero as buzzer

#CONSTANTS
FPS = 30
DIR="/home/pi/Desktop/"
SCREEN_SIZE=(1600, 900)
FULLSCREEN=True
#Define DEBUG
try :
    if sys.argv[1]=="debug" :
        DEBUG=True
except IndexError :
    DEBUG=False

#M6.3
nb_led_gamer = 8

#DATA

#M6.6

txt_6 = [
    "Votre appareil",
    "est trop vieux.",
    "Jetez-le et allez",
    "en acheter un",
    "autre"
]

#GPIO

#Buttons
M6_1_BTN = "BOARD29"
M6_2_BTN = "BOARD11"
M6_3_BTN = "BOARD37"
M6_6_BTN = "BOARD18"
M6_7_BTN = "BOARD31"
M6_8_BTN = "BOARD27"
M6_9_BTN = "BOARD28"

#Others
M6_1_BUZZ = "BOARD33"
M6_2_LGT = "BOARD35"
M6_3_LEDS = 12 # BOARD32
M6_7_VENT ="BOARD36"
M6_8_LGT = "BOARD40"
M6_9_LGT ="BOARD38"

#M6.6
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0


#ENGINE

#General
current_frame=0

#Lights

class Light() :
    def __init__(self,btn_pin,mofset_pin) :
        self.btn_pin = btn_pin
        self.mofset_pin = mofset_pin
        self.btn = gpio.Button(btn_pin)
        self.lgt = gpio.OutputDevice(mofset_pin)
    def update(self) :
        if self.btn.is_pressed :
            self.lgt.off()
        else :
            self.lgt.on()

#M6.1
M6_1_buzzer = buzzer.Sound(buzzer.default_music)
M6_1_btn = gpio.Button(M6_1_BTN)
M6_1_btn.when_pressed = M6_1_buzzer.start


#M6.3
strip = rpi.PixelStrip(nb_led_gamer,M6_3_LEDS)
strip.begin()

LED_BLACK=rpi.Color(0,0,0)
LED_WHITE=rpi.Color(255,255,255)

frames = [
    [LED_WHITE,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_WHITE,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_WHITE,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_BLACK,LED_WHITE,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_WHITE,LED_BLACK,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_WHITE,LED_BLACK,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_WHITE,LED_BLACK],
    [LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_BLACK,LED_WHITE]
]

def show_led_frame(frame) :
    for i in range(0,nb_led_gamer) :
        strip.setPixelColor(i,LED_BLACK)
    for i,led in enumerate(frame) :
        strip.setPixelColor(i,led)
    strip.show()

current_led_frame = 0

def show_next_frame() :
    global current_led_frame
    show_led_frame(frames[current_led_frame])
    current_led_frame +=1
    if len(frames)<=current_led_frame :
        current_led_frame=0


#M6.6
total_time_6 = 5
current_time_6=total_time_6
text_timer_6=0
text_waiting_time_6 = 5
mode_6 = "COUNTDOWN"
# Launching round display
disp = LCD_1inch28.LCD_1inch28()
disp.Init() # Initialize library.
disp.clear() # Clear display.
#Countdown font
font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",80)
#Text font
txt_font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",30)

def get_time() : #Get time as showable string
    str_min = str(int(current_time_6/60))
    if len(str_min)==1 :
        str_min = "0" + str_min
    str_sec = str(current_time_6%60)
    if len(str_sec)==1 :
        str_sec = "0" + str_sec
    to_return = str_min+":"+str_sec
    return to_return

def show_time() : #Show time on round display
    to_show=get_time()
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((30, 60), to_show, fill = (255,255,255),font=font)
    disp.ShowImage(img)

def show_txt() : #Show text on round display
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((35, 50), txt_6[0], fill = (255,255,255),font=txt_font)
    draw.text((35, 70), txt_6[1], fill = (255,255,255),font=txt_font)
    draw.text((20, 120), txt_6[2], fill = (255,255,255),font=txt_font)
    draw.text((30, 140), txt_6[3], fill = (255,255,255),font=txt_font)
    draw.text((80, 160), txt_6[4], fill = (255,255,255),font=txt_font)
    disp.ShowImage(img)

def update_6() :
    global mode_6
    global current_time_6
    global text_timer_6
    if mode_6=="COUNTDOWN" :
        if current_frame%FPS==0 :
            if current_time_6==0 :
                disp.clear() # Clear display.
                show_txt()
                mode_6="TEXT"
                text_timer_6=0
            else :
                disp.clear() # Clear display.
                show_time()
                current_time_6-=1
    else :
        text_timer_6+=1
        if text_timer_6==text_waiting_time_6*FPS :
            mode_6="COUNTDOWN"
            current_time_6=total_time_6


#STYLE
WHITE=pygame.Color("White")
BLACK=pygame.Color("Black")
GREEN=pygame.Color("Green")
RED=pygame.Color("Red")
COLOR_BG=pygame.Color(0,0,0,255)
COLOR_HL=pygame.Color(255,255,255,255)
pygame.font.init()
debug_font=pygame.font.Font('freesansbold.ttf',16)


#PREPARE MAINLOOP

#General
on=True
SCREEN = pygame.display.set_mode(SCREEN_SIZE,pygame.FULLSCREEN)
CLOCK = pygame.time.Clock()

#Btns
M6_3_btn = gpio.Button(M6_3_BTN)

#Lights
LIGHTS = [
    Light(M6_2_BTN,M6_2_LGT),
    Light(M6_7_BTN,M6_7_VENT),
    Light(M6_8_BTN,M6_8_LGT),
    Light(M6_9_BTN,M6_9_LGT)
]

#MAINLOOP

while on :
    #Cleaning of Screen
    SCREEN.fill(COLOR_BG)

    #Event handling
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            on = False
        if keys[pygame.K_ESCAPE] : # ECHAP : Quitter
            on=False
    
    #CHECK LIGHTS
    for light in LIGHTS :
        light.update()
    
    #UPDATE M6_3
    if M6_3_btn.is_pressed==False :
        show_next_frame()

    #UPDATE M6_6
    update_6()

    #Show DEBUG
    if DEBUG :
        fps = str(round(CLOCK.get_fps(),1))
        txt = f"DEBUG MODE | FPS : {FPS} | current_frame : {current_frame}"
        to_blit=debug_font.render(txt,1,WHITE,COLOR_BG)
        SCREEN.blit(to_blit,(0,0))
        print("GENERAL GPIO STATUS")
        for light in LIGHTS :
            print(f"Button {light.btn_pin} : {light.btn.is_pressed}")
        


    #End of loop
    pygame.display.update()
    CLOCK.tick(FPS)
    current_frame+=1