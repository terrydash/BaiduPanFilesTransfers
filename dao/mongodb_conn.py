#!/usr/bin/env python
# -*- coding:utf-8 -*-
from pymongo import MongoClient
from pymongo.errors import AutoReconnect
from retrying import retry

from config.mongodb_config import mongodb


def retry_if_auto_reconnect_error(exception):
    """Return True if we should retry (in this case when it's an AutoReconnect), False otherwise"""
    return isinstance(exception, AutoReconnect)


class MongoDB(object):

    def __init__(self):
        count = 0
        while True:
            self.conn = MongoClient(host=mongodb.get("ip"), port=mongodb.get("port"), connect=True,
                                    minPoolSize=0, maxPoolSize=200, connectTimeoutMS=400000, retryWrites=True,
                                    maxIdleTimeMS=10 * 60 * 1000)
            self.db = self.conn[mongodb.get("db")]
            try:
                self.db = self.conn["admin"]
                self.connecter = self.db.authenticate(mongodb.get("username"), mongodb.get("password"))
                self.db = self.conn[mongodb.get("db")]
                self.conn.admin.command("ping")
                break
            except Exception as e:
                count = count + 1
                self.connecter = False
                conn_result = str(e)
                print("连接失败,连接了", count, "次", "错误:", conn_result)
            if count >= 3:
                break

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@retry
def mongoconn():
    return MongoDB().db


mongodb = mongoconn()
