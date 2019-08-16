"""
httpserver v3.0

获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端
"""
import json
import re
import sys
from socket import *
from threading import Thread


class HTTPServer:
    def __init__(self, host, port, frame_ip, frame_port, debug):
        self.__host = host
        self.__port = port
        self.__frame_ip = frame_ip
        self.__frame_port = frame_port
        self.__create_socket(debug)
        self.__bind()

    def server_forever(self):
        self.__sockfd.listen(5)
        print("Start the http server:%d" % self.__port)
        while True:
            try:
                connfd, addr = self.__sockfd.accept()
            except KeyboardInterrupt:
                print("Thanks")
                sys.exit(0)
            client = Thread(target=self.__handle, args=(connfd,))
            client.setDaemon(True)
            client.start()

    def __create_socket(self, debug):
        self.__sockfd = socket()
        self.__sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, debug)

    def __bind(self):
        self.__address = (self.__host, self.__port)
        self.__sockfd.bind(self.__address)

    def __handle(self, connfd):
        request = connfd.recv(1024).decode()
        # print(request)

        pattern = r"(?P<method>^[A-Z]+)\s+(?P<info>/\S*)"
        try:
            env = re.match(pattern, request).groupdict()
            # print(env)
        except:
            connfd.close()
            return
        else:
            data = self.__connect_frame(env)
            # print(data)
            self.__response(connfd, data)

    def __connect_frame(self, env):
        sockfd_frame = socket()
        try:
            sockfd_frame.connect((self.__frame_ip, self.__frame_port))
        except Exception as e:
            print(e)
            return
        else:
            data = json.dumps(env)
            sockfd_frame.send(data.encode())
            data = sockfd_frame.recv(1024 * 1024 * 10).decode()
            return json.loads(data)

    def __response(self, connfd, data):
        if data["status"] == "200":
            respons_headers = "HTTP/1.1 200 OK\r\n"
            respons_line = "Content-Type:text/html\r\n"
            respons_body = data["data"]
            respons = respons_headers + respons_line + "\r\n" + respons_body


        elif data["status"] == "404":
            respons_headers = "HTTP/1.1 404 Not Find\r\n"
            respons_line = "Content-Type:text/html\r\n"
            respons_body = data["data"]
            respons = respons_headers + respons_line + "\r\n" + respons_body

        connfd.send(respons.encode())

