#encoding=utf-8
from util.EncryptUtil import EncryptMD5

def paramsOper(resData, encrypt):
    resData = resData
    if isinstance(resData, dict) and isinstance(encrypt, dict):
        for key, value in encrypt.items():
            # print(value)
            for i in value:
                if i == "md5":
                    resData[key] = EncryptMD5.encrypt_md5(resData[key])
    return resData

if __name__ == "__main__":
    resData = {"username":"wcx","password":"wcx123wac"}
    encrypt = {"password":["md5"]}
    print(paramsOper(resData, encrypt))