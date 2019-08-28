#!/usr/bin/env python3
########################################################################
# Filename    : clignodroid_lcd.py
# Description : Jeux de mémoire SIMON
# auther      : papsDroid
# modification: 2019/06/04
########################################################################

from PCF8574 import PCF8574_GPIO                # gestion LCD
from Adafruit_LCD1602 import Adafruit_CharLCD   # gestion LCD
import time

class Lcd:
    def __init__(self):
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)
        self.lcd.clear()
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns
        self.msg('  ClignoDroid  ', ' Initialisation ')

    def clear(self):
        self.lcd.clear()
        
    def msg(self, lig1, lig2=''):
        self.lcd.setCursor(0,0) # set cursor position
        self.lcd.message(lig1+'\n')
        self.lcd.message(lig2)
        
    def off(self):
        self.clear()
        self.msg('Au revoir.')
        time.sleep(2)
        self.lcd.clear()
        self.mcp.output(3,0)     # turn off LCD backlight     
