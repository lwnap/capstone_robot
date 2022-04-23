from __future__ import print_function
import socket
from vicon_dssdk import ViconDataStream

import socket

import time

HOST = "192.168.0.1"  # Standard loopback interface address (localhost)
PORT = 9090  # Port to listen on (non-privileged ports are > 1023)

client = ViconDataStream.RetimingClient()
client.Connect( "localhost:801" )
client.SetAxisMapping( ViconDataStream.Client.AxisMapping.EForward, ViconDataStream.Client.AxisMapping.ELeft, ViconDataStream.Client.AxisMapping.EUp )

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # bind
    s.bind((HOST, PORT))
    # remove blocking
    s.setblocking(True)
    # listen
    s.listen()
    # accept
    conn, addr = s.accept()
    # 
    with conn:
        print(f"Connected by {addr}")
        while True:
            # get update signal from laptop
            data = conn.recv(1024)

            if data.decode('utf-8').strip() == "n":
                # get from VICON
                client.UpdateFrame()
                # get object
                subjectNames = client.GetSubjectNames()
                for subjectName in subjectNames:
                        #print( subjectName )
                        segmentNames = client.GetSegmentNames( subjectName )
                        for segmentName in segmentNames:
                            translationCoors = client.GetSegmentGlobalTranslation( subjectName, segmentName )[0]
                            rotationEuler = client.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName )
                data = (str(translationCoors[0])+","+str(translationCoors[1])+","+str(translationCoors[2])+","+str(rotationEuler[0][0])+","+str(rotationEuler[0][1])+","+str(rotationEuler[0][2])+'\n').encode()
                print("data sent to the client: ", data)
                conn.sendall(data)
            elif data.decode('utf-8').strip() == "s":
                # stop server
                break
            else:
                continue

            
            # if not data:
            #     break

