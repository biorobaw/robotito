#!/usr/bin/python
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print ('Reading Values')
while True:
    values=[0]*8
    for i in range(8):
        values[i] = mcp.read_adc(i)
    print(values[i])
    print('\n\n')
    time.sleep(.25)