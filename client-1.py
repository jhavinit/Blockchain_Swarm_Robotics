import socket
import json
import time
import pprint

s1 = socket.socket()
s1.connect(('127.0.0.1', 12345))
#segregation code
#help index and start index fix

transaction_pool = [0,0,0,0,0]
start_index = 0
help_start_index = 4

box_number = -1

all_box_finished = True
my_own_box_are_finished = True

port_list_1_mem = '12346'
#port_list_2_mem = '12347'
#port_list_3_mem = '12348'
ip_list_1_mem = '127.0.0.1'
#ip_list_2_mem = '127.0.0.1'
#ip_list_3_mem = '127.0.0.1'

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

time.sleep(5)

while True: 

    if start_index < help_start_index:
        i = start_index
        while i <= help_start_index:
            if transaction_pool[i] == 0:
                my_own_box_are_finished = False
                box_number = i
                break
            i = i + 1
    else:
        i = start_index
        while i < len(transaction_pool):
            if transaction_pool[i] == 0:
                my_own_box_are_finished = False
                box_number = i
                break
            i = i + 1
            
    if my_own_box_are_finished == True:
        if start_index < help_start_index:
            i = help_start_index
            while i < len(transaction_pool):
                if transaction_pool[i] == 0:
                    all_box_finished = False
                    box_number = i
                    break
                i = i + 1
        else:
            i = help_start_index
            while i <= start_index:
                if transaction_pool[i] == 0:
                    all_box_finished = False
                    box_number = i
                    break
                i = i + 1
    else:
        all_box_finished = False
        
    if all_box_finished == False: 
        s1.send(b'lock')
        #double check before adding
        transaction_pool[box_number] = 1            
        print('Trying to add:')
        print(transaction_pool)
        s2 = socket.socket()
        s2.connect(('127.0.0.1', 12345))
        s2.send(b'server')                             #in server command do a replace chain and then a get chain
        b = b''
        tmp = s2.recv(1048576)
        b += tmp
        d = json.loads(b.decode('utf-8'))
        chain = d['chain']
        print('Replace chain results:')
        pprint.pprint(chain)
        add_it = True
        counter1 = len(chain)
        counter1 = counter1 - 1
        while counter1 > 0:
            if transaction_pool[box_number] == chain[counter1]['transactions'][0][box_number]:
                add_it = False
                print('Already present, not added to Blockchain')
                transaction_pool[box_number] = 1
                break
            counter1 = counter1 - 1

        if add_it == True:
                print('Not presesnt,adding...')
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
                print("Transaction is Added, Transaction added is :")
                print(transaction_pool)
                
        s1.send(b'release')
        #Bot 1 is moving to pick and place the box
        #After coming at base node
        if add_it == False:
            print('Bot 1 is looking for other box...')
        if add_it == True:
            print('Bot 1 is doing pickup and place...')
        time.sleep(5)
        if add_it == True:
            print('Bot 1 pickup and place done')
        my_own_box_are_finished = True
        all_box_finished = True

    else:
        print('All boxes are finished!')
        break
    
print('***END***')
s1.close()
