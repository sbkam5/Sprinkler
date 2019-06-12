#!/usr/bin/env python3
#yutong wang

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import time

title = "BRUH:"
string = "WE LIVE in a SOCIETY, and society lives in us! "


def str_loop(length):
    counter = 15
    if length>16:
        buf = string[0:15]
    else:
        buf = string
    while True:
        #lcd.delayMicroseconds(200)
        lcd.clear()
        lcd.message(title+'\n')
        lcd.message(buf)
        time.sleep(0.3)
        buf = buf[1:] + string[counter]
        counter+=1
        if counter>=length:
            counter=0



def LCDprint(str1, str2):
    mcp.output(3,1) #turn on LCD backlight
    lcd.begin(16,2) #set number of LCD lines and columns
    lcd.setCursor(0,0)
    str_loop(len(string))

def destroy():
    lcd.clear()

def lcd_start():
    PCF8574_address = 0x27 #I2C address of PCF8574
    PCF8574A_address = 0x3F #I2C address of PCF8574A

    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print("I2C Address Error !")
            exit(1)
#create LCD, passing in MCP GPIO adapter
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
    try:
        LCDprint(title + '\n',string)
    except KeyboardInterrupt:
        destroy()

if __name__ == '__main__':
    print('BRUH')
    try:

        LCDprint(title + '\n',string)
    except KeyboardInterrupt:
        destroy()
