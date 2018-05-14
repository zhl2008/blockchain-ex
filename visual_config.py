#!/usr/bin/env python

'''
This script is designed to provide the global data/queue for this program

'''


import Queue

###### basic config #########


host_list = []
debug = True
connection_timeout = 3

###########################



####### log config ##########

log_into_file = True

log_into_console = True
############################


###### broardcast config #######

broardcast_port = 8888
broardcast_msg = 'haozigege666'
max_host_num = 10
broadcast_time_span = 5


###############################

##### message config ##########

message_port = 6666
message_queue = Queue.Queue()

###############################


#### ip config ################

import socket
import os
my_name = socket.getfqdn(socket.gethostname(  ))
my_addr = socket.gethostbyname(my_name)

##############################


#### blockchain config #########

block_updated = 0
miner_sleep_time = 0.1
balance_list = {}
blockchain_list = {}
global_prev_hash = ''
global_height = ''
global_difficulty = 'haozigege'
miner_reward = 100


################################


