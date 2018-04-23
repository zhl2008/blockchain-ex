#!/usr/bin/env python

import sys
from logger import log
from config import *
from discovery import *
from message import *
import threading

def test1():
    log.info('haozigege')
    log.success('666666')
    log.warning('warning')
    log.error('error')

def test2():
    b = discovery(broardcast_msg,broardcast_port)
    b.receive()

def test3():
    b = discovery(broardcast_msg,broardcast_port)
    b.broadcast()

def test4():
    m = message('{"message":"hello world!"}',message_port)
    m.recv()

def test5():
    m = message('{"message":"hello world!"}',message_port)
    while True:
        m.send_all()
        time.sleep(10)

test1()
t2 = threading.Thread(target=test2)
t2.setDaemon(True)
t2.start()

t3 = threading.Thread(target=test3)
t3.setDaemon(True)
t3.start()

t4 = threading.Thread(target=test4)
t4.setDaemon(True)
t4.start()

t5 = threading.Thread(target=test5)
t5.setDaemon(True)
t5.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    log.error('Killed by user')
    sys.exit()






