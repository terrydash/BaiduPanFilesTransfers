from bson import ObjectId
from pymongo.errors import AutoReconnect

from common.convert import class2json
from dao.mongodb_conn import mongodb


# 基础数据库访问通用类

def retry_if_auto_reconnect_error(exception):
    """Return True if we should retry (in this case when it's an AutoReconnect), False otherwise"""
    return isinstance(exception, AutoReconnect)


class BaseRepository(object):

    def __init__(self, entity=None, collectionname=''):

        # 初始化要访问的集合
        if (entity is None) and len(collectionname) == 0:
            raise AttributeError('entity 和 collectionName必须指定一个!')
        if entity is not None and hasattr(entity(), 'COLLECTION_NAME'):
            self.collectionName = str(entity().COLLECTION_NAME)
        if len(collectionname) > 0:
            self.collectionName = collectionname
        self.db = mongodb

    # 插入一条记录
    def insert_one(self, entity):
        if type(entity) is dict and '_id' in entity:
            entity.pop('_id')
        if type(entity) is dict and '_COLLECTION_NAME' in entity:
            entity.pop('_COLLECTION_NAME')
        self.db[self.collectionName].insert_one(class2json(entity))
        return entity, 1, '正常'

    def insert_many(self, entities: list):
        entitiesforinsert = []
        for entity in entities:
            if type(entity) is dict and '_id' in entity:
                entity.pop('_id')
            if type(entity) is dict and '_COLLECTION_NAME' in entity:
                entity.pop('_COLLECTION_NAME')
            entitiesforinsert.append(class2json(entity))
        self.db[self.collectionName].insert_many(entitiesforinsert)
        return None, len(entities), '正常'

    def update_by_id(self, _id, entity: dict):

        if type(entity) is dict and '_id' in entity:
            entity.pop('_id')
        if type(entity) is dict and '_COLLECTION_NAME' in entity:
            entity.pop('_COLLECTION_NAME')
        self.db[self.collectionName].update({"_id": ObjectId(str(_id))}, {'$set': entity})
        return entity, 1, '正常'

    def search_no_page(self, query, sort=None):
        if self.collectionName in self.db.list_collection_names():
            sornum = 1
            if sort is not None and sort[0] == "-":
                sornum = -1
            filist = self.db[self.collectionName].find(query)
            if sort is not None and len(sort) > 0:
                filist = filist.sort([(sort[1:], sornum)])
            nums = self.db[self.collectionName].find(query).count()
            resultlist = []
            for x in filist:
                resultlist.append(x)
            return resultlist, nums, '正常'
        return None, 0, '未找到collection'

    # 分页搜索
    def search_page(self, page, pagesize, query, sort):
        if self.collectionName in self.db.list_collection_names():
            sornum = 1
            if sort[0] == "-":
                sornum = -1
            filist = self.db[self.collectionName].find(query)
            if sort is not None and len(sort) > 0:
                filist = filist.sort([(sort[1:], sornum)])
            filist = filist.skip((page - 1) * pagesize).limit(pagesize)
            nums = self.db[self.collectionName].find(query).count()
            resultlist = []
            for x in filist:
                resultlist.append(x)
            return resultlist, nums, '正常'
        return None, 0, '未找到collection'

    # 分页获取所有数据

    def get_all_page(self, page, pagesize, sort):
        if self.collectionName in self.db.list_collection_names():
            sornum = 1
            if sort[0] == "-":
                sornum = -1

            filist = self.db[self.collectionName].find()

            if sort is not None and len(sort) > 0:
                filist = filist.sort([(sort[1:], sornum)])
            filist = filist.skip((page - 1) * pagesize).limit(pagesize)
            nums = self.db[self.collectionName].find().count()
            resultlist = []
            for x in filist:
                resultlist.append(x)
            return resultlist, nums, '正常'
        return None, 0, '未找到collection'

    # 获取所有记录不分页

    def get_all_no_page(self, sort=None):
        if self.collectionName in self.db.list_collection_names():
            if sort is None:
                filist = self.db[self.collectionName].find()
            else:
                filist = self.db[self.collectionName].find().sort(*sort)
            nums = filist.count()
            resultlist = []
            for x in filist:
                resultlist.append(x)

            return resultlist, nums, '正常'
        return None, 0, '未找到collection'

    # 根据id获取所有

    def get_by_id(self, _id):
        if self.collectionName in self.db.list_collection_names():
            result = self.db[self.collectionName].find_one({'_id': ObjectId(str(_id))})

            return result, 1, '正常'
        return None, 0, '未找到collection'

    # 根据id删除一个

    def delete_one_by_id(self, _id):
        if self.collectionName in self.db.list_collection_names():
            self.db[self.collectionName].delete_one({'_id': ObjectId(str(_id))})
            return None, 1, '正常'
        return None, 0, '未找到collection'

    def delete_all(self):
        if self.collectionName in self.db.list_collection_names():
            self.db[self.collectionName].delete_many({})
            return None, 1, '正常'
        return None, 0, '未找到collection'
