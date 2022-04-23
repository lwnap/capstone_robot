import serial
import time
import numpy as np

# print("Start")
# bluetooth setup
port = "COM5"  # outgoing in vc
bluetooth = serial.Serial(port, 9600)
print("Connected")
bluetooth.flushInput()

# first step: input start and end position
precision = 10
# start_point = input("Starting point with 0.1 precision (format: x,y, theta): ")
sx, sy, st = (0.0, 1.0, 0.0) #eval(start_point)
# end_point = input("Ending point with 0.1 precision (format: x,y, theta): ")
ex, ey, et = (2.0, 4.0, 0.0)  # eval(end_point)
# line function calculation: ax +  by + c = 0
a = ey - sy
b = sx - ex
c = -(a*sx + b*sy)
# point to line dist: d = (ax_0 + by_0 + c) / sqrt(a^2 + b^2)
const = np.sqrt(a**2 + b**2)
print(a, b, c, const)

# some controlling parameters (tuning required)
K_p = 0.1
tol = 0.05
print(sx, sy, st, ex, ey, et)

# start_point = [str(int(i*10)) for i in eval(start_point)]
# end_point = input("Ending point (x,y): ")
# end_point = eval(end_point)

# # send to the arduino, string starting with 9 means start point, starting with 8 means end point
# start_string = "s "+" ".join(start_point)+" s"
# # string = "s 10 20 s"
#
# # bluetooth.write(" ".join(["8"] + [str(x) for x in end_point]))
# for i in range(1):
#     print(i)
#     # bluetooth.write(b"a " + bytes(start_string, 'utf-8') + b" a")
#     bluetooth.write(bytes(start_string, 'utf-8'))
#     input = bluetooth.readline().decode()
#     print(input)
#     time.sleep(0.1)
#
# bluetooth.close()
# print('Done')

# the command to the robot
message = ""

# ####################### test case 1: starting from the desired orientation #################
curr_pos = np.linspace([sx, sy, 0], [ex, ey, 0], num=11)
curr_pos[3][0] += 0.1

start = time.time()
i = 0
while time.time() - start < 10:  # almost one loop per sec
    print(i)
    curr_x, curr_y, _ = curr_pos[i]
    # error calculation (lateral error)
    e_l = abs(a * curr_x + b * curr_y + c) / const
    print(curr_x, curr_y, e_l)
    if e_l > tol:  # robot is on the right of the trajectory, and left wheel should be slower
        message = "l"
    elif e_l < -tol:
        message = "r"
    else:
        message = "f"  # go forward
    # bluetooth.write(b"a " + bytes(start_string, 'utf-8') + b" a")
    bluetooth.write(bytes(message, 'utf-8'))
    input = bluetooth.readline().decode()
    print(input)
    time.sleep(0.1)
    i += 1
bluetooth.write(bytes("s", "utf-8"))
bluetooth.close()
print('Done')


# #################### test case 2: start from an undesired orientation ##########################
