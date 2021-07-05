import socket,os
import _thread as thread
import config


def ServerBRun():
    address = ('10.112.244.60', 31503)  # 服务端地址和端口
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

        config.flags[1] = 1
        config.flags = [config.flags[0], config.flags[1]]
        print("Server B ", config.flags)
        while True:
            if config.flags[0] == 1:
                send = readResponseFromServer2("Files/ResponseFromServer2")
                if send != "###":
                    s.sendto(send.encode(), addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
    s.close()