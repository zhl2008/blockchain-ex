#!/usr/bin/env python

'''
This module is designed to record and print the log info where the main program starts

'''
from utils import color
from config import *
import sys

class log():
    @staticmethod
    def _print(word):
        sys.stdout.write(word)
        sys.stdout.flush()
    
    @staticmethod
    def beauty(word):
	res = ''
	beauty_length = 75
	loop = len(word)/beauty_length
	for i in range(loop):
	    res += word[i*beauty_length:i*beauty_length+beauty_length] + "\n    "
	res += word[loop*beauty_length:]
	return res

    @staticmethod
    def my_log(msg,word):
        if log_into_file:
            raw_msg = "[+] %s\n" % word
            open(log_file,'ab').write(raw_msg)
        if log_into_console:
            log._print(msg)

    @staticmethod
    def info(word,debug_print=True):
        msg = "[+] %s\n" % color.green(word)
        if not debug_print:
            return
        log.my_log(msg,word)

    @staticmethod
    def warning(word,debug_print=True):
        msg = "[!] %s\n" % color.yellow(log.beauty(word))
        if not debug_print:
            return
        log.my_log(msg,word)

    @staticmethod
    def error(word,debug_print=True):
        msg = "[-] %s\n" % color.red(log.beauty(word))
        if not debug_print:
            return
        log.my_log(msg,word)

    @staticmethod
    def success(word,debug_print=True):
        msg = "[+] %s\n" % color.purple(log.beauty(word))
        if not debug_print:
            return
        log.my_log(msg,word)

    @staticmethod
    def query(word,debug_print=True):
        msg = "[?] %s\n" % color.underline(log.beauty(word))
        if not debug_print:
            return
        log.my_log(msg,word)

    @staticmethod
    def context(word,debug_print=True):
        msg = "%s\n" % (color.blue(word))
        if not debug_print:
            return
        log.my_log(msg,word)
