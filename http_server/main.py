"""
    http server 入口
"""

from config import HOST, PORT, DEGUB,frame_ip,frame_port
from http_server import HTTPServer

if __name__ == '__main__':
    httpd = HTTPServer(HOST, PORT,frame_ip,frame_port, DEGUB)
    httpd.server_forever()
