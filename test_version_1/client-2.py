import socket
import json
import time

s = socket.socket()
s.connect(('127.0.0.1', 12346))
transaction_pool_block = ['bot_2',0,0,0,0]
all_box_finished = False
port_list_1_mem = '12345'
#port_list_2_mem = '12347'
#port_list_3_mem = '12348'
ip_list_1_mem = '127.0.0.1'
#ip_list_2_mem = '127.0.0.1'
#ip_list_3_mem = '127.0.0.1'
port_list = [port_list_1_mem]                              
ip_list= [ip_list_1_mem]
s.send(b'client')
time.sleep(1)
s.send(b'add_nodes')
time.sleep(1)
for port_mem in port_list:
    s.send(port_mem.encode('utf-8'))
    time.sleep(1)

for ip_mem in ip_list:
    s.send(ip_mem.encode('utf-8'))
    time.sleep(1)
print('Nodes are connected')

time.sleep(3)

s.send(b'add_transaction')
send_dict = {'block_details':transaction_pool_block,
             'own_flag':1}
time.sleep(3)
b = json.dumps(send_dict).encode('utf-8')
s.send(b)
print('Initial state of the block c2 is added on blockchain')

def update_block_from_blockchain(transaction_pool_block):
    exit_now = False
    s.send(b'get_chain')
    b = b''
    tmp = s.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    counter1 = len(d['chain'])
    counter1 = counter1 - 1
    while counter1 >= 0:
            if d['chain'][counter1]['transactions'][0][0] == 'bot_2':
                exit_now = True
                if transaction_pool_block == d['chain'][counter1]['transactions'][0]:
                    print('No change in any box position')
                else:
                    transaction_pool_block = d['chain'][counter1]['transactions']
                    print('Box position changed, block trans list updated')
            if exit_now == True:
                return
            counter1 = counter1 - 1
            
def traverse_path():
    time.sleep(5)
    update_block_from_blockchain(transaction_pool_block) 
    i = 1
    while i < len(transaction_pool_block):
        if transaction_pool_block[i] == 0:
            all_box_finished = False
            i = len(transaction_pool_block) + 1
        else:
            all_box_finished = True
        i = i + 1

    if all_box_finished == False:
        print('reached')
        #func() to move till you get a node , it has to be a blocking function
        print("Moving till node is detected...")
        print("Node detected!")
        j = 1
        while j < len(transaction_pool_block):
            if transaction_pool_block[j] == 0:
                box_number = j
                print('box selected:')
                print(box_number)
                j = len(transaction_pool_block) + 1
            j = j + 1
        #func() find the block that is at the smallest distance from it and return its 'block number'
        #box_number = ...
        transaction_pool_block[box_number] = 1
        s.send(b'add_transaction')
        time.sleep(3)
        send_dict = {'block_details':transaction_pool_block,
                     'own_flag':1}
        time.sleep(3)
        b = json.dumps(send_dict).encode('utf-8')
        s.send(b)
        #path planning code for picking the box_number and placing
        
    else:
        #func() to move till you get a node , it has to be a blocking function
        bot_name_list = ['bot_1']
        choose_shortest_list = []
        exit_now = False
        s.send(b'get_chain')
        b = b''
        tmp = s.recv(1048576)
        b += tmp
        d = json.loads(b.decode('utf-8'))
        print("bot_1 chain")
        print(d['chain'])
        bot_counter = 0
        while bot_counter < len(bot_name_list):
            block_number_to_go_list = []
            counter1 = len(d['chain'])
            counter1 = counter1 - 1 
            while counter1 >= 0: 
                 if d['chain'][counter1]['transactions'][0][0] == bot_name_list[bot_counter]:
                    exit_now = True
                    block_number_to_go_list.append(bot_name_list[bot_counter])
                    counter3 = 1
                    print('bot 1 t_list')
                    print(d['chain'][counter1]['transactions'][0])
                    while counter3 < len(d['chain'][counter1]['transactions'][0]):
                        block_number_to_go_list.append(d['chain'][counter1]['transactions'][0][counter3])
                        counter3 = counter3 + 1
                 if exit_now == True:  
                    exit_now = False
                    counter1 = -1 
                 counter1 = counter1 - 1
            choose_shortest_list.append(block_number_to_go_list)
            bot_counter = bot_counter + 1
            print('choose list:')
            print(choose_shortest_list)
        help_flag = -1
        help_index = -1
        k = 0
        while k < len(choose_shortest_list):
            n = 1
            while n < len(choose_shortest_list[k]):
                if choose_shortest_list[k][n] == 0:
                    help_flag = 1
                    help_index = n
                    transaction_pool_block_temp = choose_shortest_list[k] 
                    n = len(choose_shortest_list[k]) + 1
                n = n + 1
            if help_flag == 1:
                k = len(choose_shortest_list) + 1 
            k = k + 1        
        #code to select the shortest city and the respective box
        #transaction_pool_block_temp = #shortest selected transaction_pool
        if help_flag == 1:
            block_number_of_different_city = help_index
            transaction_pool_block_temp[block_number_of_different_city] = 1
            s.send(b'add_transaction')
            send_dict = {'block_details':transaction_pool_block_temp,
                         'own_flag':0}
            b = json.dumps(send_dict).encode('utf-8')
            s.send(b)
            print("successfuly helped bot 1")
            print("changed the flag of box index:")
            print(help_index)
        else:
            print("All the box are placed by all bots!!...no need for help")
            inp = input("Task finished")
            #movement code to pick and place the box on different city with collisison checking .
            
while True:
        traverse_path()

s.close() 
