from config import ServerIp, SatServerIp, ServerJsonPort
import socket
import _thread as thread
import base64
import os
import transFileType


def transferBinaryToJson(BinaryData):  # 输入其实为string类型
    binaryContent = BinaryData.encode('utf - 8')
    print(binaryContent)
    # base64转成json
    jsonContent = base64.b64decode(binaryContent)
    return jsonContent


def transferJsonToBinary(JsonData):
    binaryContent = base64.b64encode(JsonData.encode('utf - 8'))
    print(binaryContent)
    return binaryContent
    # binaryContent = str(encodestr, 'utf - 8')


def readResponseFromServer2(ResponseFromServer2):
    if os.path.getsize(ResponseFromServer2) != 0:
        with open(ResponseFromServer2, "r") as f:
            list = ''.join(f.readlines())
        binaryData = transferJsonToBinary(list)
        return binaryData
    else:
        return "###"


def SatServerJsonRun():
    address = (SatServerIp, ServerJsonPort)  # 卫星服务端地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)  # 绑定服务端地址和端口
    while True:
        data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址 data是string
        data = data.decode()
        if not data:
            break
        print('[Received]', data)
        # TODO 处理地面发来的数据
        JsonData = transferBinaryToJson(data)

        send = readResponseFromServer2("Files/ResponseFromServer2")  # send = input.py\n output.py
        if send != "###":
            s.sendto(send, addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
    s.close()
