#LOAD

import socket
import threading
import json
import time

# from .client3 import server_connect
i=0#dummy
BUFFER=2048
ServerIP = socket.gethostbyname(socket.gethostname())
ClientIP = socket.gethostbyname(socket.gethostname())
ServerPORT = 60501
ClientPORT = 60586
Server_ADDR=(ServerIP,ServerPORT)
Client_ADDR=(ClientIP,ClientPORT)
data = {'type':'LOAD','IP': ClientIP,'PORT':ClientPORT,'Power':50}#Create the dictonary
msg_format={'type':'LOAD','IP':ClientIP,'PORT':ClientPORT,'msg':0}#Message format for all communication apart from initial connection
client2=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Socket client2 waits for a message from the server if its a load 

def server_connect(Server_ADDR,data={}):
    print("Connected to the server")
    print(f"Power requirement is{data['Power']}")
    while True:
        send(Server_ADDR,data)
        time.sleep(100)

def client_connect(Client_ADDR,msg_format={}):
    client2.bind(Client_ADDR)
    client2.listen()
    listening=True
    while listening:
        conn,addr=client2.accept()
        msg=json.loads(conn.recv(BUFFER).decode())
        server_recv_thread = threading.Thread(target=server_recv,args=(i,msg,msg_format))
        load_recv_thread=threading.Thread(target=load_recv,args=(i,msg))
        server_recv_thread.start()
        load_recv_thread.start()

def server_recv(i,msg={},msg_format={}):
    if (msg['type']=='SERVER'):
        print(f"Address received from the server...")
        print(f"message received from the server is {msg['msg'][0]},{msg['msg'][1]}")
        ADDR = (msg['msg'][0],msg['msg'][1])
        msg_format['msg']=msg['msg'][2] #send a message to the load
        send(ADDR,msg_format)

        
def load_recv(i,msg={}):
    if(msg['type']=='SOURCE'):
        print(f"message received from the source {msg['IP']}")  
        print(f"Power availability at the source is {msg['msg']}")

def send(ADDR=(),msg={}):
    client1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#Socket client1 transmits the client info 
    client1.connect(ADDR)
    client1.sendall(json.dumps(msg).encode())
    client1.close()


if __name__ == "__main__":
    Thread1=threading.Thread(target=server_connect,args=(Server_ADDR,data))
    Thread2=threading.Thread(target=client_connect,args=(Client_ADDR,msg_format))  
    Thread1.start()
    Thread2.start()



"""# Sending the text file , uncomment this to send the text file and add lines in the server for interpreting different client file formats
# def send_TextFile():
#     with open('C1.txt', 'rb') as file:
#         chunk = file.read(BUFFER)
#         while chunk:
#             client.send(chunk)
#             chunk = file.read(BUFFER)"""


# if __name__=="__main__":
#     server_connect(Server_ADDR,data)
#     client_connect(Client_ADDR)


 
     
  
    


    
        
       


