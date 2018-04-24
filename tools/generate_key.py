#!/usr/bin/env python

'''

This tool is designed to generate random pubickey and privkey (length 256 bit)

'''
import pickle
import rsa

def generate_key():
    pubkey, privkey = rsa.newkeys(256)
    pubkey = pubkey.n
    privkey = pickle.dumps(privkey).encode('hex')
    return str(pubkey),privkey

if __name__ == '__main__':
    print generate_key()
