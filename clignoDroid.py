#!/usr/bin/env python3
########################################################################
# Filename    : ClignoDroid.py
# Description : Jeux de mémoire SIMON
# auther      : papsDroid
# modification: 2019/06/01
########################################################################
import RPi.GPIO as GPIO
from clignodroid_lcd import Lcd
from clignodroid_led import Led, RackLeds
from clignodroid_buton import Button_quit, Button_led, RackButtons
import time
from random import randint
from clignodroid_buz import Buzz
                                                   
class JeuxSIMON():
    def __init__(self):
        self.rep = '/home/pi/ClignoDroid/' # répertoire  jeux
        self.record = self.readScore() # record
        self.niveau = 1           # niveau = nb d eleds dans une séquence
        self.seq = 0              # séquence en cours du joueur (terminé si seq==niveau)
        self.seq_led_droid = []   # sequence à retenir
        self.seq_led_joueur = []  # séquence du joueur
        self.continuer = True     # fin de partie: continuer=False

    def nouvelle_seq(self):
        self.seq_led_droid = []
        self.seq_led_joueur = []
        for n in range(self.niveau):
            self.seq_led_droid.append(randint(0,3))
        print('séquence droid - niveau:', self.niveau, self.seq_led_droid)
    
    def add_sequence_joueur(self, id):
        self.seq_led_joueur.append(id)
        
    def readScore(self):
        s=0
        with open(self.rep+'score.txt') as f:
            content = f.read()
            try:
                s=int(content)
            except:
                s=0
            f.close()
            return s
    
    def writeScore(self, s):
        with open(self.rep+'score.txt','w') as f:
            f.write(str(s))
            f.close()
        
        
class Application:
    def __init__(self, buzzerOn=False, powerOff=False):
        print ('Program is starting ... ')
        GPIO.setmode(GPIO.BOARD)        # Numbers GPIOs by physical location
        self.lcd = Lcd()                # affichage LCD du jeux
        self.rackleds=RackLeds()        # rack de leds
        self.buzzer=Buzz(buzzerOn)      # buzzer du jeux
        self.button_quit=Button_quit(self, powerOff)                # bouton on/off
        self.rackbuttons=RackButtons(self.rackleds, self.buzzer)    # rack de boutons de commande des leds
        self.jeux = JeuxSIMON()

    def loop(self):
        self.lcd.clear()
        while True :
            self.jeux.niveau=1
            self.lcd.msg('Record:'+str(self.jeux.record),'On commence ?')
            self.rackbuttons.desactivateLeds()  #désactive les leds associées aux boutons
            #attente appui sur bouton de démarrage: bouton led Verte=démarrage avec buzzer activé, bouton led rouge = buzzer désactivé
            while not(self.rackbuttons.pressed 
                      and self.rackbuttons.id_button_pressed in [0,3]):
                pass
            if self.rackbuttons.id_button_pressed==0:
                self.buzzer.on()
            else:
                self.buzzer.off()
            self.lcd.clear()
            self.jeux.continuer = True
            while (self.jeux.continuer):
                #création d'une nouvelle séquence à reproduire
                self.jeux.nouvelle_seq()    
                self.lcd.msg('Record:'+str(self.jeux.record),'Niveau:'+str(self.jeux.niveau))
                #affichage séquence de leds
                time.sleep(1)
                for n in range(self.jeux.niveau):
                    id_led = self.jeux.seq_led_droid[n]
                    self.rackleds.leds[id_led].on()     # led allumée
                    self.buzzer.buzzId(id_led)          # buzzer correspondant à la led
                    time.sleep(self.rackleds.tp_led)    # temps d'attente
                    self.rackleds.leds[id_led].off()    # led éteinte
                    self.buzzer.mute()                  # buzzer mute
                    time.sleep(self.rackleds.tp_led)    # temps d'attente
                #mémorisation séquence du joueur
                print('à toi de jouer')
                self.rackbuttons.activateLeds()  #active les leds associées aux boutons
                for n in range(self.jeux.niveau):
                    #attente qu'un bouton du rack de boutons soit pressée
                    #print('allume une led')
                    while not(self.rackbuttons.pressed):
                        pass
                    self.rackbuttons.pressed = False
                    self.jeux.add_sequence_joueur(self.rackbuttons.id_button_pressed)
                self.rackbuttons.desactivateLeds()  #désactive les leds associées aux boutons
                #print('Voici ton jeu: ', self.jeux.seq_led_joueur)
                #comparaison des listes joueur et clignodroid
                time.sleep(1)
                if (self.jeux.seq_led_joueur == self.jeux.seq_led_droid):
                    print('Bien joué! niveau suivant')
                    self.rackleds.gagne()   #animation leds gagné
                    if (self.jeux.record<self.jeux.niveau): #gestion du record
                        self.jeux.record=self.jeux.niveau
                        self.jeux.writeScore(self.jeux.record)
                    self.jeux.niveau += 1
                else:
                    print('Perdu!')    
                    self.rackleds.perdu()   #animation leds perdu
                    self.jeux.continuer = False

    def destroy(self):
        print ('bye')
        self.buzzer.off()   # buzzer off
        self.rackleds.off() # etteind toutes les leds
        self.lcd.off()      # extinction lcd
        GPIO.cleanup()      # Release resource      

if __name__ == '__main__':     # Program start from here
    appl=Application(buzzerOn=False, powerOff=True)
    try:
        appl.loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        appl.destroy()
