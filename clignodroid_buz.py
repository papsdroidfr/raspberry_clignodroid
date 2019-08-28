#!/usr/bin/env python3
########################################################################
# Filename    : clignodroid_buzz.py
# Description : Jeux de mémoire SIMON
# auther      : papsDroid
# modification: 2019/06/01
########################################################################
import RPi.GPIO as GPIO

class Buzz():
    def __init__(self, buzzerOn=False):
        self.buzzerPin = 29                     # GPIO 05
        GPIO.setup(self.buzzerPin, GPIO.OUT)    # Set buzzerPin's mode is output
        self.pwmLevel=5                         # niveau 0 (off) à 100 (max) sortie buzzer
        self.pwmFreqG=262                       # fréquence ledG = DO
        self.pwmFreqB=330                       # fréquence ledB = MI
        self.pwmFreqY=392                       # fréquence ledY = SOL
        self.pwmFreqR=440                       # fréquence ledR = LA
        self.pwm = GPIO.PWM(self.buzzerPin, self.pwmFreqG)
        if buzzerOn:
            self.on()                               # activation du buzzer
        else: 
            self.off()                              # désactivation du buzzer
    
    def on(self):
        self.buzzerOn = True                    
        self.pwm.start(0);
    
    def off(self):
        self.buzzerOn = False
        self.pwm.stop()
    
    def mute(self):
        if self.buzzerOn:
            self.pwm.ChangeDutyCycle(0)
            
    def buzzId(self, id):  
        if self.buzzerOn:
            if id==0:
                self.pwm.ChangeFrequency(self.pwmFreqG)
            elif id==1:
                self.pwm.ChangeFrequency(self.pwmFreqB)
            elif id==2:
                self.pwm.ChangeFrequency(self.pwmFreqY)
            else:
                self.pwm.ChangeFrequency(self.pwmFreqR)
            self.pwm.ChangeDutyCycle(self.pwmLevel)
    
    
        
    
