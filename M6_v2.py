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

from lib import LCD_1inch28
#import buzzer_api
import adafruit_thermal_printer as printer_api
from tools import *
import settings


#----- GENERAL CONFIGURATION -----#

#Define DEBUG
try :
    if sys.argv[1]=="debug" :
        DEBUG=True
except IndexError :
    DEBUG=False

#Import Assets
pygame.mixer.init(48000, -16, 1, 4096)
notifs = [
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/1.mp3"),
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/2.mp3"),
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/3.mp3"),
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/4.mp3"),
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/5.mp3"),
    pygame.mixer.Sound("/home/pi/Desktop/M6/media/6.mp3")
]

#GPIO Config
#D.2.1 - Boite Mail
#buzzer_1 = buzzer_api.Buzzer(settings.GPIO_BUZZER_1)
#buzzer_1.start()
mail_btn = gpio.Button(settings.GPIO_INT_1)

#D.2.2 - Cookies

#D.2.3 - Streaming
range_led = 95
strip = rpi.PixelStrip(range_led,settings.GPIO_LEDSTRIP)
strip.begin()

#D.2.4 - Données Personnelles

#D.2.5 - Surveillance Numérique
camera_led = gpio.LED(settings.GPIO_LED_5)

#D.2.6 - Obsolescence programmée

#D.2.7 - Data Center
server_btn = gpio.Button(settings.GPIO_INT_7)
server_fan = gpio.OutputDevice(settings.GPIO_FAN_7)

#D.2.8 -  Terres Rares

#D.2.9 - IA



#----- BLOCK SPECIFIC CODE -----#

#D.2.1 - Boite Mail

def play_notif() :
    #buzzer_1.play(random.choice(settings.buzzer_notif_sounds))
    random.choice(notifs).play()

index_1 = 0

def update_1() :
    global index_1
    index_1+=1
    if index_1>settings.TIMING_NOTIF_1 :
        if mail_btn.is_pressed==False :
            if random.randrange(0,3)==False :
                play_notif()
        index_1=0

#D.2.2 - Cookies


#D.2.3 - Streaming

led_streaming = range(44,95) #leds used in D.2.3

possible_color = [
    rpi.Color(255,0,0),
    rpi.Color(0,255,0),
    rpi.Color(0,0,255),
]

def change_led_color() :
    color = random.choice(possible_color)
    for i,led in enumerate(led_streaming) :
        strip.setPixelColor(led,color)
    strip.show()

index_3 = 0

def update_3() :
    global index_3
    index_3+=1
    if index_3>settings.TIMING_LED_CHANGING_3 :
        change_led_color()
        index_3=0

#D.2.4 - Données Personnelles

#D.2.5 - Surveillance Numérique
index_5 = 0

def update_5() :
    global index_5
    index_5+=1
    if index_5>settings.TIMING_LED_BLINK_5 :
        camera_led.toggle()
        index_5=0

#D.2.6 - Obsolescence programmée
total_countdown = settings.TOTAL_COUNTDOWN_6
current_countdown = settings.TOTAL_COUNTDOWN_6
text_countdown = settings.TEXT_COUNTDOWN_6
current_text_countdown = settings.TEXT_COUNTDOWN_6

def get_countdown_as_string() : #Get time as showable string
    str_min = str(int(current_countdown/60))
    if len(str_min)==1 :
        str_min = "0" + str_min
    str_sec = str(current_countdown%60)
    if len(str_sec)==1 :
        str_sec = "0" + str_sec
    to_return = str_min+":"+str_sec
    return to_return

## WATCH
disp = LCD_1inch28.LCD_1inch28()
disp.Init() # Initialize library.
disp.clear() # Clear display.
font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",90) #Countdown font
txt_font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",30) #Text font

def write_time_on_watch() : #Show time on round display
    to_show=get_countdown_as_string()
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((25, 65), to_show, fill = (255,255,255),font=font)
    disp.ShowImage(img)

def write_txt_on_watch() :
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((35, 50), settings.txt_6[0], fill = (255,255,255),font=txt_font)
    draw.text((35, 70), settings.txt_6[1], fill = (255,255,255),font=txt_font)
    draw.text((20, 120),settings.txt_6[2], fill = (255,255,255),font=txt_font)
    draw.text((30, 140),settings.txt_6[3], fill = (255,255,255),font=txt_font)
    draw.text((80, 160),settings.txt_6[4], fill = (255,255,255),font=txt_font)
    disp.ShowImage(img)

## SMARTPHONE

class Smartphone(Thread) :
    def __init__(self,port="/dev/ttyACM0",baudrate=9600) :
        Thread.__init__(self)
        self.api=serial.Serial(port,baudrate,timeout=1)
        self.on=True
    def run(self) :
        while self.on :
            pass
    def send_msg(self,msg:str) :
        msg=msg+"#"
        self.api.write(bytes(msg,"utf-8"))

smart = Smartphone()

def write_on_smartphone(txt) :
    smart.send_msg(txt)

## TABLET
pygame.init()
tablet_screen = pygame.display.set_mode(settings.SCREEN_SIZE,pygame.FULLSCREEN)
pygame.font.init()
tablet_num_font=pygame.font.Font("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",300)
tablet_txt_font=pygame.font.Font("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",100)

def write_time_on_tablet() :
    to_blit = tablet_num_font.render(get_countdown_as_string(),1,pygame.Color("White"),pygame.Color("Black"))
    center_blit(tablet_screen,to_blit,(settings.SCREEN_SIZE[0]/2,settings.SCREEN_SIZE[1]/2))
    
def write_text_on_tablet() :
    for i,line in enumerate(settings.txt_6) :
        to_blit = tablet_txt_font.render(line,1,pygame.Color("White"),pygame.Color("Black"))
        center_blit(tablet_screen,to_blit,(settings.SCREEN_SIZE[0]/2,90+i*110))

index_6 = 0

def update_6() :
    global index_6
    global current_countdown
    global current_text_countdown
    index_6+=1
    if index_6>settings.FPS :
        if current_countdown>0 :
            current_countdown-=1
            write_time_on_watch()
            write_on_smartphone(get_countdown_as_string())
            write_time_on_tablet()
        else :
            tablet_screen.fill(pygame.Color("Black"))
            write_txt_on_watch()
            write_on_smartphone("MEH")
            write_text_on_tablet()
            current_text_countdown-=1
            if current_text_countdown==0 :
                current_text_countdown=text_countdown
                current_countdown = total_countdown
                tablet_screen.fill(pygame.Color("Black"))
        index_6=0

#D.2.7 - Data Center
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

def anim_server() :
    for server in led_server :
        for led in server :
            value = random.choice(possible_values)
            strip.setPixelColor(led,rpi.Color(value,value,value))

def handle_fan() :
    if server_btn.is_pressed :
        server_fan.off()
    else :
        server_fan.on()

index_7 = 0

def update_7() :
    global index_7
    index_7+=1
    handle_fan()
    if index_7>settings.TIMING_SERVER_ANIM_7 :
        anim_server()
        index_7=0

#D.2.8 -  Terres Rares

#D.2.9 - IA
class IA_printer() :
    def __init__(self) :
        self.serial = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
        self.printer_class = printer_api.get_printer_class(0)
        self.printer = self.printer_class(self.serial)
        self.index=0
        self.line_to_send = [
            {
                "txt" :"feed",
                "args":[1]
            },
            {
                "txt" :"Discussion 45 789",
                "args":["size_medium","justify_center"]
            },
            {
                "txt" :"feed",
                "args":[1]
            },
            {
                "txt" :"Operateur : Je te repose la",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"question, es-tu un outil",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"respectueux de l'environnement ?",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"feed",
                "args":[1]
            },
            {
                "txt" :"    IA : Non, je ne suis pas un",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    outil respectueux de",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    l'environnement au sens",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    strict. L'IA consomme de",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    l'energie pour fonctionner,",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    donc je ne peux pas etre",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"    considere comme \"ecologique\"",
                "args":["size_small","justify_left"]
            },
            {
                "txt" :"feed",
                "args":[1]
            },
            {
                "txt" :"Cout carbone : 458g",
                "args":["size_medium","justify_center"]
            },
            {
                "txt" :"feed",
                "args":[1]
            },
            {
                "txt" :"----------",
                "args":["size_medium","justify_center"]
            },
            
        ]
    def print_one_line(self) :
        self.index+=1
        if self.index==len(self.line_to_send) :
            self.index=0
        to_print = self.line_to_send[self.index]
        if to_print["txt"]=="feed" :
            self.printer.feed(to_print["args"][0])
        else :
            for arg in to_print["args"] :
                match arg :
                    case "size_small" :
                        self.printer.size = printer_api.SIZE_SMALL
                    case "size_medium" :
                        self.printer.size = printer_api.SIZE_MEDIUM
                    case "size_big" :
                        self.printer.size = printer_api.SIZE_BIG
                    case "justify_left" :
                        self.printer.justify = printer_api.JUSTIFY_LEFT
                    case "justify_center" :
                        self.printer.justify = printer_api.JUSTIFY_CENTER
                    case "justify_right" :
                        self.printer.justify = printer_api.JUSTIFY_RIGHT
                    case _ :
                        print(f"Unknown arg : {arg}")
            self.printer.print(to_print["txt"])

printer = IA_printer()

index_9 = 0

def update_9() :
    global index_9
    index_9+=1
    if index_9>settings.TIMING_PRINTER_9 :
        printer.print_one_line()
        index_9=0

#----- GENERAL LOOP -----#

on = True
CLOCK = pygame.time.Clock()

while on :

    #Event handling
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            on = False
        if keys[pygame.K_ESCAPE] : # ECHAP : Quitter
            on=False
    
    #D.2.1 - Boite Mail
    update_1()
    #D.2.2 - Cookies
    #D.2.3 - Streaming
    update_3()
    #D.2.4 - Données Personnelles
    #D.2.5 - Surveillance Numérique
    update_5()
    #D.2.6 - Obsolescence programmée
    #tablet_screen.fill(pygame.Color("Black"))
    
    #fps = str(round(CLOCK.get_fps(),1))
    #txt = "FPS : "+fps
    #to_blit=tablet_txt_font.render(txt,1,pygame.Color("White"),pygame.Color("Black"))
    #tablet_screen.blit(to_blit,(0,0))
    update_6()
    #D.2.7 - Data Center
    update_7()
    #D.2.8 -  Terres Rares
    #D.2.9 - IA
    update_9()

    #General
    pygame.display.flip()
    CLOCK.tick(settings.FPS)
    
buzzer_1.on=False
buzzer_1.join()

