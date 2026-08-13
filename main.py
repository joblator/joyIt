# Load libraries
from machine import Pin, PWM
from utime import sleep
from neopixel import NeoPixel
from dht import DHT11
import lcd_gfx
import ST7735
import time 
import math
#import cv2
#CONSTANTS
image_path = "cat1.bin"
buttons = [10, 11, 14, 15]
lcdLightPin = 2
dhtPin = 0

#initilazing
spi = machine.SPI(0, baudrate=8000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))
backlight = Pin(lcdLightPin, Pin.OUT)

lcd = ST7735.ST7735(spi, rst=6, ce=17, dc=3)
dht = DHT11(Pin(dhtPin, Pin.IN))
buttonUp = Pin(buttons[0], Pin.IN, Pin.PULL_UP)
buttonRight = Pin(buttons[1], Pin.IN, Pin.PULL_UP)
buttonDown = Pin(buttons[2], Pin.IN, Pin.PULL_UP)
backlight.high() 
lcd.reset()
lcd.begin()
#turn screen green
lcd.fill_screen(lcd.rgb_to_565(15, 23, 42))


def show_picture(picture_path):
        # 1. Set the window to the FULL screen dimensions just once
    lcd.set_addr_window(0, 0, 128, 160)

    # 2. Keep the SPI pins open for a long continuous transmission
    lcd._dc.high()
    lcd._ce.low()

    with open(image_path, 'rb') as f:
        # Use a standard while loop since we don't care about X/Y coordinates anymore
        while True:
            
            # Read 32 bytes (16 pixels) at a time
            chunk = f.read(1) 
            if not chunk:
                break # Reached the end of the file
                
            # Blast the chunk
            lcd._spi.write(bytearray(chunk))

    # 3. Close the SPI transmission only when the whole file is done
    lcd._ce.high()

def feels_like_temp_hot(temp, humid):
    exponent_value = (17.27*temp)/(237.7+temp)
    vapor_pressure = (humid/100) * 6.105 * math.exp(exponent_value)
    feels_temp = temp + 0.33 * vapor_pressure - 4
    return feels_temp

def show_temp():
    print("showing temp")
            # Measure DHT11 values
    dht.measure()
    temp = dht.temperature()
    humid = dht.humidity()
    if temp >= 20:
        feels_temp = feels_like_temp_hot(temp,humid)
    else:
        feels_temp = 0
    lcd.p_string(20,50,'Temp.: ' + str(temp))
    lcd.p_string(20,80,'Humid.: ' + str(humid)+'%')
    lcd.p_string(20,110,'feels like: ' + str(feels_temp))
    time.sleep(1)

    

def main():
    current_State = 'Menu'
    last_state = 'menu'
    last_down_state = 1
    last_up_state = 1
    lcd.p_string(20,50,"up to show temp")
    lcd.p_string(20,80,"down to show cat")
    while True:
        up_state = buttonUp.value()
        down_state = buttonDown.value()
        if up_state == 0 and last_up_state == 1:
            current_State = "Temp"
        if down_state == 0 and last_down_state == 1:
            current_State = "Image"
        
        if current_State == "Temp" and last_state != "Temp":
            lcd.fill_screen(lcd.rgb_to_565(15, 23, 42))
            show_temp()
        if current_State == "Image" and last_state != "Image":
            show_picture(image_path)
        last_up_state = up_state
        last_down_state = down_state
        last_state = current_State
        print(current_State)


        
main()



    