#!/usr/bin/python
#coding: utf-8

import time
import os
from threading import Thread

import gpiozero as gpio
from gpiozero.tones import Tone

#CONSTANTS
PIN=13 #BOARD33

#INIT
buzzer = gpio.TonalBuzzer(PIN,octaves=3)

#EXAMPLE MUSIC
#A music consists of a list of dict, each containing a note and a time multiplied by the interval defined in play_music()
#The " " key is silent
default_music=[
{"note":"D5","time":1},
{"note":"D5","time":1},
{"note":"D6","time":1},
{"note":" ","time":1},
{"note":"A5","time":1},
{"note":" ","time":1},
{"note":" ","time":1},
{"note":"G#5","time":1},
{"note":" ","time":1},
{"note":"G5","time":1},
{"note":" ","time":1},
{"note":"F5","time":1},
{"note":" ","time":1},
{"note":"D5","time":1},
{"note":"F5","time":1},
{"note":"G5","time":1}
]

def play_note(note,duree) : #To play a singular note for the duration of duree
    if note==" " :
        time.sleep(duree)
    else :
        buzzer.play(Tone(note))
        time.sleep(duree)
        buzzer.stop()

def play_music(music=default_music,base_interval=0.15) : #To play a music as described in DEFAULT_MUSIC
    for i,note in enumerate(music) :
        play_note(note["note"],base_interval*note["time"])

class Sound(Thread) :
    def __init__(self,sound,interval=0.15) :
        Thread.__init__(self)
        self.on=True
        self.sound=sound
        self.interval=interval
    def run(self) :
        play_music(self.sound,self.interval)

if __name__=="__main__" :
    play_music()

    #play_all_notes(0.1)

    #my_sound=Sound(default_music)
    #my_sound.start()
    #for i in range(0,10) :
    #    print(f"COUCOU {i}")
    #    time.sleep(0.5)
