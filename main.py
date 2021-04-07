import dht
from machine import I2C , Pin ,ADC ,RTC , Timer
from ssd1306 import SSD1306_I2C
from time import sleep_ms
import machine


#pin definition

dht22_pin = Pin(2)
scl_pin = Pin(5)
sda_pin = Pin(4)
adc = ADC(0)
button = Pin(14 , Pin.IN  , Pin.PULL_UP)
button_2 = Pin(12 , Pin.IN  , Pin.PULL_UP)


rtc = machine.RTC()
rtc.irq(trigger = rtc.ALARM0 , wake = machine.DEEPSLEEP)

def debounce(pin):
    prev = None
    for _ in range(32):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
        
    return prev

def deepsleep_call(pin):
    d = debounce(pin)
    
    if d == None:
        return
    elif not d:
        rtc.alarm(RTC.ALARM0 , 2000)
        machine.deepsleep()
    


#sensor function
def get_sensor_data():
    
    ldr = adc.read()
    sensor = dht.DHT22(dht22_pin)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    
    
    i2c = I2C (scl = scl_pin , sda = sda_pin )
    disp = SSD1306_I2C(128 , 32 , i2c)
    
    disp.fill(0)
    disp.show()
    
    sleep_ms(500)
    disp.text("temp: " , 0 , 0 )
    disp.text(str(temp) , 64 , 0)
    disp.text("hum: " , 0 , 8 )
    disp.text(str(hum) , 64, 8 )
    disp.text("ldr: " , 0 , 16)
    disp.text(str(ldr) , 64, 16 )
    disp.show()
    

    
button.irq(trigger = Pin.IRQ_FALLING , handler = deepsleep_call )


while True:
    get_sensor_data()
    sleep_ms(2000)
