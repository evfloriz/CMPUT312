#!/usr/bin/python

import socket
from time import sleep
from queue import Queue

# This class handles the Server side of the comunication between the laptop and the brick.
class Server:
    def __init__(self, host, port, queue):
        # Setup server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # We need to use the ip address that shows up in ipconfig for the usb ethernet adapter that handles the comunication between the PC and the brick
        print("Setting up Server\nAddress: " + host + "\nPort: " + str(port))
        
        serversocket.bind((host, port))
        # Queue up to 5 requests
        serversocket.listen(5) 
        self.cs, addr = serversocket.accept()
        print ("Connected to: " + str(addr))

        # Setup queue
        self.queue = queue

    # Send program to client
    def sendProgram(self, program_name):
        # Open program and read as string
        file = open(program_name, "r")
        
        
        # Send program name to client
        print("Sending name: " + program_name + " to robot.")
        self.cs.send(program_name.encode("UTF-8"))
        # Waiting for the client (ev3 brick) to let the server know that it has received name
        reply = self.cs.recv(128).decode("UTF-8")
        self.queue.put(reply)

        # Send program to client in 1024 byte chunks
        i = 0
        while True:

            program_chunk = str(file.read(1024))
            if not program_chunk:
                break

            print("Sending program chunk: " + str(i) + " to robot.")
            self.cs.send(program_chunk.encode("UTF-8"))
            # Waiting for the client (ev3 brick) to let the server know that it has received data
            reply = self.cs.recv(1024).decode("UTF-8")
            self.queue.put(reply)

            i += 1
        
        # Send termination
        self.cs.send("EXIT".encode("UTF-8"))

    def close(self):
        self.cs.close()


def main():
    host = "172.17.0.1"
    port = 9999
    queue = Queue()
    
    # Create server object
    server = Server(host, port, queue)

    # Send program to client
    program_name = "test.py"
    server.sendProgram(program_name)

    # Print response
    response = queue.get()
    print("Received: " + response)

    sleep(1)
        

if __name__ == '__main__':
    main()
