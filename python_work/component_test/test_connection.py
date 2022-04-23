import socket

# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
clientSocket.connect(("192.168.0.1", 9090))

# Send data to server
data = "Hello Server!"
clientSocket.send(data.encode())

# with open("Output.txt", "w") as text_file:
while True:
    try:
        # Receive data from server
        dataFromServer = clientSocket.recv(1024)

        # Print to the console
        print(dataFromServer.decode())
        # trans = eval(dataFromServer.decode())
        arr = dataFromServer.decode().split("\n")
        vals = arr[-2].split(",")

        # translational (x,y,z) rotational(Euler) (x, y, z)

        print(vals)

        # dataFromServer.decode()
        # rot = eval(dataFromServer.decode())
        # print(rot)
        # with open("Output.txt", "w") as text_file:
            # text_file.write(dataFromServer.decode())
        # print("{}".format(dataFromServer.decode()), file=text_file)
        # print("global translation: {}".format(dataFromServer.decode()), file=text_file)

    except SyntaxError:
        print("SYNTAX ERROR")
        f = open("error.log","w")
        f.write(dataFromServer.decode())
        f.write("\n")
        f.close()

            