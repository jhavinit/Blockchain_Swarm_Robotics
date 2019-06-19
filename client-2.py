import socket
import json
import time
import pprint

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

#time.sleep(5)

s.send(b'add_transaction')
time.sleep(1)
send_dict = {'block_details':transaction_pool_block,
             'own_flag':1}
b = json.dumps(send_dict).encode('utf-8')
s.send(b)
print('Initial state of the block city 2 is added on blockchain')
recieved_text = s.recv(4096)
if recieved_text == b'move_forward':
    print('Moving forward...')

def update_block_from_blockchain(transaction_pool_block):
    s.send(b'get_chain')
    b = b''
    tmp = s.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8')) 
    print('Get chain results:')
    pprint.pprint(d)
    counter1 = len(d['chain'])
    counter1 = counter1 - 1 
    while counter1 > 0: 
            if d['chain'][counter1]['transactions'][0][0] == 'bot_2':
                if transaction_pool_block == d['chain'][counter1]['transactions'][0]:
                    print('No change in any box position')
                    break
                else:
                    transaction_pool_block = d['chain'][counter1]['transactions'][0]
                    print('Box position changed, block trans. list updated')
                    break
            counter1 = counter1 - 1
            
def traverse_path():
    #time.sleep(20)
    update_block_from_blockchain(transaction_pool_block)
    i = 1
    all_box_finished = True
    box_number = -1
    while i < len(transaction_pool_block):
        if transaction_pool_block[i] == 0:
            all_box_finished = False
            box_number = i
            break
        i = i + 1

    if all_box_finished == False:
        print("Moving till node is detected...")
        print("Node detected!")
        #func() find the block that is at the smallest distance from it and return its 'block number'
        #box_number = ...
        transaction_pool_block[box_number] = 1
        s.send(b'get_chain')
        b = b''
        tmp = s.recv(1048576)
        b += tmp
        e = json.loads(b.decode('utf-8'))
        d = e
        add_it = True
        counter1 = len(d['chain'])
        counter1 = counter1 - 1
        while counter1 > 0:
            #print('d[chain][counter1][transactions][0]')
            print(counter1)
            if transaction_pool_block == d['chain'][counter1]['transactions'][0]:
                add_it = False
                print('Already present, not added to blockchain')
                break
            counter1 = counter1 - 1

        if add_it == True:
                print('Not presesnt,adding...')
                s.send(b'add_transaction')
                time.sleep(1)
                send_dict = {'block_details':transaction_pool_block,
                             'own_flag':1}
                b = json.dumps(send_dict).encode('utf-8')
                s.send(b)
                print("Transaction is added")
                recieved_text = s.recv(4096)
                if recieved_text == b'move_forward':
                    print('Moving forward...')
    #path planning code for picking the box_number and placing
        
    else:
        #func() to move till you get a node , it has to be a blocking function
        bot_name_list = ['bot_1']
        choose_shortest_list = []
        bot_counter = 0
        while bot_counter < len(bot_name_list):
            s.send(b'get_chain')
            b = b''
            tmp = s.recv(1048576)
            b += tmp
            d = json.loads(b.decode('utf-8'))
            counter1 = len(d['chain'])
            counter1 = counter1 - 1
            while counter1 > 0:
                 if d['chain'][counter1]['transactions'][0][0] == bot_name_list[bot_counter]:
                    choose_shortest_list.append(d['chain'][counter1]['transactions'][0])
                    break
                 counter1 = counter1 - 1
            bot_counter = bot_counter + 1   
        help_flag = -1
        help_index = -1
        k = 0
        transaction_pool_block_temp = []
        while k < len(choose_shortest_list):
            n = 1
            while n < len(choose_shortest_list[k]):
                if choose_shortest_list[k][n] == 0:
                    help_flag = 1
                    help_index = n
                    transaction_pool_block_temp = choose_shortest_list[k] 
                    break
                n = n + 1
            if help_flag == 1:
                break
            k = k + 1        
        #code to select the shortest city and the respective box
        #transaction_pool_block_temp = #shortest selected transaction_pool
        if help_flag == 1:
            transaction_pool_block_temp[help_index] = 1
            
            s.send(b'get_chain')
            b = b''
            tmp = s.recv(1048576)
            b += tmp
            d = json.loads(b.decode('utf-8'))
            add_it = True
            counter1 = len(d['chain'])
            counter1 = counter1 - 1
            while counter1 > 0: 
                if transaction_pool_block_temp == d['chain'][counter1]['transactions'][0]:
                    add_it = False
                    print('Already present, not added to blockchain')
                    break
                counter1 = counter1 - 1

            if add_it == True:
                print('Not presesnt,adding...')
                s.send(b'add_transaction')
                time.sleep(1)
                send_dict = {'block_details':transaction_pool_block_temp,
                             'own_flag':0}
                b = json.dumps(send_dict).encode('utf-8')
                s.send(b)
                print("Transaction is added")
                print("Successfully helped bot 1")
                print("Box no. picked was:")
                print(help_index)
                recieved_text = s.recv(4096)
                if recieved_text == b'move_forward':
                    print('Moving forward...')
            
        else:
            print("No help needed")
            inp = input("Task finished")
            #movement code to pick and place the box on different city with collisison checking
            
while True:
        time.sleep(5)
        traverse_path()
        
s.close() 
