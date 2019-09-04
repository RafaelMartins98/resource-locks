#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle
import lock_pool

def bytesToList(msg_bytes):
    list = pickle.loads(msg_bytes)
    return list[-1]

def listToBytes(msg_to_convert):
    return pickle.dumps(msg_to_convert, -1)

class Skeleton:

    def __init__(self, resources, locks, blocked, time):
        self.servicoLista = []
        self.pool = lock_pool.lock_pool(resources, locks, blocked, time)

    def processMessage(self, msg_bytes):
        pedido = bytesToList(msg_bytes)
        resposta = []

        canLock = True

        if self.pool._y <= self.pool.stat_y():
            canLock = False
        try:
            if(len(pedido) > 2):
                client_id = int(pedido[1])
                resource_id = int(pedido[2])
            elif len(pedido) == 2:
                resource_id = int(pedido[1])

            if pedido == None or len(pedido) == 0:
                resposta.append("INVALID MESSAGE")
            else:
                resposta.append(pedido[0] + 1)
                if pedido[0] == 10:
                    if resource_id < 0 or resource_id > self.pool._n:
                        resposta.append(None)
                    else:
                        if canLock and self.pool.lock(resource_id, client_id, self.pool._t):
                            resposta.append(True)
                        elif not canLock and self.pool._locks[resource_id]._clientId == client_id:
                            self.pool.lock(resource_id, client_id, self.pool._t)
                            resposta.append(True)
                        else:
                            resposta.append(False)
                elif pedido[0] == 20:
                    if resource_id < 0 or resource_id > self.pool._n:
                        resposta.append(None)
                    else:
                        if self.pool.release(resource_id, client_id):
                            resposta.append(True)
                        else:
                            resposta.append(False)
                elif pedido[0] == 30:
                    if resource_id < 0 or resource_id > self.pool._n:
                        resposta.append(None)
                    else:
                        if self.pool.test_disabled(resource_id):
                            resposta.append("disable")
                        elif self.pool.test(resource_id):
                            resposta.append(True)
                        else:
                            resposta.append(False)
                elif pedido[0] == 40:
                    if resource_id < 0 or resource_id > self.pool._n:
                        resposta.append(None)
                    else:
                        resposta.append(self.pool.stat(resource_id))
                elif pedido[0] == 50:
                    resposta.append(self.pool.stat_y())
                elif pedido[0] == 60:
                    resposta.append(self.pool.stat_n())
                else:
                    resposta.append(None)
        except ValueError as v:
            resposta.append("INVALID COMMAND")

        return (listToBytes(resposta), str(self.pool))



