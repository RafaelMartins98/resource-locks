#!/usr/bin/python
# -*- coding: utf-8 -*-

from net_client import server as client
import traceback
import sys

class Stub:

    """
        Operation structure: <COMMAND>: (<CODE>, <NARGS>)
    """
    operationsCodes = {
        "LOCK": (10, 2),
        "RELEASE": (20, 2),
        "TEST": (30, 2),
        "STATS": (40, 2),
        "STATS-Y": (50, 1),
        "STATS-N": (60, 1)
    }

    def __init__(self):
        self.client = None
        self.operations = []

    def connect(self, host, port):
        try:
            self.client = client(host, port)
            self.client.connect()
        except:
            print("Error connecting the server.")
            sys.exit()


    def disconnect(self):
        if self.client:
            self.client.close()

    def append(self, element):
        try:
            self.operations.append(element)
            obj = self.client.send_receive(self.operations)
            return 'Answer: %s' % obj[0] if len(obj) == 1 else 'Answer: %s' % str(obj)
        except Exception as e:
            print("Exception caught with the following traceback: " + str(e))
            traceback.print_exc()


    def list(self):
        return "Operations list :{}".format(self.operations)

    def clear(self):
        self.operations.clear()