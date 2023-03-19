import json
import re
from enum import Enum

from bson import ObjectId
from bson.json_util import loads


class Config:
    def __setattr__(self, key, value):
        self.__dict__[key] = value


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def redisstr2list(redisstr: str):
    redisstr = re.sub('\'', '\"', redisstr)

    return loads(redisstr)


def dict2class(mydict):  # 实现列表转实体类
    m = Config()
    for x in mydict:
        if isinstance(mydict[x], dict):
            # #print(mydict[x])
            a = dict2class(mydict[x])
            m.__setattr__(x, a)
        else:
            m.__setattr__(x, mydict[x])
    return m


def class2json(c):
    if isinstance(c, dict):
        return dict2json(c)
    elif isinstance(c, list):
        nlist = []
        for x in c:
            nlist.append(class2json(x))
        return nlist
    o = Config()
    if hasattr(c, '__dict__'):
        for key in c.__dict__:
            if str(key).upper().startswith('_'):
                continue
            if isinstance(c.__getattribute__(key), Enum):
                setattr(o, key, c.__getattribute__(key).value)
            elif isinstance(c.__getattribute__(key), bytes) or isinstance(c.__getattribute__(key), ObjectId):
                setattr(o, key, str(c.__getattribute__(key)))
            elif isinstance(c.__getattribute__(key), dict):
                setattr(o, key, class2json(c.__getattribute__(key)))
            elif isinstance(c.__getattribute__(key), list):
                r = []
                for x in c.__getattribute__(key):
                    rest = class2json(x)
                    r.append(rest)
                setattr(o, key, r)
            elif isinstance(c.__getattribute__(key), int):
                setattr(o, key, int(c.__getattribute__(key)))
            elif isinstance(c.__getattribute__(key), str):
                setattr(o, key, str(c.__getattribute__(key)))
            elif isinstance(c.__getattribute__(key), bool):
                setattr(o, key, c.__getattribute__(key))
            else:
                setattr(o, key, class2json(c.__getattribute__(key)))
    return o.__dict__


def dict2json(c):
    d = c
    if isinstance(c, dict):
        for (k, v) in c.items():

            if isinstance(v, ObjectId):

                d[k] = str(v)
            elif isinstance(v, int):
                d[k] = int(v)
            elif isinstance(v, dict):
                d[k] = class2json(v)
            elif isinstance(v, list):
                vlist = []
                for _vlist in v:
                    __vlist = class2json(_vlist)
                    vlist.append(__vlist)
                d[k] = vlist
    return d
