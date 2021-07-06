import threading
import Server, ServerB, ServerJson, ServerRemote, SatServerJson, SatServerRemote
from Server import *
from ServerB import *

if __name__ == '__main__':
    thread1 = threading.Thread(target=Server.ServerRun, args=())
    thread2 = threading.Thread(target=ServerB.ServerBRun, args=())
    thread3 = threading.Thread(target=ServerJson.ServerJsonRun, args=())
    thread4 = threading.Thread(target=ServerRemote.ServerRemoteRun, args=())
    thread5 = threading.Thread(target=SatServerJson.SatServerJsonRun, args=())
    thread6 = threading.Thread(target=SatServerRemote.SatServerRemoteRun, args=())
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    while 1:
        pass
