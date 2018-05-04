#!/usr/bin/env python

'''
This tool is designed to send the test messages to the blockchain nodes, and try to observe the reaction of the nodes
'''

import config
from message import *

m = message("",config.message_port)
m.request(2)
m.send('172.17.0.2')
