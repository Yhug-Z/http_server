"""
    web_frame 运行入口

"""
from settings import HOST, PORT, DEBUG,STATIC_DIR

from web_frame import Application

if __name__ == '__main__':
    app = Application(HOST, PORT, DEBUG,STATIC_DIR)
    app.start()
