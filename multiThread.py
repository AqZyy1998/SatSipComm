import threading
import Server, ServerB
from Server import *
from ServerB import *

if __name__ == '__main__':
    thread1 = threading.Thread(target=Server.ServerRun, args=())
    thread2 = threading.Thread(target=ServerB.ServerBRun, args=())
    thread1.start()
    thread2.start()
    while 1:
        pass
