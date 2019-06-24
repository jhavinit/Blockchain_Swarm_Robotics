import datetime
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse
import socket
from _thread import *
import threading
import time
import pprint

s = socket.socket()		 
print ("Socket successfully created")
port = 12345				
s.bind(('', port))		 
print (("Socket binded to %s") %(port)) 
s.listen(5)	 
print ("Socket is listening")

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = []
        self.ips = [] 
        self.i_added = 'F'
        self.can_i_add_block = 'T'
        self.get_chain_lock = False
        self.iamfirst = False
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.chain.append(block)
        self.transactions = []
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self,transaction_pool_list):
        self.transactions.append(transaction_pool_list)
        
    def add_node(self,address,address1):
        self.ips.append(address1)
        self.nodes.append(address)
    
    def replace_chain(self):
        network = self.nodes
        ip_network = self.ips
        longest_chain = None
        max_length = len(self.chain)
        counter = 0        
        while counter < len(network):
            m = socket.socket()
            m.connect((ip_network[counter], int(network[counter])))
            m.send(b'client')                                                 #change this if does not works
            time.sleep(2)
            m.send(b'get_chain')
            b = b''
            tmp = m.recv(1048576)
            b += tmp
            d = json.loads(b.decode('utf-8')) 
            chain = d['chain']
            length = d['length'] 
            if length > max_length:
                    max_length = length
                    longest_chain = chain
            m.close()
            counter = counter + 1
            
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    def get_node_list(self):
        return self.nodes

    def get_ip_list(self):
        return self.ips

    def set_iamfirst(self):
        self.iamfirst = True
    
    def unset_iamfirst(self):
        self.iamfirst = False

    def set_get_chain_lock(self):
        while self.iamfirst == True:
            print('waiting')
        self.get_chain_lock = True

    def unset_get_chain_lock(self):
        self.get_chain_lock = False

    def check_state_of_get_chain_lock(self):
        while self.get_chain_lock == True:
            print('Get chain is locked | Waiting to be unlocked...')

node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()
 
def mine_block(own_bot): 
    network_list = blockchain.get_node_list()
    ip_list = blockchain.get_ip_list()
    if(own_bot == 0):
        time.sleep(1) 
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(sender = node_address, receiver = 'bot_1', amount = 10$)
    block = blockchain.create_block(proof, previous_hash)
    '''
    response = {'message': 'bot_1 mined the block 1st!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    else:
        response = {'message': 'bot_1 was not able to mine the block, blockchain.mining_can_i_add_block() = False'}
        
    return response
    '''

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return response

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return response

def add_transaction(transaction_pool_list,own_flag):
    index = blockchain.add_transaction(transaction_pool_list)
    response_dict = mine_block(own_flag)
    response = {'message':'The block transaction is added to Blockchain'}
    return response

def connect_node(nodes1,ips1): 
    nodes = nodes1
    ips = ips1
    counter = 0     
    while counter < len(nodes):        
        blockchain.add_node(nodes[counter],ips[counter])
        counter = counter + 1
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the nodes:'}
    return response

def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'Response from:': 'bot-1',
                    'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return response

def for_server(c):
    m1 = socket.socket()
    m1.connect(('127.0.0.1',12346))
    m1.send(b'iam_first')                                                 #change this if does not works
    m1.close()
    replace_chain()
    m1 = socket.socket()
    m1.connect(('127.0.0.1',12346))
    m1.send(b'unset_iam_first')                                                 #change this if does not works
    m1.close()
    a_dict = get_chain()
    b = json.dumps(a_dict).encode('utf-8')
    c.send(b)


def for_unset_iam_first(c):
    blockchain.unset_iamfirst()
    
def for_iamfirst(c):
    blockchain.set_iamfirst()
    
def for_client(c):
    while 1:
        var1 = c.recv(4096)
        
        if var1 == b'':
            exit()

        if var1 == b'lock':
            blockchain.set_get_chain_lock()
        
        if var1 == b'own_get_chain':
            a_dict = get_chain()
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)

        if var1 == b'release':
            blockchain.unset_get_chain_lock()
            
        if var1 == b'get_chain':
            blockchain.check_state_of_get_chain_lock()
            a_dict = get_chain()
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
            
        if var1 == b'add_transaction': 
            b = b''
            tmp = c.recv(1048576)
            b += tmp
            d = json.loads(b.decode('utf-8')) 
            transaction_pool_list = d['block_details']
            own_flag = d['own_flag']
            response_dict  = add_transaction(transaction_pool_list,own_flag)
            c.send(b'move_forward')
             
        if var1 == b'add_nodes':
            nodes1 = []
            ips1 = []
            mem1 = c.recv(4096).decode('utf-8');
            mem4 = c.recv(4096).decode('utf-8');
            nodes1.append(mem1)
            ips1.append(mem4)
            a_dict  = connect_node(nodes1,ips1)
                           
while True: 
    c, addr = s.accept() 
    x = c.recv(4069)
    if x == b'server':
        start_new_thread(for_server, (c,))
    if x == b'client':
        start_new_thread(for_client, (c,))
    if x == b'iam_first':
        start_new_thread(for_iamfirst, (c,))
    if x == b'unset_iam_first':
        start_new_thread(for_unset_iam_first, (c,))
c.close()




