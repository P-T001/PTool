import re

def Re_find(par,str,xs=None):
    '''
    功能：正则查找符合的字符串|
    :param par: 正则表达式|str
    :param str: 目标字符串|str
    :param xs: 修饰符|re.I|re.M
    :return: 符合的字符串列表|list
    '''
    if xs:
        result=re.finditer(par,str,xs)
    else:
        result = re.finditer(par, str)
    new_li=[]
    for r in result:
        new_li.append(r.group())
    return new_li


def Re_change(par,str,change,xs=None):
    '''
    功能：正则替换
    :param par: 正则表达式|str
    :param str: 目标字符串|str
    :param change: 替换字符串|str or def|
    :param xs: 修饰符|re.I|re.M
    :return: 替换后的字符串|str
    '''
    if xs:
        result=re.sub(par,change,str,xs)     #'change可以是函数
    else:
        result = re.sub(par, change, str)
    return result
'''
正则表达式：
身份证：'\d{6}(17|18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)'
    总数：15（old）|18（new）
    6位地区、8出生年月日、3位顺序码、1位校验码
手机号：'(?<=\D)1[34789]\d{9}'
    总数：11位
    3位运行商
    电信：133 / 134-9 / 153/173 / 174-00〜05/177/180/181/189/190/191/193/199
    联通：130/131/132/155/156/166/175/176/185/186/196
    移动：134-0〜8/135/136/137/138/139/150/151/152/157/158/159/172/178/182/183/184/187/188/195/197/198/198
    4位地区
    
IPv4地址：'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)'
    255.255.255.255 最大

域名：'https?://[a-z0-9:.-]+/?'
    http://xxx.com/  or https://xxx.com/ or http://x.x.x.x:xxxx/

'''

if __name__ == '__main__':
    par=r'\d{6}(17|18|19|20)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|X)'
    par1='(?<=\D)1[34789]\d{9}'
    line = '432227198712000012 asdXS 4318287199608230024 13377642748'
    #print(Re_find(par,line))
    print(Re_find(par1,line,re.I|re.M))
