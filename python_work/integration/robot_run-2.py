import socket
import serial
import time
import numpy as np
import math

HOST = "192.168.0.1"  # The server's hostname or IP address
PORT = 9090  # The port used by the server

# ####bluetooth setup
port = "COM5"  # outgoing
bluetooth = serial.Serial(port, 9600, write_timeout=0.1)
print("Connected")
bluetooth.flushInput()

# some controlling parameters (tuning required)
K_p = 0.1
tol = 0.5
tol_angle = 0.05    # 0.0005

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    data = None
    stable_start_time = time.time()
    stable_start_timeout = stable_start_time + 2.0

    s.sendall(b"n")
    while not data:
        # request server to send data
        # s.sendall(b"n")
        data = s.recv(1024)
    
    arr = data.decode().split("\n")
    vals = arr[-2].split(",")
    sx, sy, st = (float(vals[0]), float(vals[1]), float(vals[-1]))
    print("start point: ", sx, sy, st)

    # assume we only travels l meters
    l = 0.5

    # ####################### test case 1: starting from the desired orientation #################
    ex = sx + l * 1000 * np.cos(st)  # vicon represents in mm
    ey = sy + l * 1000 * np.sin(st)
    et = st
    print("end point: ", ex, ey, et)

    # line function calculation: ax +  by + c = 0
    a = ey - sy
    b = sx - ex
    c = -(a * sx + b * sy)
    slope = -a/b

    time.sleep(0.11)

    start = time.time()
    while abs(time.time() - start) <= 10:
        data = None
        # request server to send data
        s.sendall(b"n")
        while not data:
            data = s.recv(1024)

        arr = data.decode().split("\n")
        vals = arr[-2].split(",")
        curr_x, curr_y, curr_t = (float(vals[0]), float(vals[1]), float(vals[-1]))

        slope1 = -(curr_y - sy)/(sx - curr_x)

        error_angle = np.arctan2((slope - slope1), (1 + slope*slope1))

        if error_angle > 3.14/2:
            error_angle = error_angle - np.pi
        elif error_angle < -3.14/2:
            error_angle = np.pi + error_angle

        print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, error_angle))

        if abs(error_angle) < tol_angle:
            message = "f"
        elif error_angle > tol_angle:
            message = "r"  # "l"
        elif error_angle < -tol_angle:
            message = "l"  # "r"

        # bluetooth.write(b"a " + bytes(start_string, 'utf-8') + b" a")
        bluetooth.write(bytes(message, 'utf-8'))
        # input = bluetooth.readline().decode()
        # print(input)
        time.sleep(0.11)

    s.sendall(b's')

print(time.time()-start)
print("cry ab it")
bluetooth.flushInput()
bluetooth.write(bytes("s", "utf-8"))
bluetooth.close()





