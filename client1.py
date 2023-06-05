#SOURCE

import socket
import threading
import json
from queue import Queue

i=0#dummy
Q=Queue
BUFFER=2048
ServerIP = socket.gethostbyname(socket.gethostname())
ClientIP = socket.gethostbyname(socket.gethostname())
ServerPORT = 60501
ClientPORT = 60583
Server_ADDR=(ServerIP,ServerPORT)
Client_ADDR=(ClientIP,ClientPORT)
data = {'type':'SOURCE','IP': ClientIP,'PORT':ClientPORT,'Power':100}#Create the dictonary
msg_format={'type':'SOURCE','IP':ClientIP,'PORT':ClientPORT,'msg':0}#Message format for all communication apart from initial connection
client2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Socket client2 waits for a message from the load if its a source

def server_connect(Server_ADDR,data={}):
    send(Server_ADDR,data)
    print("Connected to the server")
    
def client_connect(Client_ADDR,msg_format={}):
    client2.bind(Client_ADDR)
    client2.listen()
    Listening=True
    while Listening:
        conn,addr=client2.accept()
        msg=json.loads(conn.recv(BUFFER).decode())
        server_recv_thread = threading.Thread(target=server_recv,args=(i,msg))
        load_recv_thread=threading.Thread(target=load_recv,args=(i,msg,msg_format))
        server_recv_thread.start()
        load_recv_thread.start()

def server_recv(i,msg={}):
    if (msg['type']=='SERVER'):
        print(f"message received from the server is {msg['msg']}")
        
def load_recv(i,msg={},msg_format={}):
    if(msg['type']=='LOAD'):
        print(f"message received from the load {msg['IP']}")
        print(f"Power requirement of the Load is {msg['msg']}")
        msg_format['msg']=data['Power']
        ADDR=(msg['IP'],msg['PORT'])
        send(ADDR,msg_format)
        
def send(ADDR=(),msg={}):
    client1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Socket client1 transmits the client info 
    client1.connect(ADDR)
    client1.sendall(json.dumps(msg).encode())
    client1.close()

server_connect(Server_ADDR,data)
client_connect(Client_ADDR,msg_format)






 
     
  
    


    
        
       


