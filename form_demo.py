#-- coding: utf - 8 - -
import os
import pandas as pd

'''
xls: pip install xlwt,xlrd 
xlsx: pip install openpyxl
csv : csv (默认就有)
'''

def Save_csv(filename,data,mode,encoding='utf-8'):
    '''
    功能：保存csv数据，支持data格式
        {'字段名1':[数据1,数据3],'字段名2':[数据2,数据4]}
        [{'字段名1':数据1,'字段名2':数据2,},{'字段名1':数据3,'字段名2':数据4,}]
        [['字段名1','字段名2'],[数据1,数据2],[数据3,数据4]]
    表格数据：    字段名1 字段名2
                数据1  数据2
                数据3  数据4
    :param filename:文件名
    :param data:数据
    :param mode:写入模式w/a
    :param encoding:文件编码
    :return:
    '''
    if os.path.splitext(filename)[1]=='.csv':
        try:
            if isinstance(data,dict) and isinstance(list(data.values())[0],list):
                df = pd.DataFrame(data)
                header = list(data.keys())
            elif isinstance(data,list) and isinstance(data[0],dict):
                df = pd.DataFrame(data)
                header = list(data[0].keys())
            elif isinstance(data,list) and isinstance(data[0],list):
                df = pd.DataFrame(data[1:])
                header = data[0]
            else:
                raise RuntimeError('没有这个类型')
            if mode == 'a':
                if not os.path.exists(filename):
                    df.to_csv(filename, index=False, mode=mode, header=header, encoding=encoding)
                else:
                    df.to_csv(filename, index=False, mode=mode, encoding=encoding,header=False)
            elif mode == 'w':
                df.to_cdf.to_csv(filename, index=False, mode=mode, header=header, encoding=encoding)
        except RuntimeError as R_error:
            print(R_error)
        except Exception as E_error:
            print('运行error|%s'%E_error)
    else:
        print('不支持该文件类型')

def Read_file(filename, encoding='utf-8'):
    '''
    功能：读取表格（.xls/.xlsx/.csv）文件，返回list_dict格式
    :param filename: 文件路径名
    :return:
    '''
    hz = os.path.splitext(filename)[1]
    if hz == '.xls' or hz == '.xlsx':
        data = pd.read_excel(filename)
    elif hz == '.csv':
        data = pd.read_csv(filename, encoding=encoding)
    else:
        data = None
        exit()
    headers = list(data.keys())
    rows = data.values.tolist()
    li = []
    for row in rows:
        li.append(dict(zip(headers, row)))
    return li

def Read_FD(filename,size):
    '''
    功能：单文件csv分段
    :param filename: 文件名路径|str
    :param size:分割大小，单位行|int
    :return:
    '''

    if os.path.splitext(filename)[1] == '.csv':
        try:
            data = pd.read_csv(filename, chunksize=size)
            for num,d in enumerate(data):
                new_filename='%s-%s.csv'%(os.path.splitext(filename)[0],str(num))
                df=pd.DataFrame(d)
                df.to_csv(new_filename,index=False)
        except:
            print('文件分割失败|filename:%s'%filename)
    else:
        print('不支持该文件类型')






# ---
# di = {'name1': ['aaa', 'bbb'], 'age': ['18', '19']}
# di_dic={"0":{'字段名1':'数据1','字段名2':'数据2',},"1":{'字段名1':'数据3','字段名2':'数据4',}}
# li = [['name', 'age'], ['aaa', '16'], ['bbb', '16'], ['ccc', '16']]
# dic2={'name1': 'aaa','age':'111'}
# dic = [{'name1': 'aaa%d' % i} for i in range(0, 3333)]
# df = pd.DataFrame(di_dic)
# header=list(dict(di_dic.values()).keys())
# df.to_csv(filename, index=False, mode='a', header=header)  # index=False 关闭索引，header=False 关闭表头，有则使用
if __name__ == '__main__':
    # filename='./xx/x1/xx.csv'
    # print(os.path.splitext(filename)[0])
    Read_FD('cms_result.csv',100)
