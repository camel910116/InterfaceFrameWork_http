#encoding=utf-8
from config.GloableData import request_Data, response_Data
'''testdata.xlsx中有DependDataStore这个依赖字段，这个字段是以字典形式存储的，这个字典中的value应该是request字典或者response数据字典中的key
在__findData这个私有方法中，第一个参数就是我们的requestData或者responseData，第二个参数就是excel表格里面的DependDataStore字典中value值
因为会有字典嵌套的情况，所以递归处理找到这个key，然后将这个key对应的值传给foundData类变量
在stronge函数中通过调用__findData已经取到了想要的值，接下来用{“excel表格名>表格中API名字->案例名”：foundData}格式存储下来'''

class DataStore(object):
    # 类变量，用于在递归过程中存储找到的数据
    foundData = None

    def __findData(self, sourceDict, find):
        # 在字典对象中递归查找需要被存储的数据
        if DataStore.foundData is not None:
            return
        if isinstance(sourceDict, dict):
            if find in sourceDict:
                DataStore.foundData = sourceDict[find]
            else:
                for v in sourceDict.values():
                    self.__findData(v, find)
        else:
            return

    def storage(self, fileName, ApiName, sourceData, sourceDataIndex, needStoreData):
        """
        :函数功能: 存储依赖数据到内存中
        :参数:
            ApiName: string，接口名字，用于区分不同接口
            sourceDataDict: dict，存有将要被存储的数据的字典对象
            sourceDataIndex: int，源数据的索引号，用于区分用一个接口的不同数据源
            needStorage: dict，指明将要存储的数据
        :返回值: 无
        """
        print ("----", type(sourceData), type(needStoreData))
        if isinstance(sourceData, dict) and isinstance(needStoreData, dict):
            # needStoreData = {"request": ["username", "password"], "response": ["userid"]}
            for key, value in needStoreData.items():
                for v in value:
                    # 循环找到字典中value值然后调用私有方法__findData
                    DataStore.foundData = None
                    # 查找需要被存储的数据
                    self.__findData(sourceData, v)
                    if DataStore.foundData is not None:
                        if key == "request":
                            if fileName + "->" + ApiName + "->" + str(sourceDataIndex) in request_Data:
                                request_Data[fileName + "->" + ApiName + "->" + str(sourceDataIndex)][v] = DataStore.foundData
                                '''{'blog->wcx->2': {'userId': '54215615', 'name': 'wcx'}}
                                    拿这个字典举例说明，request_Data[fileName + "->" + ApiName + "->" + str(sourceDataIndex)]取到的是{'userId': '54215615', 'name': 'wcx'}
                                    {'userId': '54215615', 'name': 'wcx'}[v]=DataStore.foundData则是如果v存在与字典中则更新，不存在则新增一个key:value组合'''
                            else:
                                request_Data[fileName + "->" + ApiName + "->" + str(sourceDataIndex)] = {v: DataStore.foundData}
                        elif key == "response":
                            if fileName + "->" + ApiName + "->" + str(sourceDataIndex) in response_Data:
                                response_Data[fileName + "->" + ApiName + "->" + str(sourceDataIndex)][v] = DataStore.foundData
                            else:
                                response_Data[fileName + "->" + ApiName + "->" + str(sourceDataIndex)] = {v: DataStore.foundData}
                    else:
                        print (u"源数据（%s）中未找到需要存储的依赖数据（%s）。" %(key, v))
        else:
            print (u"数据格式不满足规则")
        print (request_Data, response_Data)

if __name__ == "__main__":
    s = {"data": {"common":
                      {"userId": "54215615", "userSession": "6829c6e9f8222b5477f559a915e93216", "mid": "0","test1": "2e7d635ba23991aef59c842be542124f", "cityCode": "31000",
                       "test": {"name": "wcx"}},
                  "data":
                      {"ids": "", "category": "", "brand": "", "keyword": "","order": "mer_sellcount---string---desc", "page": "1", "perPage": "10"}}}
    t = {"request": ["userId", "name"],"response": ["ids", "perPage", "wcx"]}
    # a1 = {"response":["userid"]}
    # a = {u'code': u'00', u'userid': 19}
    d = DataStore()
    # d.storage("Cart", "test", a, 2, a1)
    d.storage("blog", "wcx", s, 2, t)