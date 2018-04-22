#!/usr/bin/env python

'''
this module is used to detect the peer nodes in the subnet, and it trys to sent the heart beat package peer 10s (default config)
'''
import socket
from logger import *
from config import *
import time

class discovery():
    def __init__(self,message,port,host_list=[]):
        self.host_list = host_list
        self.message = message 
        self.port = port
        # send socket
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # recv socket
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def broadcast(self):
        log.info('Sending broardcast...')
        network = '<broadcast>'
        while True:
            self.s1.sendto(str(self.message).encode('utf-8'), (network, self.port))
            time.sleep(broadcast_time_span)

    def receive(self):
        self.s2.bind(('', self.port))
        log.info('Listening for broadcast at %s' % str(self.s2.getsockname()))
        while True:
            data, address = self.s2.recvfrom(65535)
            if data == self.message:
                # limit the number of the peers to connect to (using tcp)
                if len(self.host_list) < max_host_num and address not in self.host_list:
                    self.host_list.append(address)
                    log.info('Find a peer: %s'% str(address))

