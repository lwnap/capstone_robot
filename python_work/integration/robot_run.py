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

# keep receiving data

# line set up
arr = dataFromServer.decode().split("\n")
vals = arr[-2].split(",")
sx, sy, st = (float(vals[0]), float(vals[1]), float(vals[-1]))
print("start point: ", sx, sy, st)
#start_point = input("Starting point with 0.1 precision (format: x,y, theta): ")
#sx, sy, st = eval(start_point)
# end_point = input("Ending point with 0.1 precision (format: x,y, theta): ")
# ex, ey, et = eval(end_point)

# assume we only travels l meters
l = 0.5

# ####################### test case 1: starting from the desired orientation #################
print("###################### test case 1: starting from the desired orientation. #########################")
ex = sx + l * 1000 * np.cos(st)  # vicon represents in mm
ey = sy + l * 1000 * np.sin(st)
et = st
print("end point: ", ex, ey, et)

# ####################### test case 2: starting from a wrong orientation #################
print("################# test case 2: starting from a wrong orientation ###############")
et = st + np.pi/4   # suppose we are off by 45 degrees
ex = sx + l * 1000 * np.cos(et)  # vicon represents in mm
ey = sy + l * 1000 * np.sin(et)


# line function calculation: ax +  by + c = 0
a = ey - sy
b = sx - ex
c = -(a * sx + b * sy)
slope = -a/b
# point to line dist: d = (ax_0 + by_0 + c) / sqrt(a^2 + b^2)
const = np.sqrt(a ** 2 + b ** 2)
# print(a, b, c, const)



# the command to the robot
message = ""

cnt = 0
#while True:
start = time.time()
timeout = start + 1.5
print(start)
bluetooth.write(bytes('f', 'utf-8'))
input = bluetooth.readline().decode()
print(input)
while True:

    if time.time() > timeout:
        bluetooth.write(bytes("s", "utf-8"))
        bluetooth.close()
        break

    print("in looop: ", cnt)
    dataFromServer = clientSocket.recv(1024)

    # try:
    # Print to the console
    print(dataFromServer.decode())
    arr = dataFromServer.decode().split("\n")
    # we only take the last set of measurements
    vals = [float(s) for s in arr[-2].split(",")]
    # translational (x,y,z) rotational(Euler) (x, y, z)
    print("split values: ", vals)

    # get current position and orientation
    curr_x, curr_y, curr_t = vals[0], vals[1], vals[-1]

    # slope of current position to the starting point
    slope1 = -(curr_y - sy)/(sx - curr_x)
    # angle between two lines:
    error_angle = np.arctan2((slope - slope1), (1 + slope*slope1))

    if error_angle > 3.14/2:
        error_angle = error_angle - np.pi
    elif error_angle < -3.14/2:
        error_angle = np.pi + error_angle

    # error calculation (lateral error)
    # e_l = (a * curr_x + b * curr_y + c) / const
    # error calculation (heading error)
    # e_h = et - curr_t
    print("current x position {}, y_position {}, lateral distance to line {}".format(curr_x, curr_y, error_angle))
    # if e_l > tol:  # robot is on the right of the trajectory, and left wheel should be slower
    #     message = "l"
    # elif e_l < -tol:
    #     message = "r"

    # if abs(error_angle) < tol_angle:
    #     message = "f"
    if error_angle > tol_angle:
        message = "r"  # "l"
    elif error_angle < -tol_angle:
        message = "l"  # "r"

    # bluetooth.write(b"a " + bytes(start_string, 'utf-8') + b" a")
    bluetooth.write(bytes(message, 'utf-8'))
    # input = bluetooth.readline().decode()
    # print(input)
    time.sleep(0.1)

    # except SyntaxError:
    #     print("SYNTAX ERROR")
    #     f = open("error.log", "w")
    #     f.write(dataFromServer.decode())
    #     f.write("\n")
    #     f.close()
    cnt += 1

print("time ended")
print(time.time()-start)
# bluetooth.write(bytes("s", "utf-8"))
# bluetooth.close()
print('Done')
