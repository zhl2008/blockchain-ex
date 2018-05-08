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

log_file = './logs/sys.log'

log_into_file = True

log_into_console = True
############################


###### broardcast config #######

broardcast_port = 8888
broardcast_msg = 'haozigege666'
max_host_num = 2
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
if not os.path.exists('blockchain/%s'%my_addr):
    os.mkdir('blockchain/%s'%my_addr)

##############################

#### key config ###############

from tools.generate_key import *

admin_pubkey = 'ba7693c5c1f80bd85c0ede83713f491c2b9a72039f77683495155e66e6dddd2f1c107c6b1a5b5419aa1324cfe8fb61afe892bd3250760e9255594090b39a0019'
if not os.path.exists('key/%s'%my_addr):
    os.mkdir('key/%s'%my_addr)
    pubkey,privkey = generate_key()
    open('key/%s/mykey'%my_addr,'w').write(pubkey + "\n" + privkey)
else:
    pubkey,privkey = open('key/%s/mykey'%my_addr).readlines()
    pubkey = pubkey.strip()
    privkey = privkey.strip()

###############################


#### blockchain config #########

block_updated = 0
miner_sleep_time = 0.03
blockchain_dir = 'blockchain/%s/' %my_addr
balance_list = {}
blockchain_list = {}
global_prev_hash = ''
global_height = ''
global_difficulty = 'haozigege'
miner_reward = 100


################################


