#!/usr/bin/env python

import sys
from logger import log
import config
from discovery import *
from message import *
import threading
from blockchain import *

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

def test6():
    pass

def test7():
    load_current_hash()
    log.info(str(blockchain_list))
    load_current_balance()
    log.info(str(balance_list))
    b = block(prev_hash=config.global_prev_hash,height=config.global_height,difficulty=config.global_difficulty,address=config.pubkey)
    b.generate()

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

test6()
test7()

try:
    while True:
        pass
except KeyboardInterrupt:
    log.error('Killed by user')
    sys.exit()






