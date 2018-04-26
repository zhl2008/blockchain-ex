#!/usr/bin/env python

'''
This script is designed to provide the global data/queue for this program

'''


import Queue

###### basic config #########


host_list = []
debug = True

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
broadcast_time_span = 10

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
    os.system('touch blockchain/%s/meta'%my_addr)

##############################

#### key config ###############

from tools.generate_key import *

admin_pubkey = '9765869799823383359622359754181812625324231512026077082381651287440341672379839014722257386111774035152974440781781367383855004017506803031463021493485593'
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

blockchain_length = 0
last_block_hash = ''
block_updated = 0
miner_sleep_time = 1
block_height = 0
blockchain_dir = 'blockchain/%s/' %my_addr
blockinfo = {}
balance_list = {}
blockchain_list = {}
global_prev_hash = ''
global_height = ''
global_difficulty = 'haozigege'
print 'import config'
miner_reward = 100
################################


