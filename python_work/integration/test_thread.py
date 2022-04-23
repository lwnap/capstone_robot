import socket
import serial
import time
import numpy as np
import math
import threading
from multiprocessing import Queue

# global q, q_control
global q_control
global sx, sy, st, slope

# some controlling parameters (tuning required)
K_p = 0.1
tol = 0.5
tol_angle = 0.05    # 0.0005


def bluetooth_conn():
    # bluetooth setup
    port = "COM5"  # outgoing
    bluetooth = serial.Serial(port, 9600, write_timeout=0, timeout = 0)
    print("bluetooth Connected")
    bluetooth.flushInput()

    # bluetooth.write(bytes("f", 'utf-8'))
    # time.sleep(3)
    # bluetooth.write(bytes("s", 'utf-8'))
    # time.sleep(3)
    # bluetooth.write(bytes("f", "utf-8"))
    # time.sleep(3)
    # bluetooth.write(bytes("s", "utf-8"))

    global q_control
    signal = q_control.get()
    start = time.time()
    print("signal :{}".format(signal))
    # prrint()
    # bluetooth.write(bytes("f", 'utf-8'))
    bluetooth.write(bytes("f",'utf-8'))
    # while True:
    #     if time.time() - start > 3:
    #         break
    time.sleep(3)
    bluetooth.write(bytes("s", 'utf-8'))

    print("bt time: {}".format(time.time() - start))
    print("bt break!!!!!")
    bluetooth.close()
    return


def vicon_conn():
    server_HOST = "192.168.0.1"  # The server's hostname or IP address
    server_PORT = 9090  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_HOST, server_PORT))
        start_vicon = time.time()
        start_stable = time.time()
        i = 0
        while True:

            if time.time() - start_vicon > 10:
                print("vicon break!!!!!")
                s.sendall(b's')
                break

            data = None
            s.sendall(b"n")
            while not data:
                # request server to send data
                # s.sendall(b"n")
                data = s.recv(1024)

            arr = data.decode().split("\n")
            vals = arr[-2].split(",")
            # global q
            if i == 0:
                time.sleep(1)
                global sx, sy, st, slope
                sx, sy, st = (float(vals[0]), float(vals[1]), float(vals[-1]))
                print("start point: ", sx, sy, st)
                i += 1
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
                slope = -a / b
                q_vicon.put((sx, sy, st),block=True)
            else:
                q_vicon.put((float(vals[0]), float(vals[1]), float(vals[-1])),block=True)

        # s.sendall(b's')
    print("vicon time: {}".format(time.time()-start_vicon))
    return

if __name__ == '__main__':

    q_vicon = Queue()
    q_control = Queue()

    bt_thread = threading.Thread(target = bluetooth_conn)
    vicon_thread = threading.Thread(target = vicon_conn)
    # main_thread = threading.Thread(target = main)
    
    # main_thread.start()
    bt_thread.start()
    vicon_thread.start()

    while True:
        # global q, q_control
        # print("q: {}".format(q))
        vals = q_vicon.get()
        # print("real time vicon: {}".format(vals))
        curr_x, curr_y, curr_t = (float(vals[0]), float(vals[1]), float(vals[-1]))

        if curr_x == sx:
            message = "f"
        else:
            slope1 = -(curr_y - sy) / (sx - curr_x)

            error_angle = np.arctan2((slope - slope1), (1 + slope * slope1))

            if error_angle > 3.14 / 2:
                error_angle = error_angle - np.pi
            elif error_angle < -3.14 / 2:
                error_angle = np.pi + error_angle

            print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, error_angle))

            if abs(error_angle) < tol_angle:
                message = "f"
            elif error_angle > tol_angle:
                message = "r"  # "l"
            elif error_angle < -tol_angle:
                message = "l"  # "r"
            else:
                message = ""
        print("message from main : {}".format(message))
        q_control.put((message), block = True)



