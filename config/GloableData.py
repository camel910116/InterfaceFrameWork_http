import os

# 数据源表中存放接口的数据表名
ApiSheetName = "API"
# 框架根目录所在绝对路径
baseDir = os.path.dirname(os.path.dirname(__file__))
# 数据文件所在绝对路径
DataFilePath = baseDir + "\\TestData\\InterfaceTestCase.xlsx"


# Test API Sheet
API_name = 2
API_protocol = 3
API_requestUrl = 4
API_requestMothod = 5
API_paramsInfo = 6
API_requestDataFile = 7
API_isExecute = 8

# API TestCase Sheet
TestCase_requestHeaders = 1
TestCase_headersEncrypt = 2
TestCase_requestData = 3
TestCase_bodyEncrypt = 4
TestCase_isExecute = 5
TestCase_responseDecrypt = 6
TestCase_DependDataStore = 7
TestCase_checkPoint = 8

# 存储请求参数中的依赖数据
request_Data = {}
# 存储响应数据中的依赖数据
response_Data = {}
