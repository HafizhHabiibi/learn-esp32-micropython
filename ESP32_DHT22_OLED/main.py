from machine import Pin, I2C
from time import sleep
import dht
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor = dht.DHT22(Pin(4))

while True:
    sensor.measure() # baca parameter dari sensor
    suhu = sensor.temperature()
    lembab = sensor.humidity()
    print("Suhu : ", suhu)
    print("Kelembaban : ", lembab)

    #reset tampilan oled
    oled.fill(0)

    oled.text("Suhu : ", 0, 5)
    oled.text(str(suhu), 0, 15)
    oled.text("Kelembaban : ", 0, 30)
    oled.text(str(lembab), 0,40)

    #memperbarui tampilan oled
    oled.show()

    sleep(1)