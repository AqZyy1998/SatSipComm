import socket
import os

def createJsonContent():
    ip = "10.112.244.62"
    clientname = "clientB"
    with open("Files/requestA", "w") as f:
        f.write("ip:" + ip + "\n")
        f.write("serverName:" + clientname + "\n")
        f.close()
    return "ip:" + ip + "\n" + "clientName:" + clientname + "\n"


address = ('10.112.244.60', 31501)  # 服务端地址和端口
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    trigger = createJsonContent()
    s.sendto(trigger.encode(), address)
    filename, addr = s.recvfrom(1024)  # 返回数据和接入连接的（服务端）地址
    filename = filename.decode()
    print('[Recieved]', filename)
    os.system(r"python " + filename)  # filename带py
    # startClientSip(filename)
    if trigger == '###':  # 自定义结束字符串
        break
s.close()
