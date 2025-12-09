
#CONSTANTS
FPS = 30
DIR="/home/pi/Desktop/"
SCREEN_SIZE=(1024, 600)

#GAMEPLAY
TIMING_NOTIF_1 = FPS/3
TIMING_LED_CHANGING_3 = FPS/3
TIMING_LED_BLINK_5 = FPS/5

TIMING_SERVER_ANIM_7 = FPS/2

TOTAL_COUNTDOWN_6 = 10
TEXT_COUNTDOWN_6 = 20
txt_6 = [
    "Votre appareil",
    "est trop vieux.",
    "Jetez-le et allez",
    "en acheter un",
    "autre"
]



#GPIOS
GPIO_LEDSTRIP = 21 #GPIO21, BOARD40
#D.2.1 - Boite Mail
GPIO_BUZZER_1 = 13 #"BOARD33" #GPIO13
#D.2.2 - Cookies

#D.2.3 - Streaming

#D.2.4 - Données Personnelles

#D.2.5 - Surveillance Numérique
GPIO_LED_5 = 6 #"BOARD31" #GPIO6

#D.2.6 - Obsolescence programmée

#D.2.7 - Data Center
GPIO_INT_7 = 19 #"BOARD35" #GPIO19
GPIO_FAN_7 = 26 #"BOARD37" #GPIO26

#D.2.8 - Terres Rares

#D.2.9 - IA


#----- DATA -----#

buzzer_notif_sounds = [
    [
        {"note":"D4","time":1},
        {"note":"A6","time":1}
    ],
    [
        {"note":"E4","time":1},
        {"note":"D5","time":1},
        {"note":"D6","time":1}
    ],
    [
        {"note":"A4","time":1},
        {"note":"D6","time":1}
    ],
    [
        {"note":"D4","time":1},
        {"note":"A6","time":1},
        {"note":"D5","time":1}
    ],
    [
        {"note":"A6","time":1},
        {"note":"D4","time":1}
    ],
    [
        {"note":"D6","time":1},
        {"note":"D5","time":1},
        {"note":"E4","time":1}
    ],
    [
        {"note":"D6","time":1},
        {"note":"A4","time":1}
    ],
    [
        {"note":"A6","time":1},
        {"note":"D4","time":1},
        {"note":"D5","time":1}
    ]
]




#NAMES
#D.2.1 - Boite Mail
#D.2.2 - Cookies
#D.2.3 - Streaming
#D.2.4 - Données Personnelles
#D.2.5 - Surveillance Numérique
#D.2.6 - Obsolescence programmée
#D.2.7 - Data Center
#D.2.8 - Terres Rares
#D.2.9 - IA




