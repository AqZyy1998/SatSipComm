import os
import socket
import transFileType
import base64
from config import SatServerIp, ServerJsonPort


def writeFile(data, address):
    with open(address, "w") as f:
        f.write(data)
    f.close()


def ServerJsonRun():
    address = (SatServerIp, ServerJsonPort)  # 卫星服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        trigger = transFileType.jsonTransferToBinary("Files/serverFile")  # trigger是二进制流
        s.sendto(trigger.encode(), address)
        satBinaryData, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址
        satStrData = base64.b64decode(satBinaryData).decode()  # string类型的input.py\n output.py
        print('[Received]', satStrData)
        writeFile(satStrData, "Files/satJsonData.txt")
        if trigger == '###':  # 自定义结束字符串
            break
    s.close()
