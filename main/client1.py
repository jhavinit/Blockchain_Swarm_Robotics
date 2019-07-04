#* Filename: client1.py
#* Project: Blockchain_Swarm_Robotics
#* Functions: init_blockchain(), nodes_config(), add_transaction_to_blockchain(transaction_pool, box_number, my_own_box_are_finished) 
#* Global Variables: s1

#Imported for bidirectional end to end connection between server and client scripts
import socket
#Imported for sending and recieving data
import json
#Imported for syncronization and handshakes
import time
#Imported for printing large dictionaries with indentation
import pprint

#s1: socket communication object that helps to recieve and send data between sockets
s1 = socket.socket()

'''
* Function Name: nodes_config()
* Input: None
* Output: Returns nothing, prints 'Nodes are connected'
* Logic: Stores the list of nodes in the blockchain. Sends a " b'client' " and then " b'add_nodes' " request to server-1.py so as to send the list of IP's and respective port numbers.  
* Example Call: nodes_config()
'''

def nodes_config():        
    port_list_1_mem = '12346'
    ip_list_1_mem = '127.0.0.1'
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


'''
* Function Name: add_transaction_to_blockchain(transaction_pool, box_number, my_own_box_are_finished)
* Input: transaction_pool: It contains the transaction pool recieved by main-1.py for adding it to blockchain
*        box_number: It contains the box_number which is picked by bot-1, whose state is to be changed from 0 to 1
*        my_own_box_are_finished: It contains a boolean value that wheather boxes that were assigned to bot-1 are finished or not 
* Output: Returns add_it, add_it: It returns the boolean value that weather the box was added or not into blockchain
* Logic: During a transaction is being added into blockchain first a lock is created on the get_chain()(In server-1.py), because if transaction is added into the blockhain and some other
*        other node reads the former bot's chain in between the transaction then the second bot has incorrect chain (dirty read), and after block is added then the lock is released.
* Example Call: add_transaction_to_blockchain(list, int, bool)
'''

def add_transaction_to_blockchain(transaction_pool, box_number, my_own_box_are_finished):
    s1.send(b'lock')            
    s2 = socket.socket()
    s2.connect(('127.0.0.1', 12345))
    #After creating a lock on get_chain() function in server-1.py, any file cannot read the chain that bot-1 has but (b'server') is a special request to server-1.py that returns results of get_chain() directly. 
    s2.send(b'server')          
    b = b''
    tmp = s2.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    chain = d['chain']
    add_it = True
    counter1 = len(chain)
    counter1 = counter1 - 1
    #Checking in the blockchain that wheather the transaction is already present or not
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
            #Recieving 'ok' to create a handshake  
            if s1.recv(4096) == b'move_forward':
                print('ok') 
    s1.send(b'release')
    return add_it


'''
* Function Name: init_blockchain
* Input: None 
* Output: It connects the s1 object to server's port using sockets 
* Logic: It is the initailizing function for blockchain,It connects the s1 object to server's port using sockets and then calls nodes_config() to add nodes in network.
* Example Call: init_blockchain()
'''

def init_blockchain():
    s1.connect(('127.0.0.1', 12345))
    nodes_config()
