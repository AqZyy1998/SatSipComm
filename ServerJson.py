import socket,os
import _thread as thread
import config
from config import ServerIp, SatServerIp, ServerJsonPort
import transFileType


def ServerJsonRun():
    address = (SatServerIp, ServerJsonPort)  # 卫星服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        trigger = transFileType.jsonTransferToBinary("Files/serverFile")
        s.sendto(trigger.encode(), address)
        filename, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址
        filename = filename.decode()
        print('[Recieved]', filename)
        os.system(r"python " + filename)  # filename带py
        # startClientSip(filename)
        if trigger == '###':  # 自定义结束字符串
            break
    s.close()