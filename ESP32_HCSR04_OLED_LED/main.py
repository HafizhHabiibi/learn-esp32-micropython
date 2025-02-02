from hcsr04 import HCSR04
from time import sleep
from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
led = Pin(2, Pin.OUT)
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

while True:
    distance = sensor.distance_cm()
    print('Jarak :', distance, 'CM')
    # Reset tampilan OLED
    oled.fill(0)

    oled.text("Jarak:", 30, 15)
    oled.text(str(distance), 20, 35)
    oled.text("CM", 90, 35)

    # Perbarui tampilan OLED
    oled.show()
    
    sleep(1)

    if distance < 100 and distance > 0:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)
        
    else:
        led.off()