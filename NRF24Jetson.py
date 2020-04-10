"""
Example of library driving the nRF24L01 to communicate with a nRF24L01 driven by
the TMRh20 Arduino library. The Arduino program/sketch that this example was
designed for is named GettingStarted_HandlingData.ino and can be found in the "RF24"
examples after the TMRh20 library is installed from the Arduino Library Manager.
"""
import time
import struct
import board
import digitalio as dio
from circuitpython_nrf24l01 import RF24

# addresses needs to be in a buffer protocol object (bytearray)
address = [b'1Node', b'2Node']

# change these (digital output) pins accordingly
ce = dio.DigitalInOut(board.D5)
csn = dio.DigitalInOut(board.D13)

# using board.SPI() automatically selects the MCU's
# available SPI pins, board.SCK, board.MOSI, board.MISO
spi = board.SPI()  # init spi bus object

# initialize the nRF24L01 on the spi bus object
nrf = RF24(spi, csn, ce, ask_no_ack=False)
nrf.dynamic_payloads = False # this is the default in the TMRh20 arduino library

# set address of TX node into a RX pipe
nrf.open_rx_pipe(1, address[1])
# set address of RX node into a TX pipe
nrf.open_tx_pipe(address[0])

def master():  # count = 5 will only transmit 5 packets
    """Transmits an arbitrary unsigned long value every second. This method
    will only try to transmit (count) number of attempts"""

    # for the "HandlingData" part of the test from the TMRh20 library example
    float_value = 0.01
    while 1:
        nrf.listen = False # ensures the nRF24L01 is in TX mode
        print("Now Sending")
        start_timer = int(time.monotonic() * 1000) # start timer
        # use struct.pack to packetize your data into a usable payload
        # '<' means little endian byte order.
        # 'L' means a single 4 byte unsigned long value.
        # 'f' means a single 4 byte float value.
        buffer = struct.pack('<Lf', start_timer, float_value)
        result = nrf.send(buffer)
        if not result:
            print('send() failed or timed out')
        time.sleep(.05)

print("""\
    nRF24L01 communicating with an Arduino running the\n\
    TMRh20 library's "GettingStarted_HandlingData.ino" example.\n\
    Run slave() on receiver\n\
    Run master() on transmitter""")
master()