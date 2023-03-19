# -*- coding:utf-8 -*-
import logging
import os

from common.utils import PathUtil

log_path = os.path.join(PathUtil.rootPath, "logs")
if not os.path.exists(log_path):
    os.makedirs(log_path)


class Logger:
    def __init__(self, loggername):
        # 创建一个logger
        self.logger = logging.getLogger(loggername)

        handler1 = logging.StreamHandler()
        handler2 = logging.FileHandler(filename=os.path.join(log_path, "debug.log"))

        self.logger.setLevel(logging.DEBUG)
        handler1.setLevel(logging.DEBUG)
        handler2.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler1.setFormatter(formatter)
        handler2.setFormatter(formatter)

        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)

        # 分别为 10、30、30
        # print(handler1.level)
        # print(handler2.level)
        # print(logger.level)

    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger


hslogger = Logger("hsgame").get_log()
floggger = Logger("fgame").get_log()
