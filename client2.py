import socket
import json
import time
import pprint

s1 = socket.socket()

def nodes_config():        
    port_list_1_mem = '12345'
    #port_list_2_mem = '12347'
    ip_list_1_mem = '127.0.0.1'
    #ip_list_2_mem = '127.0.0.1'
    port_list = [port_list_1_mem]                              
    ip_list = [ip_list_1_mem]
    s1.send(b'client')
    time.sleep(1)
    s1.send(b'add_nodes')
    time.sleep(1)
    for port_mem in port_list:
        s1.send(port_mem.encode('utf-8'))
        time.sleep(1)
    for ip_mem in ip_list:
        s1.send(ip_mem.encode('utf-8'))
        time.sleep(1)
    print('Nodes are connected')

def add_transaction_to_blockchain(transaction_pool, box_number, my_own_box_are_finished):
    s1.send(b'lock')            
    s2 = socket.socket()
    s2.connect(('127.0.0.1', 12346))
    s2.send(b'server')          
    b = b''
    tmp = s2.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    chain = d['chain']
    add_it = True
    counter1 = len(chain)
    counter1 = counter1 - 1
    while counter1 > 0:
        if chain[counter1]['transactions'][0][box_number] == 1:
            add_it = False
            break
        counter1 = counter1 - 1
    if add_it == True:
            s1.send(b'add_transaction')
            time.sleep(1)
            if my_own_box_are_finished == False:
                send_dict = {'block_details':transaction_pool,'own_flag':1}
            else:
                send_dict = {'block_details':transaction_pool,'own_flag':0}
            b = json.dumps(send_dict).encode('utf-8')
            s1.send(b)
            if s1.recv(4096) == b'move_forward':
                print('ok') 
    s1.send(b'release')
    return add_it

def init_blockchain():
    s1.connect(('127.0.0.1', 12346))
    nodes_config()
