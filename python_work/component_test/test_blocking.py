import socket
import serial
import time
import numpy as np
import math

HOST = "192.168.0.1"  # The server's hostname or IP address
PORT_server = 9090  # The port used by the server

# bluetooth setup
port = "COM5"  # outgoing
bluetooth = serial.Serial(port, 9600, timeout = 0, write_timeout = 0)
print("Connected")
bluetooth.flushInput()
start = time.time()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT_server))

    run1_end = time.time()+1
    while time.time() < run1_end:
        data = None
        while not data:
            # request server to send data
            s.sendall(b"n")
            data = s.recv(1024)
        
        arr = data.decode().split("\n")
        vals = arr[-2].split(",")
        curr_x, curr_y, curr_t = (float(vals[0]), float(vals[1]), float(vals[-1]))

        print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, curr_x))
        
        bluetooth.write(bytes('f', 'utf-8'))
        time.sleep(0.1)

    run2_end = time.time()+1
    while time.time() < run2_end:
        data = None
        while not data:
            data = s.recv(1024)

        arr = data.decode().split("\n")
        vals = arr[-2].split(",")
        curr_x, curr_y, curr_t = (float(vals[0]), float(vals[1]), float(vals[-1]))

        print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, curr_x))
        
        bluetooth.write(bytes('r', 'utf-8'))
        time.sleep(0.1)
    s.sendall(b's')

bluetooth.write(bytes("s", "utf-8"))
bluetooth.close()





