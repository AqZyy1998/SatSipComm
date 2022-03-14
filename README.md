# 星地融合实验文档

GitHub地址：https://github.com/AqZyy1998/SatSipComm



## 整体实验流程：

1、启动sip server，启动server端程序监听端口；

2、启动客户端，发送请求到server端；

3、上传生成的文件，然后从卫星获取下发文件；

4、下发文件放在Files路径下，名字需要命名为 `ResponseFromServer2`

5、server端会自动下发sip启动脚本，两个client终端启动sip通话，通话成功，实验完成；



## 地面端：

### 实验设备：

两个Linux设备作为客户端进行通话实验，一个Linux系统作为服务端；

### 配置文件：

- config.py文件：

  配置client IP，clientB IP，server IP地址，以及对应端口号；

- Input.py文件：放于client端，用于启动sip通话；

  （注，需要修改文件中路径为pc中sip地址）

- Output.py文件：放于clientB端，用于启动sip通话；

  （注，需要修改文件中路径为pc中sip地址）

### 程序文件：

- client.py文件：Linux系统电脑执行；
- clentB.py文件：Linux系统电脑执行；
- server.py 和 serverB.py文件：这两个文件不需要运行，在服务端Linux系统同时执行，直接执行`multiThread.py`文件会同时启动这两个脚本；

### Files文件夹：

- json文件：传输input.py、output.py文本，代码读取json文件启动这两个脚本；（测试文件，实验环境不使用）
- requestA文件：client ---- clientB 传输日志，携带目标终端IP、serverName；（requestB文件同理）
- ResponseFromServer2文件：卫星传输下来的启动脚本，用于启动sip；功能和json文件相同；
- serverFile文件：待定测试文件；
- serverFileInBinary文件：待定测试文件；
- serverFileInBinaryTransferToJson文件：待定测试文件；
- test文件：遥测文件；
- remote文件：待定测试文件；

### 实验执行步骤：

1、配置静态IP命令：<!--三台设备需要配在同一网关下-->

```shell
--clientA Ip：10.42.0.61
--clientB Ip：10.42.0.62
--server Ip：10.42.0.1
--server PortA: 31500
--server PortB: 31501
```

Ip配置常用指令参考：

```shell
网络配置命令
sudo ifconfig enp0s25 up 
sudo ifconfig enp0s25 down
sudo ifconfig enp0s25 10.42.0.61 netmask 255.255.255.0
route -n
ip route show
sudo route add -net 10.42.0.0/24 dev wlp3s0
route -n
```

2、执行启动脚本

- 启动sip server服务

```shell
启动命令：
cd /usr/local/sbin/
sudo ./opensipsctl start
```

- 启动server程序

```shell
1、先修改启动脚本，client ----- input.py, clientB ----- output.py文件中路径，改为sip client启动路径
2、启动命令：
cd SatSipComm/G
python3 multithread.py
```

- 启动client程序

```shell
1、启动命令
cd SatSipComm/Ground/
python3 Client.py
python3 ClientB.py --在另一台客户端启动
```

<!--注意，需要先执行server端，再执行client端程序；client端两个程序最好同时启动，最后sip启动不要动光标，会影响自动启动；如果不能同时启动sip，可以尝试修改睡眠时间达到启动一致；需要确保所有的执行都是Python3；-->



## 卫星端：

天仪研究院操作