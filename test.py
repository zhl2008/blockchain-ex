#!/usr/bin/env python

from logger import log
from config import *
from discovery import *

def test1():
    log.info('haozigege')
    log.success('666666')
    log.warning('warning')
    log.error('error')

def test2():
    b = discovery(broardcast_msg,broardcast_port,[])
    #b.broadcast()
    b.receive()

test1()
test2()
