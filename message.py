#!/usr/bin/env python

'''

This module is designed to send, receive and parse the message from the peers. and change the status of the 
blockchain and this program

'''

import socket
from config import *
import config
from logger import *
from blockchain import *
import json

class message(object):
    def __init__(self,msg,msg_port):
        self.msg = msg
        self.msg_port = msg_port
    
    def send(self,peer_address):
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.settimeout(config.connection_timeout)
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
            log.context('Receive data: %s' % data, True)
            config.message_queue.put({'data':data,'address':address[0]})

    def handle(self):
        '''
        we have these messages to be handled:
        1. block request
        2. block reply
        3. legacy_reply
        4. admin

        '''

        while True:
            if not config.message_queue.empty():
                log.info('Handing incoming message...',config.debug)
                raw_msg = config.message_queue.get()
                my_msg = json.loads(raw_msg['data'])
                self.ip_address = raw_msg['address']
                method = my_msg['method']
                self.height = my_msg['height']
                self.msg = json.loads(my_msg['content'])
                log.context(my_msg['content'],config.debug)
                func = getattr(self,'handle_' + method)
                func()

    def handle_legacy_reply(self):
        ''' 
        when receiving the message of legacy reply, do not reply, just be silent 
        '''
        pass

    def handle_block_request(self):
        '''
        to handle the block request, we just get the block request, then using the 
        reply function
        '''
        log.info('Handling block request...',True)
        height = self.height
        self.reply(height)
        self.send(self.ip_address)

    def handle_global_request(self):
        '''
        this function is used to communicate with the terminal to be presented
        '''
        log.info('Handling globakl request...',True)
        extra = {}
        extra['host_list'] = config.host_list
        extra['msg_queue_length'] = str(config.message_queue.qsize())
        extra['address'] = config.pubkey
        extra['local_host'] = config.my_addr
        extra['global_height'] = config.global_height
        extra['blockchain_list'] = config.blockchain_list
        extra['global_difficulty'] = config.global_difficulty
        extra['balance_list'] = config.balance_list
        extra['global_pre_hash'] = config.global_prev_hash
        
        extra = json.dumps(extra)
        msg = {"method":"global_reply", "height":self.height,"content":extra}
        self.msg = json.dumps(msg)
        self.send(self.ip_address)
        

    def handle_block_reply(self):
        '''
        this is a very important part in the p2p network to reach to consensus:

        1. if the block height of the reply equals to global_block_height, then we 
        try to check the prev_hash of the block, if hash matches, then we accept
        the block, and update the blockchain using the message.update method; if 
        the hash mismatches, stop the miner. And we may ask for an elder block until
        the prev_hash matches, all of the blocks are stored locally, and we 
        initialize the whole block chain

        2. if the block height higher than the global_block_height, then we send a 
        block request at the height of the global_block_height

        3. if the block height is lowwer than that of the global_block_height,
        just ignore it
        '''
        log.info('Handling block reply...')
        height = self.msg['height']
        prev_hash = self.msg['prev_hash']
        difficulty = self.msg['difficulty']
        address = self.msg['transaction'][0]['input'][1]['address']
        amount = self.msg['transaction'][0]['input'][0]['amount']
        signature = self.msg['transaction'][0]['signature']
        nonce = self.msg['nonce']
        time = self.msg['time']
        data = self.msg['transaction'][0]['data']
        log.info(str(config.global_height)+"|"+str(height),True)

        if config.global_height == height:
            # hash matches
            if config.global_prev_hash == prev_hash:
                log.info('Receiving next block...')
                b = block(prev_hash=prev_hash,height=height,difficulty=difficulty,\
                        address=address,amount=amount,signature=signature,\
                        nonce=nonce,data=data,time=time)
                if(b.verify()):
                    b.update()
            # if hash mismatches, we ask for the elder block
            else:
                config.block_updated = 1
                log.warning('Receiving elder block...')

                # update the balance
                log.warning('Updating the balance')
                filename = config.blockchain_dir + str(config.global_height-1) + '-' + config.global_prev_hash
                old_block = json.loads(open(filename,'r').read())
                old_address = old_block['transaction'][0]['input'][1]['address']
                config.balance_list[old_address] -= miner_reward

                # you need to delete the elder block file
                log.warning('Removing elder block...')
                os.system('rm %s'%(filename))
                config.global_height -= 1
                config.global_prev_hash = blockchain_list[str(config.global_height-1)]
                config.global_difficulty = update_difficulty(config.global_difficulty)
                

        elif config.global_height < height:
            self.request(config.global_height)
            self.send(self.ip_address)
        elif config.global_height-1 == height:
            pass
        else:
            # if we do nothing, some of the nodes are too stubborn to keep their own
            # records
            self.reply(height + 1)
            self.send(self.ip_address)
        
    def global_request(self,height):
        extra = json.dumps({"extra":"helloworld"})
        msg = {"method":"global_request", "height":height,"content":extra}
        self.msg = json.dumps(msg)
        log.info("This is global request")
        log.context(self.msg,config.debug)

    def request(self,height):
        extra = json.dumps({"extra":"helloworld"})
        msg = {"method":"block_request", "height":height,"content":extra}
        self.msg = json.dumps(msg)
        log.info('This is request')
        log.context(self.msg,config.debug)

    def reply(self,height):
        block_hash = config.blockchain_list[str(height)]
        block_filename = config.blockchain_dir + str(height) + '-' + block_hash
        # the file may be deleted, so, we would better using os.path.exists first
        if not os.path.exists(block_filename):
            return self.legacy_reply(height)
        content = open(block_filename).read()
        msg = {"method":"block_reply","height":height}
        msg["content"] = content
        self.msg = json.dumps(msg)
        log.info('This is reply')
        log.context(self.msg,config.debug)

    def legacy_reply(self,height):
        extra = json.dumps({"extra":"do not reply"})
        msg = {"method":"legacy_reply","height":height,"content":extra}
        self.msg = json.dumps(msg)
        log.info('This is legacy reply')
        log.context(self.msg,config.debug)

    def admin(self,method):
        method = json.dumps({"method":method})
        msg = {"method":"admin", "height":height,"content":method}
        self.msg = json.dumps(msg)
        
    def send_all(self):
        log.info('Broardcasting message...')
        for i in range(len(config.host_list)):
            host = config.host_list[i][0]
            try:
                self.send(host)
            except Exception,e:
                log.error(str(e))
                #if error occurs, remove the host from the host_lists
                del config.host_list[i]
                # if u don't return, there will be a list-out-of-range-error due to 
                # the deletion above, we can just stop this turn of broadcast, it 
                # doesn't hurt
                return
    
        



