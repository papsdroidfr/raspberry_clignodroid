#!/usr/bin/env python3
########################################################################
# Filename    : clignodroid_buton.py
# Description : Jeux de mémoire SIMON
# auther      : papsDroid
# modification: 2019/06/04
########################################################################

import RPi.GPIO as GPIO
import time, os

class Button_quit():
    def __init__(self, ap, powerOff=False):
        self.application=ap             # pour appel de la fonction ap.destroy()   
        self.powerOff = powerOff        # True: extinction du raspberry, False=Raspberry reste allumé
        self.buttonPin=40               # define the buttonPin
        self.on=False                   # etat off au début: bouton non appuyé
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set buttonPin's mode is input, and pull up to high level(3.3V)
        GPIO.add_event_detect(self.buttonPin,GPIO.FALLING,callback=self.buttonEvent, bouncetime=300)

    def buttonEvent(self,channel): #When the button is pressed, this function will be executed
        self.on = True
        print('button quit pressed, etat=', self.on)
        self.application.destroy()
        if self.powerOff:
           print('Extinction Raspberry...')
           os.system('sudo halt')
        raise SystemExit

    def setPowerOff(self, b=False):
        self.powerOff = b;


class Button_led():
    def __init__(self, rackleds, rackbuttons, buzz, pin, nom, id):
        self.rackleds = rackleds   
        self.rackbuttons = rackbuttons
        self.buzzer = buzz     
        self.buttonPin=pin     # define the buttonPin
        self.nom = nom         # nom du bouton
        self.id = id           # id du bouton
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set buttonPin's mode is input, and pull up to high level(3.3V)
        GPIO.add_event_detect(self.buttonPin,GPIO.FALLING,callback=self.buttonEvent, bouncetime=1000)
        
    #fonction exécutée quand le bouton est préssé
    def buttonEvent(self,channel): 
        print('button ', self.nom,' pressed')    
        self.rackbuttons.pressed=True
        self.rackbuttons.id_button_pressed = self.id
        if self.rackbuttons.ledsActivated:
            self.rackleds.leds[self.id].on()        # allume la led correspondante au bouton
            self.buzzer.buzzId(self.id)             # fait sonner le buzzer avec la fréquence correspondante à la led allumée
            time.sleep(0.5)
            self.rackleds.leds[self.id].off()       # led etteinte
            self.buzzer.mute()                      # arrête le son du buzzer
        else:
            time.sleep(0.5)
        self.rackbuttons.pressed=False

class RackButtons():
    def __init__(self, rackleds, buzz):
        self.rackleds = rackleds
        self.buzzer=buzz
        self.ledsActivated=True 
        self.buttons=[]
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin=12, nom='ledG', id=0))  # bouton LedG
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin=16, nom='ledB', id=1))  # bouton LedB
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin=18, nom='ledY', id=2))  # bouton LedY
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin=22, nom='ledR', id=3))  # bouton LedR
        self.id_button_pressed=0   # id du bouton préssé
        self.pressed=False         # par défaut aucun bouton n'a été préssé
     
    def activateLeds(self):
        self.ledsActivated=True
        
    def desactivateLeds(self):
        self.ledsActivated=False
