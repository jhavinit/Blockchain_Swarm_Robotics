import socket
import json
import time
import pprint

while True:
    
    s6 = socket.socket()
    s6.connect(('127.0.0.1', 12345))

    s7 = socket.socket()
    s7.connect(('127.0.0.1', 12346))

    time.sleep(5)
    message = """<!DOCTYPE html>
<html lang="en">
                  <head><meta http-equiv="refresh" content="10">  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script></head>
                  <style>.text-white {
    color: #fff!important;
    font-weight: bolder;
}
.bg-primary {
    background-color: #007bff!important;
    width: 625px;
}
.container1 {
    width: 625px;
}

.connect_1 {
margin-left:280px;
width: 625px;}

.connect_2 {
margin-left:280px;
width: 625px;}

.container2 {
    width: 625px;
}
</style><body><center><br><button type="button" class="btn btn-default"><h1 style="font-weight:bolder;font-family:Courier"><span style="color:white;font-weight:bolder;font-family:Courier;background-color:red"> e-Yantra </span> &nbsp Blockchain Demonstration</h1></button><br><br></center><hr><div class="container-fluid"><div class="row">"""
    s6.send(b'display')
    b = b''
    tmp = s6.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    chain = d['chain']
    s6.close()
    #print(chain)
    message_length = len(chain)
    counter = 0
    message = message + """<div class="col-md-6"><center><button type="button" class="btn btn-danger"><h2 style="font-weight:bolder;font-family:Courier">BOT-2</h2></button></center><br>"""
    while counter < message_length:
        message = message + """<div class="container1">"""
        message = message + """<div class="card bg-primary text-white"><div class="card-body">"""
        message = message + """<p>Index : """ + str(chain[counter]['index']) + """</p><p>Timestamp : """ + str(chain[counter]['timestamp']) + """</p><p>Proof : """ + str(chain[counter]['proof']) + """</p><p>Previous Hash : """ + str(chain[counter]['previous_hash']) + """</p>"""
        message = message + """<p>Transactions: """
        counter1 = 0
        if len(chain[counter]['transactions']) != 0:
            while counter1 < len(chain[counter]['transactions'][0]):
                message = message + str(chain[counter]['transactions'][0][counter1]) + """ """ 
                counter1 = counter1 + 1
        message = message + """</p></div></div></div><br><h1 class="connect_1" style="font-weight:bolder">||</h1><br>"""
        counter = counter + 1
    message = message + """</div>"""

    s7.send(b'display')
    b = b''
    tmp = s7.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))
    chain = d['chain']
    #print(chain)
    s7.close()
    message_length = len(chain)
    counter = 0
    message = message + """<div class="col-md-6"><center><button type="button" class="btn btn-danger"><h2 style="font-weight:bolder;font-family:Courier">BOT-1</h2></button></center><br>"""
    while counter < message_length:
        message = message + """<div class="container2">"""
        message = message + """<div class="card bg-success text-white"><div class="card-body">"""
        message = message + """<p>Index : """ + str(chain[counter]['index']) + """</p><p>Timestamp : """ + str(chain[counter]['timestamp']) + """</p><p>Proof : """ + str(chain[counter]['proof']) + """</p><p>Previous Hash : """ + str(chain[counter]['previous_hash']) + """</p>"""
        message = message + """<p>Transactions: """
        counter1 = 0
        if len(chain[counter]['transactions']) != 0:
            while counter1 < len(chain[counter]['transactions'][0]):
                message = message + str(chain[counter]['transactions'][0][counter1]) + """ """ 
                counter1 = counter1 + 1
        message = message + """</p></div></div></div><br><h1 class="connect_2" style="font-weight:bolder">||</h1><br>"""
        counter = counter + 1
    message = message + """</div>"""
    
    message = message + """</div></div></body></html>"""
    #print('message:')
    #print(message)
    f = open('display_blockchain.html','w')
    print('Writing to html file...')
    f.write(message)
    f.close()
