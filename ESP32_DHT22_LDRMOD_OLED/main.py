from machine import Pin, I2C, ADC
from time import sleep
import dht
import ssd1306

# Inisialisasi I2C untuk OLED (0.96" 128x64)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Inisialisasi sensor DHT22
sensor = dht.DHT22(Pin(15))

# Inisialisasi sensor LDR di pin ADC (gunakan GPIO 34)
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)  # Agar bisa membaca hingga ~3.3V

while True:
    # Membaca suhu dan kelembaban dari DHT22
    sensor.measure()
    suhu = sensor.temperature()
    lembab = sensor.humidity()

    # Membaca nilai dari sensor LDR (0 - 4095) setiap sensor berbeda
    nilai_ldr = 4095 - ldr.read()

    # Menampilkan hasil di Serial Monitor
    print("-" * 30)
    print(f"Suhu      : {suhu} °C")
    print(f"Kelembaban: {lembab} %")
    print(f"Cahaya    : {nilai_ldr}")
    print("-" * 30)

    # Membersihkan layar OLED
    oled.fill(0)

    # Header
    oled.text("Monitoring IoT", 15, 0)

    # Menampilkan data sensor lebih besar & rapi
    oled.text("Suhu  :", 0, 15)
    oled.text(f"{suhu:.1f} C", 70, 15)

    oled.text("Humid :", 0, 30)
    oled.text(f"{lembab:.1f} %", 70, 30)

    oled.text("LDR   :", 0, 45)
    oled.text(f"{nilai_ldr}", 70, 45)  # Menampilkan nilai LDR dalam rentang 0-4095

    # Memperbarui tampilan OLED
    oled.show()

    # Delay 1 detik sebelum membaca ulang
    sleep(1)