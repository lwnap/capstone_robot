import socket
import serial
import time
import numpy as np

# ####bluetooth setup
port = "COM5"  # outgoing
bluetooth = serial.Serial(port, 9600)
print("STOP THAT THING")
bluetooth.flushInput()
bluetooth.write(bytes("s", "utf-8"))
bluetooth.close()
print('Done')
