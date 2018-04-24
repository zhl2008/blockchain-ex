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


    def generate(self):
        

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
        flag_2 = verify_diff(hashlib.sha1(str(output)).hexdigest(),self.difficulty)
        return (flag_1 and flag_2) 







def init_blockchain():
    pass


def get_blance(address):
    pass


