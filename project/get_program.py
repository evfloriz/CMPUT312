#!/usr/bin/python

import socket
import os
from time import sleep

# This class handles the client side of communication. It has a set of predefined messages to send to the server as well as functionality to poll and decode data.
class Client:
    def __init__(self, host, port):
        # We need to use the ipv4 address that shows up in ipconfig in the computer for the USB. Ethernet adapter handling the connection to the EV3
        print("Setting up client\nAddress: " + host + "\nPort: " + str(port))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect((host, port))                               
        
    # Block until a message from the server is received. When the message is received it will be decoded and returned as a string.
    # Output: UTF-8 decoded string containing the instructions from server.
    def pollData(self):
        print("Waiting for Data")
        data = self.s.recv(128).decode("UTF-8")
        print("Data Received")
        return data
    
    # Sends a message to the server letting it know that the program was received
    def sendDone(self):
        self.s.send("DONE".encode("UTF-8"))

    def close(self):
        self.s.close()


def main():
    # Automatically run file after downloading - not working currently
    autorun = False
    
    host = "172.17.0.1"
    port = 9999

    client = Client(host, port)

    # Receive program name from server
    programName = client.pollData()
    client.sendDone()

    # Receive program from server
    program = client.pollData()
    client.sendDone()
    
    # Create program file
    file = open(programName, "w")
    file.write(program)

    sleep(1)
    
    # Doesn't work currently
    #if (autorun):
    #    os.system("python3 " + programName)


if __name__ == '__main__':
    main()