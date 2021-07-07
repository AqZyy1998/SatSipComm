from config import ServerIp, SatServerIp, ServerRemotePort, ObcPort, ObcIp
import socket
import _thread as thread
import base64
import os
import time
import numpy
import transFileType


class RemoteObject:
    def __init__(self):
        self.runNum = numpy.uint8(0)
        self.hasInputFile = numpy.uint8(0)
        self.isDecode = numpy.uint8(0)
        self.isEncode = numpy.uint8(0)
        self.hasOutputFile = numpy.uint8(0)
        self.inputFileLen = numpy.uint8(0)
        self.encodeFileLen = numpy.uint8(0)


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


def writeFileFromSatToGround(data, address):
    with open(address, "a") as f:
        f.write(data)
    f.close()


def readRemoteFile(address):
    with open(address, "r") as f:
        remoteInfo = f.read()
        return remoteInfo


def writeRemoteFile(address, remoteInfo):
    try:
        with open(address, "a") as f:
            f.write(remoteInfo)
    except IOError:
        return False
    else:
        return True


def isJsonOK(address, remoteObject):
    if not os.path.exists(address):
        return remoteObject
    if not os.path.getsize(address) == 19:
        return remoteObject
    remoteObject.hasOutputFile = numpy.uint8(1)
    remoteObject.encodeFileLen = numpy.uint(19)
    print("RECEIVE JSON SUCCESSFULLY")
    return remoteObject


def transferRemoteToStr(remoteObject):
    remoteInfo = numpy.uint32(0)
    remoteInfo = numpy.uint32(remoteObject.runNum << 24) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.hasInputFile << 22) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.isDecode << 20) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.isEncode << 18) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.hasOutputFile << 16) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.inputFileLen << 8) | remoteInfo
    remoteInfo = numpy.uint32(remoteObject.encodeFileLen) | remoteInfo
    return remoteInfo
    
    
def SatServerRemoteRun():
    time_start = time.time()
    address = (ObcIp, ObcPort)  # OBC地址和端口
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)
    remoteObject = RemoteObject()  # 新建对象
    while True:
        time_run = time.time() - time_start
        remoteFileName = "Files/remote"
        if time_run > 5:  # 超过60s发json包
            jsonFileName = "Files/json"
        else:
            jsonFileName = "Files/jsonBackup"
        # remoteInfo = readRemoteFile(remoteFileName)
        remoteObject = isJsonOK(jsonFileName, remoteObject)  # 处理遥测包信息

        remoteInfo = transferRemoteToStr(remoteObject)  # 封装遥测包
        if writeRemoteFile(remoteFileName, str(remoteInfo)):
            try:
                send2 = int(remoteInfo)
                sendToData = send2.to_bytes(length=4, byteorder='big', signed=False)
                # print(send2, remoteInfo, sendToData)
                s.sendto(sendToData, address)
            except IOError:
                print("SENDTO ERROR")
            # else:
            #     remoteObject.runNum += 1
        else:
            print("WRITE ERROR")
    s.close()

# def SatServerRemoteRunBackup():
#     address = (SatServerIp, ServerRemotePort)  # 卫星服务端地址和端口
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.bind(address)  # 绑定服务端地址和端口
#     while True:
#         # data, addr = s.recvfrom(1024)  # 返回数据和接入连接的（客户端）地址 data是string
#         # data = str(data, 'utf - 8')
#         # if not data:
#         #     break
#         # print('[Received]', data)
#
#         # 遥测包判断
#         data = isJsonOK("Files/remote")
#
#         # TODO 处理遥测包信息
#         # writeContent = "input.py\noutput.py\n"
#         # writeFileFromSatToGround(writeContent, "Files/ResponseFromServer2")
#         ObcAddress = (ObcIp, ObcPort)
#         s2obc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s2obc.bind(ObcAddress)
#         # send = readResponseFromServer2("Files/ResponseFromServer2")  # send = input.py\n output.py
#         send = transferJsonToBinary(data)
#         if send != "###":
#             s2obc.sendto(send, addr)  # UDP 是无状态连接，所以每次连接都需要给出目的地址
#     s.close()


if __name__ == '__main__':
    SatServerRemoteRun()
