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

#### blockchain config #########

blockchain_length = 0
last_block_hash = ''

################################



