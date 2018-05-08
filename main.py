#!/usr/bin/env python

import os
import sys
import time
import hashlib
import base64
import threading
import config
from discovery import *
from logger import *
from blockchain import *
from message import *

def discovery_send():
    log.info('Starting host discovery...')
    d = discovery(broardcast_msg,broardcast_port)
    d.broadcast()

def discovery_receive():
    d = discovery(broardcast_msg,broardcast_port)
    d.receive()

def init_block():
    log.info('Initializing the block...')
    load_current_hash()
    log.info(str(config.blockchain_list),config.debug)
    load_current_balance()
    log.info(str(config.balance_list),config.debug)

def miner():
    log.info('Starting miner...')
    while True:
        b = block(prev_hash=config.global_prev_hash,height=config.global_height,difficulty=config.global_difficulty,address=config.pubkey)
        if(b.generate()):
            b.update()

def msg_generator():
    log.info('Receiving message...')
    m = message("",config.message_port)
    m.recv()

def msg_consumer():
    log.info('Handling message...')
    m = message("",config.message_port)
    m.handle()

def block_broadcast():
    log.info('Broadcasting block status...')
    m = message("",config.message_port)
    while True:
        m.reply(int(config.global_height) -1)
        time.sleep(config.broadcast_time_span)
        m.send_all()

def watch_dog():
    global thread_array
    while True:
        time.sleep(5)
        log.warning('######  thread status ######')
        for my_thread in thread_array:
            log.warning(my_thread.name + ' => ' + 'Alive' if my_thread.isAlive() else 'Dead')
        log.warning('######  status ends  ######')
        time.sleep(55)

if __name__ == "__main__":


    # start blockchain
    init_block()

    # start threads
    t1 = threading.Thread(target=discovery_send,name='discovery_send')
    t2 = threading.Thread(target=discovery_receive,name='discovery_receive')
    t3 = threading.Thread(target=miner,name='miner')
    t4 = threading.Thread(target=msg_generator,name='msg_generator')
    t5 = threading.Thread(target=msg_consumer,name='msg_consumer')
    t6 = threading.Thread(target=block_broadcast,name='block_broadcast')
    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    t5.setDaemon(True)
    t6.setDaemon(True)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    
    thread_array = [t1,t2,t3,t4,t5,t6]
    t7 = threading.Thread(target=watch_dog,name='watch_dog')
    t7.setDaemon(True)
    t7.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        log.error('Killed by user')
        sys.exit()


