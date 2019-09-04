#!/usr/bin/python
# -*- coding: utf-8 -*-

from lock_stub import Stub
import sys
import socket

if(len(sys.argv) != 4):
    print("Expected input: python lock_client.py <server-ip> <server-port> <client-id>")
    sys.exit()

HOST = sys.argv[1]
PORT = int(sys.argv[2])
CLIENT_ID = sys.argv[3]

print("###### Properties ######")
print("Host: " + HOST)
print("Port: " + str(PORT))
print("ClientId: " + CLIENT_ID)

try:
    stub = Stub()
    stub.connect(HOST, PORT)

    while True:
        msg = str(input('Command > '))

        if msg.lower() == 'exit':
            exit()
        params = msg.split(" ")

        while params[0] not in Stub.operationsCodes.keys() or len(params) != Stub.operationsCodes[params[0]][1]:
            print("Invalid Command")
            msg = str(input('Command > '))
            if msg.lower() == 'exit':
                exit()
            params = msg.split(" ")

        if len(params) > 1:
            appendStatements = [Stub.operationsCodes[params[0]][0], CLIENT_ID, params[1]]
        else:
            appendStatements = [Stub.operationsCodes[params[0]][0], CLIENT_ID]

        resp = stub.append(appendStatements)
        print("Received: " + str(resp))
        
except (socket.error, socket.herror):
        print("\Error with socket.")
except Exception as e:
        print(e)
        print('Socket closed!')
