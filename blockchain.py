#!/usr/bin/env python

'''

This module create the functions concerning with blockchain, such as generate, update or delete


'''

import rsa
from logger import *
import config 
import json
import pickle
import hashlib
import time

class block():
    '''

    this class is utilized to create,verify the blocks, when the 
    block is created, the nonce and signature are not supposed to provide,
    it will generate automatically. And during the period of calculating the new block, if a new
    block is generated, we should regenerate meta information of the block and continue 
    generating.

    '''
    def __init__(self,prev_hash,height,difficulty,address,amount=config.miner_reward,signature="",nonce="",data="haozigege",time=int(time.time())):
        self.prev_hash = prev_hash
        self.height = height
        self.nonce = nonce
        self.time = str(time)
        self.difficulty = difficulty
        self.address = address
        self.amount = amount
        self.balance = get_balance(address)
        # if the signature is blank, and the address is from our own server, create the signature
        if not signature and address==config.pubkey:
            self.signature = rsa.sign(address + data,pickle.loads(config.privkey.decode('hex')),'SHA-256').encode('hex')
        else:
            self.signature = signature
        self.data = data

    def generate(self):
        '''
        we try to generate a new block, which meet the requirement of difficulty
        by chaning the nonce. The hash function we implement here is SHA-256, 
        which is at the length of 32 bytes. Each time brefore we start to calculate the hash
        , we need to check the status that whether we need to update the meta data of the block
        , if the meta info is changed, stop the generate process and start a new one

        '''
        # $$$$$ to be replaced laterly
        self.nonce = '$$$$$'
        self.time = '*****'
        self.difficulty = update_difficulty(config.global_difficulty)
        template = json.dumps(self.output())
        seed = 0
        while True:
            self.nonce = hashlib.sha256(str(seed)).hexdigest()
            self.time = str(int(time.time()))
            my_block = template.replace('$$$$$',self.nonce).replace('*****',self.time)
            my_hash = hashlib.sha256(my_block).hexdigest()
            if verify_diff(my_hash,self.difficulty):
                # find a new block, stop, nonce has been updated
                log.warning('One block has been found!')
                print my_hash,self.difficulty
                res = self.output()
                log.context(json.dumps(res),config.debug)
                return res
            if config.block_updated:
                log.warning('Meta data has been updated!')
                # if the meta info has been updated, stop, and then restart
                config.block_updated = 0
                return {}
            seed += 1
            time.sleep(miner_sleep_time)

    def is_next(self):
        '''
        judge whether a block is next to the latest block, if so, return true
        '''
        #print self.prev_hash,config.global_prev_hash
        if self.prev_hash == config.global_prev_hash:
            return True
        return False

    def update(self):
        '''
        if the new block is next to our latest block, then using it to update our blockchain
        the steps of updation:
        1. save the new block to file
        2. update the balance_list, blockchain_list and some other global variables
        3. if the miner is from other host, then update the block_updated to 1
        '''
        if not self.is_next():
            log.error(self.prev_hash,True)
            log.error(config.global_prev_hash,True)
            log.error('Hash mismatch!')
            return
        log.info('Updating the blocks...')
        res = self.output()
        my_hash = hashlib.sha256(json.dumps(res)).hexdigest()
        log.context(json.dumps(res),True)
        filename = config.blockchain_dir + str(self.height) + '-' + my_hash
        open(filename,'w').write(json.dumps(res))

        balance_addr = res['transaction'][0]['input'][1]['address']
        balance = res['transaction'][0]['input'][1]['amount']
        config.balance_list[balance_addr] = balance + config.miner_reward

        config.blockchain_list[str(self.height)] = my_hash
        config.global_prev_hash = my_hash
        config.global_height = self.height + 1
        config.global_difficulty = self.difficulty

        if not self.address==config.pubkey:
            # not our own address, so this block is received from other host
            config.block_updated = 1

    def output(self):
        output = {}
        output['prev_hash'] = self.prev_hash
        output['nonce'] = self.nonce
        output['height'] = self.height
        output['difficulty'] = self.difficulty
        output['time'] = self.time
        output['transaction'] = [{},]
        output['transaction'][0]['input'] = [{},{}]
        output['transaction'][0]['input'][0] = {"address":"god","amount":config.miner_reward}
        output['transaction'][0]['input'][1] = {"address":self.address,"amount":self.balance}
        output['transaction'][0]['output'] = {"address":self.address}
        output['transaction'][0]['signature'] = self.signature
        output['transaction'][0]['data'] = self.data
        return output

    def verify(self):
        ''' 
        since we have not implement the full version of the blockchain, but we may want to verify
        some of the transaction in later work, so here I preserve the sample implementation of 
        signature verification to notice myself of that
    
        sign = rsa.sign => (config.pubkey + data)

        '''
        #print json.dumps(self.output())
        #print hashlib.sha256(json.dumps(self.output())).hexdigest()
        #print self.difficulty
        flag_1 = rsa.verify(self.address + self.data,self.signature.decode('hex'),rsa.PublicKey(int(self.address, 16), 65537))
        flag_2 = verify_diff(hashlib.sha256(json.dumps(self.output())).hexdigest(),self.difficulty)
        return (flag_1 and flag_2) 

def init_blockchain():
    '''
    to init the blockchain, the following steps should be done:
    1. get current block height
    2. if the height is 0, then generate the genesis block
    3. establish the index of the blockchain according to the filename of blocks

    '''
    load_current_hash()
    load_current_balance()

def load_current_hash():
    '''
    generate the maps from height to hash
    '''
    log.info('Loading current hash...')
    for tmp in os.walk(config.blockchain_dir):
        pass
    # the filenames are stored in the tmp[0][2]
    filenames = tmp[2]
    blockchain_height = len(filenames)
    if blockchain_height == 0:
        generate_genesis_block()
        config.blockchain_list['1'] = config.global_prev_hash
        return
    for filename in filenames:
        if filename!='meta':
            height,my_hash = filename.split('-')
            config.blockchain_list[height] = my_hash
    tmp = sorted(config.blockchain_list.items(),key=lambda x:int(x[0]))
    last_block = tmp[-1]
    log.context(str(last_block),True)
    config.global_prev_hash = last_block[1]
    config.global_height = int(last_block[0]) + 1 
    last_block_filename = blockchain_dir + last_block[0] + '-' + last_block[1]
    last_block_info = json.loads(open(last_block_filename,'r').read())
    difficulty = last_block_info['difficulty']
    config.global_difficulty = difficulty

def load_current_balance():
    '''
    load current balance from files
    '''
    for height,my_hash in sorted(config.blockchain_list.items(),key=lambda x:int(x[0]),reverse=True):
        filename = config.blockchain_dir + height + '-' + my_hash
        block = json.loads(open(filename,'r').read())
        transaction = block['transaction']
        address = transaction[0]['output']['address']
        if address not in balance_list:
            balance = int(transaction[0]['input'][0]['amount']) + int(transaction[0]['input'][1]['amount'])
            config.balance_list[address] = balance


def load_block(height):
    '''
    load a block at the specific height, return with json.loads(file_content)
    '''
    my_hash = blockchain_list[str(height)]
    filename = config.blockchain_dir + str(height) + '-' + my_hash
    block = json.loads(open(filename,'r').read())
    return block

def generate_genesis_block():
    '''

    the genesis block
    
    '''
    
    prev_hash = '0000000000000000000000000000000000000000000000000000000000000000'

    nonce = '0000000000000000000000000000000000000000000000000000000000000000'
    difficulty = hex(int(0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff/1000))[2:-1]
    height = 1
    data = 'The Times 24/4/2018 Hencecoin start'
    address = config.admin_pubkey
    # the time in the genesis block, must be the same
    time = 1525772773
    b = block(prev_hash=prev_hash,height=height,difficulty=difficulty,address=address,nonce=nonce,data=data,time=time)
    res = b.output()
    log.info('Generate genesis block...')
    log.context(json.dumps(res),True)
    my_hash = hashlib.sha256(json.dumps(res)).hexdigest()
    filename = '1' + '-' +  my_hash
    blockchain_filename = config.blockchain_dir + filename

    open(blockchain_filename,'w').write(json.dumps(res))
    config.global_prev_hash = my_hash
    config.global_height = height + 1
    config.global_difficulty = difficulty


def update_difficulty(difficulty):
    '''
    to update the difficulty according to the former calculation time
    we use the nodes which has a gap of five blocks as our input, and using the timestamp to
    calculate and update the difficulty 
    for example, block 2 <-> block 7
    '''

    # global height < 8 , no need to update
    if config.global_height <8:
        return difficulty
    update_height_higher = config.global_height - 1
    update_height_lower = config.global_height - 6
    higher_block = load_block(update_height_higher)
    lower_block = load_block(update_height_lower)
    time_span = int(higher_block['time']) - int(lower_block['time'])
    old_difficulty = higher_block['difficulty']
    print time_span
    print old_difficulty
    difficulty = hex(int(int(old_difficulty,16) * (time_span)/ 300))[2:-1]
    print hex(int(int(old_difficulty,16) * (time_span) /300))

    log.warning('Difficulty updated: %s'%difficulty,True)
    
    return difficulty

def get_balance(address):
    '''
    get user balance from the balance_list
    '''
    if address in balance_list:
        return balance_list[address]
    else:
        return 0

def verify_diff(my_hash,difficulty):
    #log.context(difficulty)
    #log.context(my_hash)
    if int(my_hash,16) <= int(difficulty,16):
        log.context(my_hash,True)
        return True
    else:
        return False


