#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from lock_skel import Skeleton
import sock_utils as su
import select as sel
import pickle as p
import sys
import struct
import socket

if(len(sys.argv) != 6):
    print("Expected input: python lock_server.py <server-port> <resource-number> <lock-number> <blocked-resources> <time>")
    sys.exit()

try:
    PORT = int(sys.argv[1])
    RESOURCES = int(sys.argv[2])
    LOCKS = int(sys.argv[3])
    BLOCKED = int(sys.argv[4])
    TIME = int(sys.argv[5])
except:
    print("Input must be of type Integer")
    sys.exit()

skel = Skeleton(RESOURCES, LOCKS, BLOCKED, TIME)
sock = su.create_tcp_server_socket("", PORT, 1)


SocketList = [sock]



while True:
    try:
        R, W, X = sel.select(SocketList, [], [])
        for sckt in R:
            if sckt is sock:
                (conn_sock, addr) = sock.accept()
                print("### CONNECTED TO: ###")
                print("ADDRESS: ", addr[0])
                print("PORT: ", str(addr[1]))
                SocketList.append(conn_sock)
            else:
                size_bytes = su.receive_all(sckt, 4)

                if size_bytes:
                    skel.pool.clear_expired_locks()
                    skel.pool.disable_expired_resources()

                    size = struct.unpack("!i", size_bytes)[0]

                    #receber mensagem em bytes
                    resp, pool = skel.processMessage(su.receive_all(sckt, size))

                    #enviar resposta

                    size_mens = struct.pack("!i", len(resp))
                    sckt.sendall(size_mens)
                    sckt.sendall(resp)
                    print(pool)
                else:
                    sckt.close()
                    SocketList.remove(sckt)
                    print('The Client has finised the connection')
    except (socket.error, socket.herror):
        print("\nError with the socket.")
        conn_sock.close()
    except p.UnpicklingError:
        print('Unkown message format!')
        SocketList.remove(sckt)
        conn_sock.close()
    except Exception as e:
        print(e)
        print('Socket closed!')
        conn_sock.close()