import serial
import time

print("Start")
port = "COM5"  # outgoing in vc
#port="COM4"
bluetooth = serial.Serial(port, 9600)
print("Connected")
bluetooth.flushInput()
start = time.time()
while time.time() - start < 1.5:
    print("ping")
    bluetooth.write(b'f')
    input_date = bluetooth.readline()
    print(input_date.decode())
    # print(input_date)
    time.sleep(0.1)
bluetooth.write(b's')

bluetooth.close()
print("Done")

