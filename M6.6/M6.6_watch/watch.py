import time

import spidev as SPI
from PIL import Image,ImageDraw,ImageFont

from lib import LCD_1inch28

#CONSTANTS

total_time = 5
txt = [
    "Votre appareil",
    "est trop vieux.",
    "Jetez-le et allez",
    "en acheter un",
    "autre"
]

#GPIO
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0

#ENGINE
current_time = 0

#Launching LCD Device

disp = LCD_1inch28.LCD_1inch28()

disp.Init() # Initialize library.

disp.clear() # Clear display.

img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",80)

txt_font = ImageFont.truetype("/home/pi/Desktop/M6/M6.6/M6.6_watch/SourceSansPro.ttf",30)


draw.text((20, 60), 'Hello World', fill = (255,255,255),font=font)

disp.ShowImage(img)

time.sleep(5)

def get_time() :
    str_min = str(int(current_time/60))
    if len(str_min)==1 :
        str_min = "0" + str_min
    str_sec = str(current_time%60)
    if len(str_sec)==1 :
        str_sec = "0" + str_sec
    to_return = str_min+":"+str_sec
    return to_return

def show_time() :
    to_show=get_time()
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((30, 60), to_show, fill = (255,255,255),font=font)
    disp.ShowImage(img)

def show_txt() :
    img = Image.new("RGB", (disp.width, disp.height), "BLACK") # Create blank image for drawing.
    draw = ImageDraw.Draw(img)
    draw.text((35, 50), txt[0], fill = (255,255,255),font=txt_font)
    draw.text((35, 70), txt[1], fill = (255,255,255),font=txt_font)
    draw.text((20, 120), txt[2], fill = (255,255,255),font=txt_font)
    draw.text((30, 140), txt[3], fill = (255,255,255),font=txt_font)
    draw.text((80, 160), txt[4], fill = (255,255,255),font=txt_font)
    disp.ShowImage(img)


while True :
    disp.clear() # Clear display.
    show_time()
    print(current_time)
    time.sleep(1)
    current_time=current_time-1
    if current_time==0 :
        show_txt()
        time.sleep(5)
        current_time=total_time


disp.module_exit()