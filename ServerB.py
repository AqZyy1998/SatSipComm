import socket,os
import _thread as thread

def readFile(filecontent):
    with open("Files/serverFile", "a+") as f:
        f.read()
        f.write(str(filecontent))


def readResponseFromServer2(ResponseFromServer2):
    if os.path.getsize(ResponseFromServer2) != 0:
        with open(ResponseFromServer2, "r") as f:
            list = f.readlines()
            return list[1]
    else:
        return "###"


global flagB
flagB = bool(False)
address = ('10.112.244.60', 31501)  # 服务端地址和端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)  # 绑定服务端地址和端口
while True:
    data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址
    data = data.decode()

    if not data:
        break
    print('[Received]', data)

    # tempDataRcvFromB = "ClientB:" + data
    thread.start_new_thread(readFile, (data.encode('utf - 8'),))

    flagB = bool(True)
    global flagA
    while True:
        if flagA == bool(True) and flagB == bool(True):
            send = readResponseFromServer2("Files/ResponseFromServer2")
            if send != "###":
                s.sendto(send.encode(), addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
s.close()
