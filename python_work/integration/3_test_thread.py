import socket
import serial
import time
import numpy as np
import math
import threading
from multiprocessing import Queue

# global q, q_control
global q_control, signal_stack
global sx, sy, st, ex, ey, et, slope

# some controlling parameters (tuning required)
K_p = 0.1
tol = 0.5
tol_angle = 0.05    # 0.0005
tol_dist = 20
global_timeout = 5

# assume we only travels l meters
l = 0.3

# bluetooth signal delay
k = 0.4


def bluetooth_conn():
    # bluetooth setup
    port = "COM5"  # outgoing
    bluetooth = serial.Serial(port, 9600)
    print("bluetooth Connected")
    bluetooth.flushInput()
    start = time.time()
    global q_control
    bluetooth.write(bytes("f", 'utf-8'))
    bt_send_delay = False
    while True:
        # time.sleep(k)
        signal_stack = q_control.get()
        if signal_stack[-1] == "s":
            bluetooth.write(bytes("s", 'utf-8'))
            break

        if time.time() - start > global_timeout:
            # bluetooth.write(bytes("s", 'utf-8'))
            print("bt timeout!!!")
            break

        signal = signal_stack[-1]
        print("signal {}".format(signal))
        bluetooth.write(bytes(signal, 'utf-8'))
        delay_start = time.time()
        while time.time() - delay_start < 0.5:
            if signal_stack[-1] == "s":
                bluetooth.write(bytes("s", 'utf-8'))
                break
    # time.sleep(2)
    bluetooth.write(bytes("s", 'utf-8'))
    print("bt time: {}".format(time.time() - start))
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

            if time.time() - start_vicon > global_timeout:
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
                global sx, sy, st, ex, ey, et, slope
                sx, sy, st = (float(vals[0]), float(vals[1]), float(vals[-1]))
                print("start point: ", sx, sy, st)
                i += 1

                # ####################### test case 1: starting from the desired orientation #################
                ex = sx - l * 1000 * np.cos(st)  # vicon represents in mm
                ey = sy - l * 1000 * np.sin(st)
                et = st
                print("end point: ", ex, ey, et)

                # line function calculation: ax +  by + c = 0
                a = ey - sy
                b = sx - ex
                slope = -a / b
                q_vicon.put((sx, sy, st),block=True)
            else:
                curr_x, curr_y, curr_t = (float(vals[0]), float(vals[1]), float(vals[-1]))
                # print("current vicon pose: x {} y {} t {}".format(curr_x, curr_y, curr_t))
                q_vicon.put((curr_x, curr_y, curr_t),block=True)

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
    signal_stack = ["f"]
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

            # print("current x position {}, y_position {}, orientation {}, lateral distance to line {}".format(curr_x, curr_y, curr_t, error_angle))

            if abs(error_angle) < tol_angle:
                message = "f"
            elif error_angle > tol_angle:
                message = "r"  # "l"
            elif error_angle < -tol_angle:
                message = "l"  # "r"
            else:
                message = ""

            if np.sqrt((curr_x - ex) ** 2 + (curr_y - ey) ** 2) < tol_dist:
                message = "s"
        # print("message from main : {}".format(message))
        if message != signal_stack[-1]:
            signal_stack.append(message)
        q_control.put((signal_stack), block = True)
        # print(signal_stack)



