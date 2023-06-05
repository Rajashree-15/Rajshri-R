import socket
import threading
import json

#Variables and constants
#encoding='utf-8'
BUFFER=2048
disconnect_msg='!DISCONNECT'
IP = socket.gethostbyname(socket.gethostname())
PORT=60501
ADDR=(IP,PORT) #Tuple to store the address
data={'type':{},'IP':{},'PORT':{},'Power':{}}
source={'type':{},'IP':{},'PORT':{},'Power':{}}
load={'type':{},'IP':{},'PORT':{},'Power':{},'match':{}}
i=0
l=0
s=0

#Create the socket
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

#Server functions
def server_start (data={},load={},source={}):
     global i
     server.listen()
     print(f"[LISTENING] Server is listening on {PORT}")
     listening=True
     while listening:
          conn, addr = server.accept() #SOCKET.accept() returns the IP and port of the client
          print(f"[NEW CONNECTION]{addr} connected.")
          i=i+1
          client_thread1 = threading.Thread(target=handle_client,args=(i,conn)) #passing the client's address to the handle function in a thread
          client_thread1.start()
          print(f"[ACTIVE CONNECTIONS]{threading.active_count()-1}")
         
#Thread1      
def handle_client(i,conn):
     global data,source,load,l,s
     json_data = conn.recv(BUFFER).decode()
     data_temp= json.loads(json_data) #may not be needed try json.loads to data without data_temp and additionally add port number
     data['type'][i]=data_temp['type']
     data['IP'][i]=data_temp['IP'] #may not be needed
     data['PORT'][i]=data_temp['PORT']
     data['Power'][i]=data_temp['Power'] #maynot be needed
     with open('table.json','a') as file1:
          json.dump(data,file1)
     if(data_temp['type']=='LOAD'):
          l=l+1
          with open('load.json','a') as file2:
               load['type'][l]=data_temp['type'] #may not be needed try json.loads to data without data_temp and additionally add port number
               load['IP'][l]=data_temp['IP'] #may not be needed
               load['PORT'][l]=data_temp['PORT']
               load['Power'][l]=data_temp['Power'] #maynot be needed
               load['match'][l]=0
               json.dump(load,file2)
     if(data_temp['type']=='SOURCE'):
          s=s+1
          with open('source.json','a') as file3:
               source['type'][s]=data_temp['type'] #may not be needed try json.loads to data without data_temp and additionally add port number
               source['IP'][s]=data_temp['IP'] #may not be needed
               source['PORT'][s]=data_temp['PORT']
               source['Power'][s]=data_temp['Power'] #maynot be needed
               json.dump(source,file3)
     client_thread2=threading.Thread(target=match_load,args=(load,source))
     client_thread2.start()
    

#Thread2
def match_load(load={},source={}):
     loads = int((sum(len(value) for value in load.values()))/4)+1
     #print(f"no of loads={loads-1}")
     sources = int((sum(len(value) for value in source.values()))/4)+1
     #print(f"no of sources={sources-1}")
     for j in range(1,loads):
          if(load['match'][j]==0):
               print(f"[LOAD found]{load['Power'][j]} is the Required power for the load")
               for k in range(1,sources):
                    print(f"[source found], checking its power")
                    if (source['Power'][k]>=load['Power'][j]):
                         print(f'[MATCH found] load {j} has been matched with the source {k}')
                         L_ADDR=(load['IP'][j],load['PORT'][j])
                         S_ADDR=(source['IP'][k],source['PORT'][k])
                         load['match'][j]=1
                         source['Power'][k]= source['Power'][k]-load['Power'][j]
                         with open('source.json','a') as file3:
                              json.dump(source,file3)
                         with open('load.json','a') as file2:
                              json.dump(load,file2)
                         print(f"load{L_ADDR} Source{S_ADDR}")
                         client_thread3=threading.Thread(target=send_client,args=(L_ADDR,S_ADDR))
                         client_thread3.start()
                         break
                    else:
                         print('source cannot be matched')
          
def send_client(L_ADDR=(),S_ADDR=()):
     msg_format={'type':'SERVER','IP':IP,'PORT':PORT,'msg':0}
     server_send=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     server_send.connect(L_ADDR)
     msg_format['msg']=S_ADDR
     server_send.sendall((json.dumps(msg_format)).encode())

print("[STARTING] server is starting...")
server_start(data,load,source)




