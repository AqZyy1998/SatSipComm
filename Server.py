import socket
import time
import _thread as thread
import os
import config
from config import ServerIp, ServerPortA


def readFile(filecontent):
    with open("Files/serverFile", "a+") as f:
        f.write(str(filecontent))


def readResponseFromServer2(ResponseFromServer2):
    if os.path.getsize(ResponseFromServer2) != 0:
        with open(ResponseFromServer2, "r") as f:
            list = f.readlines()
            return list[0]
    else:
        return "###"


def ServerRun():
    address = (ServerIp, ServerPortA)  # 服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)  # 绑定服务端地址和端口
    while True:
        data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址
        data = data.decode()
        data += "serverIp:10.112.244.60" + "\n" + "serverName:Server1" + "\n"

        if not data:
            break
        print('[Received]', data)

        # tempDataRcvFromA = "ClientA:" + data
        thread.start_new_thread(readFile, (data.encode('utf - 8'),))
        # TODO 写入上传文件
        with open("Files/uploadJson", "a+") as f:
            f.write(data)
            f.close()

        while True:
            if os.path.exists("Files/ResponseFromServer2") and os.path.getsize("Files/ResponseFromServer2") == 19:
                config.flags[0] = 1
                config.flags = [config.flags[0], config.flags[1]]
                break
            print("wait for file")
        print("Server ", config.flags)
        time.sleep(2)
        while True:
            if config.flags[1] == 1:
                send = readResponseFromServer2("Files/ResponseFromServer2")
                if send != "###":
                    s.sendto(send.encode(), addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
    s.close()


if __name__ == '__main__':
    ServerRun()

