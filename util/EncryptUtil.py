#encoding=utf-8
import hashlib

class EncryptMD5(object):
    def __init__(self):
        pass

    '''classmethod是用来指定一个类的方法为类方法,cls代表这个类本身。
    这样的好处就是你以后重构类的时候不必要修改构造函数，只需要额外添加你要处理的函数，然后使用装饰符 @classmethod 就可以了
    这种类方法在构造函数之前执行'''
    @classmethod
    def encrypt_md5(cls,data):
        """
        :函数功能: 实现MD5加密
        :参数:
            text: string，被加密的内容
        :返回值: string，加密后的内容
        """
        m5 = hashlib.md5()
        m5.update(data.encode('utf-8'))
        return m5.hexdigest()

if __name__ == '__main__':
    ee =EncryptMD5()
    print(ee.encrypt_md5('abcd12345'))