from distutils.log import error
import socket
from sqlite3 import connect
HOST=input("Please input host's ip address: ")
PORT=input("Please input port number: ")
FORMAT='utf-8'
ADDR=(HOST,int(PORT))
count=0
check=False
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.settimeout(5)
def close():
    client.shutdown(socket.SHUT_RDWR)
    client.close()
try:#find error
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Connect status: ERROR")
    client.close()
except OSError:
    print("no such host or root")
    client.close()
except:
    print("Timeout Error!")
    client.close()
else:
    print("Try Connecting.....\n"+"IP Address: "+ HOST+"  Port Number: "+ PORT+"\nConnect status: OK")
    while True:#take in command
        COMMAND=input('client:')
        #POST case.............................
        if COMMAND=='POST':
            client.send(COMMAND.encode(FORMAT))
            while True:
                content=input("client: ")
                count=count+1 #record how many contents have been inputed
                try:
                    client.send(bytes(content,encoding='utf-8'))
                except BrokenPipeError:#if the server turn off suddenly
                    print("Send status: ERROR")
                    client.close()
                else:
                    if content=="#":#end the input
                    #print("Send status: OK")
                        ack=client.recv(4096)
                        ack_str=str(ack, encoding='utf-8')
                        print(ack_str)
                        break
                #client.send(bytes(COMMAND,encoding='utf-8'))
        #READ case.............................
        elif COMMAND=='READ':
            client.send(COMMAND.encode(FORMAT))
            for index in range(count):
                msg=client.recv(4096)
                msg_str = str(msg, encoding='utf-8')
                print(msg_str)
        #QUIT case.............................
        elif COMMAND=='QUIT':
            client.send(COMMAND.encode(FORMAT))
            msg=client.recv(4096)
            msg_str=str(msg, encoding='utf-8')
            if msg_str=='server: OK':
                break
        #other case.............................
        else:
            client.send(COMMAND.encode(FORMAT))
            msg=client.recv(4096)
            msg_str=str(msg, encoding='utf-8')
            print(msg_str)
    client.close()