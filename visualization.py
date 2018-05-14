# coding: utf-8
import sys
import time
import curses
import time
import threading
import socket
from visual_config import *
import visual_config
import json

class discovery():
    def __init__(self,message,port):
        self.message = message 
        self.port = port
        # send socket
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # recv socket
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def broadcast(self):
        #log.info('Sending broardcast...')
        network = '<broadcast>'
        while True:
            self.s1.sendto(str(self.message).encode('utf-8'), (network, self.port))
            time.sleep(broadcast_time_span)

    def receive(self):
        self.s2.bind(('', self.port))
        while True:
            data, address = self.s2.recvfrom(65535)
            if data == self.message:
                # limit the number of the peers to connect to (using tcp)
                if not address[0]==my_addr  and len(host_list) < max_host_num and address not in host_list:
                    host_list.append(address)

class message(object):
    def __init__(self,msg,msg_port):
        self.msg = msg
        self.msg_port = msg_port
    
    def send(self,peer_address):
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.settimeout(visual_config.connection_timeout)
        s1.connect((peer_address,self.msg_port))
        s1.send(self.msg)

    def recv(self):
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s2.bind(('0.0.0.0',int(self.msg_port)))
        while True:
            s2.listen(5)
            ss, address = s2.accept()
            data = ss.recv(65535)
            visual_config.message_queue.put({'data':data,'address':address[0]})

    def handle(self):
        '''
        we have these messages to be handled:
        1. block request
        2. block reply
        3. legacy_reply
        4. admin
        5. global_request
        '''
        while True:
            if not visual_config.message_queue.empty():
                raw_msg = visual_config.message_queue.get()
                my_msg = json.loads(raw_msg['data'])
                self.ip_address = raw_msg['address']
                method = my_msg['method']
                self.height = my_msg['height']
                self.msg = json.loads(my_msg['content'])
                if method == "global_reply":
                    func = getattr(self,'handle_' + method)
                    func()

    def handle_global_reply(self):
        global extra
        extra['host_list'] = self.msg["host_list"]
        extra['msg_queue_length'] = self.msg["msg_queue_length"]
        extra['address'] = self.msg["address"]
        extra['local_host'] = self.msg["local_host"]
        extra['global_height'] = self.msg["global_height"]
        extra['blockchain_list'] = self.msg["blockchain_list"]
        extra['global_difficulty'] = self.msg["global_difficulty"]
        extra['balance_list'] = self.msg["balance_list"]
        extra['global_pre_hash'] = self.msg["global_pre_hash"]

    def global_request(self):
        while True:
            for i in range(len(visual_config.host_list)):
                host = visual_config.host_list[i][0]
                try:
                    extra = json.dumps({"extra":"get global data!"})
                    msg = {"method":"global_request","height":0,"content":extra}
                    self.msg = json.dumps(msg)
                    self.send(host)
                except:
                    del visual_config.host_list[i]
                    break
                time.sleep(1)


    def send_all(self):
        #log.info('Broardcasting message...')
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

def discovery_send():
    #log.info('Starting host discovery...')
    d = discovery(broardcast_msg,broardcast_port)
    d.broadcast()

def discovery_receive():
    d = discovery(broardcast_msg,broardcast_port)
    d.receive()

def msg_generator():
    #log.info('Receiving message...')
    m = message("",visual_config.message_port)
    m.recv()

def msg_consumer():
    #log.info('Handling message...')
    m = message("",visual_config.message_port)
    m.handle()

def update_global():
    m = message("",visual_config.message_port)
    m.global_request()

def report_progress():
    global extra
    height,width = stdscr.getmaxyx()
    global_data = extra
    if not global_data:
        return

    for i in range(1,50):
        stdscr.addstr(i, 0, " "*(width-1))

    half_width = min(width/2, 30)

    #stdscr.addstr(0, 0, "my address is "+visual_config.my_addr, curses.color_pair(3))

    host_list = []
    host_num = 0
    for dirname in os.listdir("./blockchain"):
        host_list.append(dirname)
        host_num += 1

    local_host = global_data["local_host"]
    alive_host_list = visual_config.host_list

    alive_host_num = len(alive_host_list)

    dead_host_num = host_num - alive_host_num
    dead_host_list = list(host_list)
    try: 
        del dead_host_list[dead_host_list.index(local_host)]
    except Exception, e:
        pass

    for host in alive_host_list:
        try:
            del dead_host_list[dead_host_list.index(host[0])]
        except Exception, e:
            pass

    next_line = 2
    stdscr.addstr(next_line, 0, "*****  Visual View  *****".rjust(width/3, " "), curses.color_pair(2))
    next_line += 3
    stdscr.addstr(next_line, 0, (str(alive_host_num)+" Alive").rjust(half_width, " "), curses.color_pair(2))
    stdscr.addstr(next_line, half_width, (str(dead_host_num)+" Dead").rjust(half_width), curses.color_pair(1))
    
    max_host_num = max(alive_host_num, dead_host_num)
    for i in range(1, max_host_num+1):
        if i<=alive_host_num:
            if alive_host_list[i-1][0]==local_host:
                stdscr.addstr(next_line + i, 0, local_host.rjust(half_width, " "), curses.color_pair(3))
            else:
                stdscr.addstr(next_line + i, 0, alive_host_list[i-1][0].rjust(half_width, " "), curses.color_pair(2))
        if i<=dead_host_num:
            stdscr.addstr(next_line + i, half_width, dead_host_list[i-1].rjust(half_width, " "), curses.color_pair(1))

    next_line = next_line + max_host_num + 3
    global_height_str = "global_height: "+str(global_data["global_height"])
    global_difficulty_str = "global_difficulty: "+global_data["global_difficulty"]
    global_pre_hash = "global_pre_hash: "+global_data["global_pre_hash"]

    stdscr.addstr(next_line, 0, global_height_str[:width], curses.color_pair(5))
    next_line += 1
    stdscr.addstr(next_line, 0, global_difficulty_str[:width], curses.color_pair(5))
    next_line += 1
    stdscr.addstr(next_line, 0, global_pre_hash[:width], curses.color_pair(5))
    next_line += 1

    next_line += 2
    stdscr.addstr(next_line, 0, "height", curses.A_BOLD)    # 8
    stdscr.addstr(next_line, 8, "hash", curses.A_BOLD)    #(64) 72
    stdscr.addstr(next_line, 80, "pre_hash", curses.A_BOLD)   #(64) 70
    stdscr.addstr(next_line, 150, "input.god.amount", curses.A_BOLD)  #20
    #stdscr.addstr(next_line, 170, "input.address", curses.A_BOLD)  #128
    next_line += 1

    blockchain_list = global_data["blockchain_list"]
    blockchain_num = len(blockchain_list)
    show_num = min(blockchain_num, 20)
    for i in range(blockchain_num, blockchain_num-show_num, -1):
        tmp_hash = blockchain_list[str(i)]
        try:
            with open("./blockchain/"+local_host+"/"+str(i)+"-"+tmp_hash) as f:
                tmp_data = json.loads(f.read().strip().strip())
                stdscr.addstr(next_line, 0, str(i), curses.A_BOLD)    # 8
                stdscr.addstr(next_line, 8, tmp_hash, curses.A_BOLD)    #(64) 72
                stdscr.addstr(next_line, 80, tmp_data["prev_hash"], curses.A_BOLD)   #(64) 70
                stdscr.addstr(next_line, 150, str(tmp_data["transaction"][0]["input"][0]["amount"]), curses.A_BOLD)  #20
                #stdscr.addstr(next_line, 170, tmp_data["transaction"][0]["input"][1]["address"], curses.A_BOLD)  #128
                next_line += 1
        except Exception, e:
            pass
    stdscr.refresh()

if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    stdscr.keypad(1)
    
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    extra = {}

    t1 = threading.Thread(target=discovery_send,name='discovery_send')
    t2 = threading.Thread(target=discovery_receive,name='discovery_receive')
    t3 = threading.Thread(target=msg_generator,name='msg_generator')
    t4 = threading.Thread(target=msg_consumer,name='msg_consumer')
    t5 = threading.Thread(target=update_global,name='update_global')
    #t6 = threading.Thread(target=block_broadcast,name='block_broadcast')
    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    t5.setDaemon(True)
    #t6.setDaemon(True)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    #t6.start()

    try:
        i = 0
        while True:
            i += 1
            report_progress()
            time.sleep(1)
    except KeyboardInterrupt:
        #log.error('Killed by user')
        sys.exit()
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        stdscr.keypad(0)
