#!/usr/bin/env python

from utils.log import Log


def test1():
    log = Log()
    log.info('haozigege')
    log.success('666666')
    log.warning('warning')
    log.error('error')

test1()
