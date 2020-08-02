import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
cur_db = None
cur_col = None


def initMongo():
    return myclient


def addDB(db_name):
    global cur_db
    dblist = myclient.list_database_names()
    for db in dblist:
        if db == db_name:
            cur_db = myclient[db_name]
            return
    cur_db = myclient[db_name]
    print("数据库创建完成:" + cur_db.name)


def addCollect(collect_name):
    global cur_col
    if cur_db:
        collects = cur_db.list_collection_names()
        for col in collects:
            if col == collect_name:
                cur_col = cur_db[collect_name]
                return
        cur_col = cur_db[collect_name]
        print("数据表创建完成:" + cur_col.name)
        # cur_col.create_index([("日期", 1)], unique=True, background=True)
    else:
        print("请先创建数据库!")


def insert(sql, isMulti=False):
    if isMulti:
        cur_col.insert_many(sql)
    else:
        cur_col.insert_one(sql)


def find(sql=None, filterField=None, isMulti=False):
    if isMulti:
        # 查找所有数据
        return cur_col.find(sql, filterField)
    else:
        # 查找一条数据
        return cur_col.find_one()

    # 需要返回字段设置为1，否则设置为0
    # 除了 _id 你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1
    # cur_col.find({}, {"name": 1, "age": 0})
    # 使用sql来选择,并限制返回最大条数为3
    # sql = {"name": "weicong"}
    # 使用正则，配置name首字母为R的记录
    # sql_reg = {"name": {"$regex": "^R"}}
    # cur_col.find(sql).limit(3)
    # 升序
    # cur_col.find(sql).sort("alexa")
    # 降序
    # cur_col.find(sql).sort("alexa", -1)


def update(query_sql, update_sql, isMulti=False):
    if isMulti:
        cur_col.update_many(query_sql, update_sql)
    else:
        cur_col.update_one(query_sql, update_sql)


def delete(sql, isMulti=False):
    if isMulti:
        cur_col.delete_many(sql)
    else:
        cur_col.delete_one(sql)


def drop():
    # 删除集合
    cur_col.drop()
