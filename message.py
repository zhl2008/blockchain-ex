#!/usr/bin/env python

'''

This module is designed to send, receive and parse the message from the peers. and change the status of the 
blockchain and this program

'''

import socket
from config import *
from logger import *


class message(object):
    def __init__(self,msg,msg_port):
        self.msg = msg
        self.msg_port = msg_port
    
    def send(self,peer_address):
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((peer_address,self.msg_port))
        s1.send(self.msg)

    def recv(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s2.bind(('0.0.0.0',int(self.msg_port))) 
        log.info('Listening for message at %s' % (str(s2.getsockname())))
        while True:
            s2.listen(5)
            ss, address = s2.accept()
            data = ss.recv(65535)
            log.info('Receive data: %s' % data, True)
            message_queue.put({'data':data,'address':address[0]})

    def send_all(self):
        log.info('Broardcasting message...')
        for host in host_list:
            self.send(host[0])
    
        



