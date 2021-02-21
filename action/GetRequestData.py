from util.ParseExcel import ParseExcel
from config.GloableData import *
from action.ParamsOper import *
from action.DataStore import *
import random, json, ast
from util.HttpClient import HttpClient

class GetRequestData(object):
    def __init__(self, filePath):
        # 创建解析Excel工具类的实例对象
        self.parseEx = ParseExcel()
        # 将数据文件Excel加载到内存
        self.parseEx.loadWorkBook(filePath)
        self.apiSheetFileName = ""
        self.apiName = ""
        self.requestMethod = ""
        self.requestUrl = ""
        self.paramsInfo = ""
        self.reponseDataStore = {}
        self.CheckPoint = {}


    def getApi(self):
        # 通过Excel工具类中提供的getSheetByName方法获取数据文件中存放api工作表的对象
        apiSheetObject = self.parseEx.getSheetByName(ApiSheetName)
        # 获取api表中是否需要执行列对象
        isExecColObj = self.parseEx.getColumn(apiSheetObject, API_isExecute)
        # print('isExecColObj=',isExecColObj)
        for idx, col in enumerate(isExecColObj[1:]):
            print('idx=',idx)
            if col.value == "y":
                # 如果单元格的值为y，说明该行的api需要被执行

                # 依次获取需要执行api的行对象，以便拿到请求api的相关数据
                rowObj = self.parseEx.getRow(apiSheetObject, idx + 2)
                # API_name等变量定义在GloableData里面
                self.apiName = rowObj[API_name - 1].value
                self.requestUrl = rowObj[API_requestUrl - 1].value
                self.requestMethod = rowObj[API_requestMothod - 1].value
                self.paramsInfo = rowObj[API_paramsInfo - 1].value
                apiTestCasefileName = rowObj[API_requestDataFile - 1].value
                print(self.apiName, self.requestUrl, self.requestMethod, self.paramsInfo, apiTestCasefileName)
                self.getTestCase(apiTestCasefileName)
            else:
                print(u"接口【" + rowObj[API_name - 1].value + u"】被忽略执行")

    def getTestCase(self, testCaseSheetName):
        try:
            # 根据测试用例sheet名获取sheet对象
            testCaseObj = self.parseEx.getSheetByName(testCaseSheetName)
            # 获取测试用例表中是否执行列对象
            isExeccolObj = self.parseEx.getColumn(testCaseObj, TestCase_isExecute)
            for t_idx, t_col in enumerate(isExeccolObj[1:]):
                # 依次遍历测试用例表中的测试用例行，需要执行则执行
                if t_col.value == "y":
                    # 如果测试用例单元格值为y，说明该行测试用例需要被执行
                    rowObj = self.parseEx.getRow(testCaseObj, t_idx + 2)
                    RequestHeaders = rowObj[TestCase_requestHeaders - 1].value
                    HeadersEncrypt = rowObj[TestCase_headersEncrypt - 1].value
                    RequestData = rowObj[TestCase_requestData - 1].value
                    # 如果没有内容，得到的将是None，如果有内容，根据我们自己定义的规则，得到将是一个字符串字典类型数据"{xxx}"
                    BodyEncrypt = rowObj[TestCase_bodyEncrypt - 1].value

                    ResponseDecrypt = rowObj[TestCase_responseDecrypt - 1].value
                    DependDataStore = rowObj[TestCase_DependDataStore - 1].value
                    self.CheckPoint = rowObj[TestCase_checkPoint - 1].value
                    print(RequestHeaders, RequestData, DependDataStore, self.CheckPoint)

                    RequestHeaders = ast.literal_eval(RequestHeaders) if (RequestHeaders) else None
                    RequestData = ast.literal_eval(RequestData) if (RequestData) else None
                    print('111111111111',type(RequestData))
                    HeadersEncrypt = ast.literal_eval(HeadersEncrypt) if (HeadersEncrypt) else None
                    BodyEncrypt = ast.literal_eval(BodyEncrypt) if (BodyEncrypt) else None

                    if BodyEncrypt and RequestData:
                        # 对请求参数进行加密处理，如果需要的话
                        RequestData = paramsOper(RequestData, BodyEncrypt)
                        print("sdfd = ", type(RequestData))
                    if HeadersEncrypt and RequestHeaders:
                        # 对头信息进行加密处理，如果需要的话
                        RequestHeaders = paramsOper(RequestHeaders, HeadersEncrypt)
                        print(RequestHeaders)
                    # 数据存储
                    if DependDataStore:
                        DependDataStore = ast.literal_eval(DependDataStore)
                        if isinstance(DependDataStore, dict) and "request" in DependDataStore:
                            requestDataStore = {"request": DependDataStore["request"]}

                            d = DataStore()
                            print ("sdfd = ", type(RequestData))
                            # storage(self, fileName, ApiName, sourceData, sourceDataIndex, needStoreData)
                            d.storage(ApiSheetName, self.apiName, RequestData, t_idx + 1, requestDataStore)
                        elif isinstance(DependDataStore, dict) and "response" in DependDataStore:
                            self.reponseDataStore = {"response": DependDataStore["response"]}
                        else:
                            print(u"存储数据数据规则错误")
                    else:
                        print(u"不需要存储依赖数据")
                    # 处理完请求参数以及依赖数据存储后，接下来该发送接口请求了
                    self.sendRequest(RequestData, RequestHeaders, t_idx + 1)
                else:
                    print(u"测试用例文件【" + testCaseSheetName + "】中第%d条用例被忽略执行" %(t_idx + 1))
        except Exception as e:
            raise e

    def sendRequest(self, RequestData, RequestHeaders, index):
        dataFormat, paramType, dataOper = "", "", ""
        res = self.paramsInfo.split("_")
        if len(res) == 3:
            dataFormat, paramType, dataOper = res
        elif len(res) == 2:
            dataFormat, paramType = res
            print('dataFormat, paramType=',dataFormat, paramType)
        elif len(res) == 1:
            dataFormat = res[0]
            print('dataFormat=',dataFormat)
        if dataOper == "json":
            RequestData = json.dumps(RequestData)
        elif dataFormat =='data':
            if type(RequestData) == str:
                RequestData = ast.literal_eval(RequestData)

        httpC = HttpClient()
        # requestMethod, requesturl, paramMethod = None, requestData = None, headers = None, ** kwargs
        responseObj = httpC.request(self.requestMethod,self.requestUrl, paramType, RequestData, RequestHeaders, timeout = 10)
        print(responseObj.json())
        print(responseObj.text)
        print(type(responseObj.text))
        self.ReponseDataStore(responseObj.text, index)

    def ReponseDataStore(self, responseObj, index):
        if self.reponseDataStore:
            d = DataStore()
            # fileName, ApiName, sourceData, sourceDataIndex, needStoreData
            if type(responseObj) == str:
                RequestData = ast.literal_eval(responseObj)
            d.storage(ApiSheetName, self.apiName, responseObj, index, self.reponseDataStore)
        checkPoint = ast.literal_eval(self.CheckPoint) if self.CheckPoint else {}



if __name__ == "__main__":
    grd = GetRequestData(DataFilePath)
    grd.getApi()


