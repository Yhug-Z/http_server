"""
    模拟网站的后端应用

从httpserver接收具体请求
根据请求进行逻辑处理和数据处理
将需要的数据反馈给httpserver
"""
import json
import os
import sys
from select import *
from socket import *


class Application:
    def __init__(self, host, port, debug, static):
        self.__host = host
        self.__port = port
        self.__static = static
        self.__create_socket(debug)
        self.__bind()
        self.__epoll = epoll()
        self.__dict_fdmap = {}

    def start(self):
        self.__sockfd.listen(5)
        print("Listen the port from", self.__port)
        self.__epoll.register(self.__sockfd, EPOLLIN | EPOLLERR)
        self.__dict_fdmap[self.__sockfd.fileno()] = self.__sockfd
        while True:
            try:
                events = self.__epoll.poll()
            except KeyboardInterrupt:
                sys.exit("Thanks")
            for fd, event in events:
                if self.__dict_fdmap[fd] == self.__sockfd:
                    connfd, addr = self.__dict_fdmap[fd].accept()
                    # print(addr)
                    self.__epoll.register(connfd, EPOLLIN | EPOLLERR)
                    self.__dict_fdmap[connfd.fileno()] = connfd
                elif event & EPOLLIN:
                    self.__handle(self.__dict_fdmap[fd])
                    self.__epoll.unregister(fd)
                    del self.__dict_fdmap[fd]
                elif event & EPOLLOUT:
                    pass

    def __handle(self, connfd):
        request = connfd.recv(128).decode()
        request = json.loads(request)
        #print(data){'method': 'GET', 'info': '/'}
        if request["method"]=="GET":
            if request["info"]=="/" or request["info"][-5:]==".html":
                response=self.__get_html(request["info"])
            else:
                # print("---")
                with open(os.path.join(self.__static,"404.html")) as fd:
                    response=json.dumps({"status": "404", "data": fd.read()})

        elif request["method"]=="POST":
            pass
        # response=json.dumps(response)

        connfd.send(response.encode())
        connfd.close()

    def __create_socket(self, debug):
        self.__sockfd = socket()
        self.__sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, debug)

    def __bind(self):
        self.__address = (self.__host, self.__port)
        self.__sockfd.bind(self.__address)

    def __get_html(self, info):
        if info=="/":
            # print(self.__static)
            filename=os.path.join(self.__static,"index.html")
            # print(filename)
        else:
            filename=os.path.join(self.__static,info[1:])
            # print(filename)
        try:
            # print(filename)
            fd=open(filename)
            status="200"
        except :

            fd=open(os.path.join(self.__static,"404.html"))
            status="404"
        finally:
            data=fd.read()
            # print(data)
            fd.close()
            return json.dumps({"status":status,"data":data})
