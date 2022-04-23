import socket
import serial
import time
import numpy as np

# ####bluetooth setup
port = "COM5"  # outgoing
bluetooth = serial.Serial(port, 9600)
print("Connected")
bluetooth.flushInput()


# ####vicon connection
# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to the server
clientSocket.connect(("192.168.0.1", 9090))
# Send data to server
data = "Hello Server!"
clientSocket.send(data.encode())

# some controlling parameters (tuning required)
K_p = 0.1
tol = 0.5
tol_angle = 0.05    # 0.0005

dataFromServer = clientSocket.recv(1024)

# line set up
arr = dataFromServer.decode().split("\n")
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
const = np.sqrt(a ** 2 + b ** 2)

# the command to the robot
message = ""

# robot path
x_point = []
y_point = []
cnt = 0

start_stable_data = time.time()
stable_data_timeout = start_stable_data+2
while True:

    if time.time() > stable_data_timeout:
        break

    print("====== show data for 2 sec ======")
    dataFromServer = clientSocket.recv(1024)
    print(dataFromServer.decode())
    arr = dataFromServer.decode().split("\n")
    vals = [float(s) for s in arr[-2].split(",")]
    # translational (x,y,z) rotational(Euler) (x, y, z)
    print("split values: ", vals)


time.sleep(5)
start = time.time()
timeout = start + 1.5
print(start)
bluetooth.write(bytes('f', 'utf-8'))
input = bluetooth.readline().decode()
print(input)
while True:

    print("++++++++ start while loop ++++++++")
    if time.time() > timeout:
        # bluetooth.write(bytes("s", "utf-8"))
        # bluetooth.close()
        break

    print("in looop: ", cnt)
    dataFromServer = clientSocket.recv(1024)

    print(dataFromServer.decode())
    arr = dataFromServer.decode().split("\n")
    # we only take the last set of measurements
    vals = [float(s) for s in arr[-2].split(",")]
    # translational (x,y,z) rotational(Euler) (x, y, z)
    print("split values: ", vals)

    # get current position and orientation
    curr_x, curr_y, curr_t = vals[0], vals[1], vals[-1]
    slope1 = -(curr_y - sy)/(sx - curr_x)
    # angle between two lines:
    error_angle = np.arctan2((slope - slope1), (1 + slope*slope1))

    if error_angle > 3.14/2:
        error_angle = error_angle - np.pi
    elif error_angle < -3.14/2:
        error_angle = np.pi + error_angle

    print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, error_angle))

    if error_angle > tol_angle:
        message = "r"  # "l"
    elif error_angle < -tol_angle:
        message = "l"  # "r"

    # bluetooth.write(b"a " + bytes(start_string, 'utf-8') + b" a")
    bluetooth.write(bytes(message, 'utf-8'))
    # input = bluetooth.readline().decode()
    # print(input)
    time.sleep(0.1)

    cnt += 1

print("time ended")
print(time.time()-start)
bluetooth.write(bytes("s", "utf-8"))
bluetooth.close()
print('Done')
