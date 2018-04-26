#!/usr/bin/env python

'''

This module create the functions concerning with blockchain, such as generate, update or delete


'''

import rsa
from logger import *
from config import *

class block():
    '''

    this class is utilized to create,verify the blocks, when the 
    block is created, the nonce and signature are not supposed to provide,
    it will generate automatically. And during the period of calculating the new block, if a new
    block is generated, we should regenerate meta information of the block and continue 
    generating.

    '''
    def __init__(self,prev_hash,height,difficulty,address,amount,signature="",nonce=""):
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.address = address
        self.amount = amount
        self.balance = get_balance(address)
        self.signature = signature
o

    def generate(self):
        '''
        we try to generate a new block, which meet the requirement of difficulty
        by chaning the nonce. The hash function we implement here is SHA-256, 
        which is at the length of 32 bytes. Each time brefore we start to calculate the hash
        , we need to check the status that whether we need to update the meta data of the block
        , if the meta info is changed, stop the generate process and start a new one

        '''
        # signature should be updated according to your address, sign with your privkey
        self.signature = ''
        # $$$$$ to be replaced laterly
        self.nonce = '$$$$$'
        template = str(self.output())
        seed = 0
        while True:
            self.nonce = hashlib.sha256(str(seed)).hexdigest()
            my_block = template.replace('$$$$$',self.nonce)
            if verify_diff(hashlib.sha256(my_block)):
                # find a new block, stop, nonce has been updated
                return self.output()
            if block_updated:
                log.info('Meta data has been updated!')
                # if the meta info has been updated, stop, and then restart
                block_updated = 0
                return {}
            seed += 1
            time.sleep(miner_sleep_time)


        

    def output(self):
        output = {}
        output['pre_hash'] = self.prev_hash
        output['nonce'] = self.nonce
        output['height'] = self.height
        output['difficulty'] = self.difficulty
        output['transaction'] = [{},]
        output['transaction'][0]['input'][0] = {"address":"god","amount":"100"}
        output['transaction'][0]['input'][1] = {"address":self.address,"amount":self.balance}
        output['transaction'][0]['output'] = {"address":self.address}
        output['transaction'][0]['signature'] = self.signature
        return output

    def verify(self):
        ''' 
        since we have not implement the full version of the blockchain, but we may want to verify
        some of the transaction in later work, so here I preserve the sample implementation of 
        signature verification to notice myself of that
        '''

        flag_1 = rsa.verify('haozigege',self.signature.decode('hex'),rsa.PublicKey(int(address, 16), 65537))
        flag_2 = verify_diff(hashlib.sha256(str(output)).hexdigest(),self.difficulty)
        return (flag_1 and flag_2) 

def init_blockchain():
    '''
    to init the blockchain, the following steps should be done:
    1. get current block height
    2. if the height is 0, then generate the genesis block
    3. establish the index of the blockchain according to the filename of blocks

    '''
    blockchain_dir = 'blockchain/%s/' %my_addr 
    for tmp in os.walk(blockchain_dir):
        pass
    # the filenames are stored in the tmp[0][2]
    filenames = tmp[0][2]
    blockchain_height = len(filenames) - 1
    if blockchain_height == 0:
        generate_genesis_block()



def generate_genesis_block():
    '''

    the genesis block
    
    '''


    blockchain_dir = 'blockchain/%s/' %my_addr


    b = block(
    

def get_balance(address):
    pass

def verify_diff(hash,difficulty):
    pass

