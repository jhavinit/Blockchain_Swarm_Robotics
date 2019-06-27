import socket
import json
import time
import pprint

while True:
    
    s1 = socket.socket()
    s1.connect(('127.0.0.1', 12345))

    time.sleep(5)
    message = """<html>
                  <head><meta http-equiv="refresh" content="10"></head>
                  <body>"""
    s1.send(b'display')
    b = b''
    tmp = s1.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    chain = d['chain']
    #print(chain)
    message_length = len(chain)
    counter = 0
    while counter < message_length:
        message = message + """<p>index : """ + str(chain[counter]['index']) + """</p><p>timestamp : """ + str(chain[counter]['timestamp']) + """</p><p>proof : """ + str(chain[counter]['proof']) + """</p><p>previous_hash : """ + str(chain[counter]['previous_hash']) + """</p>"""
        message = message + """<p>Transactions: </p>"""
        counter1 = 0
        #print(chain[counter]['transactions'])
        #print('reached')
        if len(chain[counter]['transactions']) != 0:
            #print('reached here also')
            #leng = len(chain[counter]['transactions'][0])
            while counter1 < len(chain[counter]['transactions'][0]):
                message = message + """<p>""" + str(counter1 + 1) + """: """ + str(chain[counter]['transactions'][0][counter1]) + """</p>""" 
                counter1 = counter1 + 1
            message = message + """<p>--------------------->>></p>"""
        counter = counter + 1
    message = message + """</body></html>"""
    #print('message:')
    #print(message)
    f = open('display_blockchain.html','w')
    print('Writing to html file...')
    f.write(message)
    f.close()
    s1.close()
