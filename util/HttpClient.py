#encoding=utf-8
import requests
import traceback
import urllib

class HttpClient(object):
    def __init__(self):
        pass

    def request(self, requestMethod, requesturl, paramMethod = None, requestData = None, headers = None, **kwargs):
        print ("----", requestMethod, requesturl, paramMethod, requestData, headers)
        try:
            if requestMethod.lower() == "post":
                # print ("++++++++++++")
                return self.__post(paramMethod, requesturl, requestData = requestData, headers = headers, **kwargs)
            elif requestMethod == "get":
                return self.__get(requestUrl = requesturl, params = requestData, **kwargs)
        except Exception as e:
            print(traceback.format_exc())

    # 私有方法
    def __post(self, paramMethod, requestUrl, requestData = None, headers = None, **kwargs):
        try:
            if paramMethod == "form" or "data":
                # print ("===========")
                # print (type(requestData))
                responseObj = requests.post(requestUrl, data = requestData, headers = headers, timeout = 3)
                return responseObj
            elif paramMethod == "json":
                responseObj = requests.post(requestUrl, json = requestData, headers = headers, timeout = 3)
                return responseObj
            elif paramMethod == "url":
                url = ""
                if isinstance(requestData, str):
                    # urllib.quote_plus方法将数据编码成浏览器能识别的字符
                    url = requestUrl + "?%s" %urllib.quote_plus(requestData)
                # elif isinstance(requestData, dict):
                #     url = requestUrl + "?%s=%s" %(requestData.keys()[0], requestData.values()[0])
                responseObj = requests.post(url, headers = headers, **kwargs)
                return responseObj
        except Exception as e:
            print(traceback.format_exc())

    def __get(self, requestUrl, params = None, **kwargs):
        try:
            url = requestUrl
            if params:
                responseObj = requests.get(url=url, params=params,**kwargs)
            return responseObj
        except Exception as e:
            print(traceback.format_exc())

if __name__ == '__main__':
    hh =HttpClient()

