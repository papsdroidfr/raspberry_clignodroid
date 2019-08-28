#!/usr/bin/env python3
########################################################################
# Filename    : clignodroid_led.py
# Description : Jeux de mémoire SIMON
# auther      : papsDroid
# modification: 2019/06/04
########################################################################

import RPi.GPIO as GPIO
import time

class Led:
    def __init__(self, pin):
        self.pin = pin           # pin du GPIO qui commande la Leds.
        GPIO.setup(self.pin, GPIO.OUT)  # Set pins' mode is output
        
    def on(self):
        GPIO.output(self.pin, GPIO.HIGH) # led on
        
    def off(self):
        GPIO.output(self.pin, GPIO.LOW) # led off
    
    def clignote(self, n):
        for x in range(n):
            self.on()
            time.sleep(0.1)
            self.off()
            time.sleep(0.1)

class RackLeds:
    def __init__(self):
        self.leds = []   #liste des leds du rack
        self.leds.append(Led(pin=7))     # 1ère led (verte) sur le pin 7 
        self.leds.append(Led(pin=11))    # 2nd led (bleue)  sur le pin 11 
        self.leds.append(Led(pin=13))    # 3ème led (jaune) sur le pin 13
        self.leds.append(Led(pin=15))    # 4ème led (rouge) sur le pin 15
        self.off()                                 # leds toutes etteintes
        self.animation_demarrage()                 # animation de démarrage
        self.tp_led = 0.5                          # temps d'allumage des leds 
        
    def off(self):
        for l in self.leds:
            GPIO.output(l.pin, GPIO.LOW)    # toutes les leds off

    def on(self):
        for l in self.leds:
            GPIO.output(l.pin, GPIO.HIGH)   # toutes les leds on

    def wave(self): #allume les leds une par une dans un sens, puis dans l'autre
        for l in self.leds: #allumage des leds vers la droite
            l.on()
            time.sleep(0.1)
            l.off()
        for l in self.leds[::-1]: #allumage des leds vers la gauche
            l.on()
            time.sleep(0.1)
            l.off()

    def clignote(self): #fait clignoter toutes les leds toutes en même temps
        self.on()
        time.sleep(0.1)
        self.off()
        time.sleep(0.1)

    def animation_demarrage(self):
        for x in range(3):
            self.wave()
        for x in range(3):
            self.clignote()
            
    def gagne(self):
        self.leds[0].clignote(3)    #clignoter la led verte 3 fois
    
    def perdu(self):
        self.leds[3].clignote(3)    #clignoter la led rouge 3 fois
