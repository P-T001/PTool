# -- coding: utf-8 --
import os
import pandas as pd

'''
xls: pip install xlwt,xlrd 
xlsx: pip install openpyxl
csv : csv (默认就有)
'''




def FD_data(data_li, fd_len):
    '''
    功能：对数据进分段列表输出
    :param data_li: 数据列表|list|例：[[1],[2],[3],[4]] or [{1},{2},{3},{4}]
    :param fd_len: 分段长度|int|例：2
    :return:  返回|list|例：[  [[1],[2]] , [[3],[4]] ]  or [ [{1},{2}] ,[{3},{4}] ]
    '''
    try:
        new_li = []
        for i in range(0, len(data_li), fd_len):
            new_li.append(data_li[i:i + fd_len])
        return new_li
    except Exception as E:
        print('分段失败：{}'.format(E))

def CH(df, filename, header, mo):
    '''
    功能：针对文件名后缀处理数据
    :param df: df对象|
    :param filename: 文件名|str|
    :param header: 字段名|list|
    :param mo: 打开文件方式|str|
    :return:
    '''

    hz = os.path.splitext(filename)[1]
    if hz == '.xlsx' or hz == '.xls':
        if mo == 'a':
            if not os.path.exists(filename):
                df.to_excel(filename, index=None, columns=header)
            else:
                old_data = pd.read_excel(filename)
                new_data = pd.concat([old_data, df], axis=0)
                new_data.to_excel(filename, index=None)
        elif mo == 'w':
            df.to_excel(filename, index=None, columns=header)
    elif hz == '.csv':
        if mo == 'a':
            if not os.path.exists(filename):
                df.to_csv(filename, index=False, mode=mo, header=header)
            else:
                df.to_csv(filename, index=False, mode=mo, header=None)
        elif mo == 'w':
            df.to_csv(filename, index=False, mode=mo, header=header)

            
def To_list_dict(data):
    '''
    功能：将三种数据格式，转换成字典|
    :param filename:文件名 |
    :param data: 数据|{'字段名1':['第一行数据1','第二行数据1'],'字段名2':['第一行数据2','第二行数据2']} or
                    [['字段名1','字段名2'],['第一行数据1','第二行数据1']] or
                    [{'字段名1':'第一行数据1','字段名2':'第一行数据2'},{'字段名1':'第二行数据1','字段名2':'第二行数据2'}]
    :return:[{'字段名1':'第一行数据1','字段名2':'第一行数据2'},{'字段名1':'第二行数据1','字段名2':'第二行数据2'}]
    '''
    if isinstance(data, dict):
        if isinstance(list(data.values())[0], list):  # {'':[],'':[]}
            header = list(data.keys())
            dfs = pd.DataFrame.from_dict(data)
            dfs.columns = header
            news_data = list(dfs.values.tolist())
            result = [dict(zip(header, d)) for d in news_data]
            return result
    elif isinstance(data, list):
        if isinstance(data[0], list):  # [[],[]]
            header = data[0]
            dfs = pd.DataFrame(data[1:])
            dfs.columns = header
            news_data = list(dfs.values.tolist())
            result = [dict(zip(header, d)) for d in news_data]
            return result
        elif isinstance(data[0], dict):  # [{},{}]
            return data

def write_file(filename, data, mo, max_num=0):
    '''
    功能：保存表格数据的主函数|过程：对数据进行处理成统一格式-》是否超过限制，需要分段-》保存文件
    :param filename: 文件名|str|
    :param data: 数据|list/dict|
    :param mo: 模式|str|w:覆盖保存 ；a:追加
    :param header:字段名|list|
    :param max_num:最大分段长度|int|
    :return:
    ps: 1.xls单个sheet限制：65,535条记录 2.xlsx单个sheet限制：1,048,576条记录 3.csv 只能存单个sheet，单个sheet存储无限制，但wps和office读取.csv最多只能显示1,048,576行
        因追加模式 a 分段不完善：对应格式限制数量以下的可以使用追加模式 a （不超过max_num）
        超过对应格式限制数量的只能使用覆盖模式w
    '''
    if filename.find('/') != -1:
        if not os.path.exists(filename[0:filename.rfind('/')]):
            os.makedirs(filename[0:filename.rfind('/')])
    if max_num == 0:
        hz = os.path.splitext(filename)[1]
        if hz == '.xls':
            max_num = 65535
        elif hz == '.xlsx':
            max_num = 1048576
        elif hz == '.csv':
            max_num = 99999999999999999999999
        else:
            print('该文件后缀不是表格文件后缀')
            exit()
    new_data = To_list_dict(data)
    header = new_data[0].keys()
    if len(new_data) < max_num:  # 如果数据长度小于最大长度，直接保存文件
        new_df = pd.DataFrame(new_data)
        CH(new_df, filename, header, mo)
    elif len(new_data) > max_num and mo != 'a':  # 如果数据长度大于最大长度，分段后保存文件(追加模式下不能分段)
        FD_data_list = FD_data(new_data, max_num)
        for fd_num in range(0, len(FD_data_list)):
            new_filename = filename[0:filename.rfind('.')] + '-' + str(fd_num + 1) + filename[filename.rfind(
                '.'):]  # xx.csv -> xx-1.csv
            new_df = pd.DataFrame(FD_data_list[fd_num])
            CH(new_df, new_filename, header, mo)
    else:
        print('{}|数据量超过{},不能使用a模式'.format(filename, max_num))

def Read_file(filename,encode='utf-8'):
    '''
    功能：读取表格（.xls/.xlsx/.csv）文件，返回list_dict格式
    :param filename: 文件路径名
    :return:
    '''
    hz = os.path.splitext(filename)[1]
    if hz == '.xls' or hz == '.xlsx':
        data = pd.read_excel(filename)
    elif hz == '.csv':
        data = pd.read_csv(filename,encoding=encode)
    else:
        data = None
        exit()
    headers = list(data.keys())
    rows = data.values.tolist()
    li = []
    for row in rows:
        li.append(dict(zip(headers, row)))
    return li

def Csv_split(filename, file_num, header=None):
    '''
    功能：csv大文件分割
    :param filename: 文件路径名|str
    :param file_num: 分割个数|int
    :param header: 字段名|list|个数一定要与分割文件的字段个数一致
    :return:
    '''
    # 根据是否有表头执行不同程序，默认是否表头的
    if header:
        # 获得每个文件需要有的行数
        chunksize = 1000000  # 先初始化的chunksize是100W
        data1 = pd.read_csv(open(filename), chunksize=chunksize, sep=',', encoding='utf-8')
        num = 0
        for chunk in data1:
            num += len(chunk)
        chunksize = round(num / file_num + 1)  # 根据分割大小计算分块读取的值
        # 需要存的file
        head, tail = os.path.splitext(filename)
        data2 = pd.read_csv(open(filename), chunksize=chunksize, sep=',', encoding='utf-8',names=header)  # 加入自定义header以新的分块大小重新读取csv
        i = 0  # 定文件名
        for chunk in data2:
            chunk.to_csv('{0}_{1}{2}'.format(head, i, tail), index=False)
            print('保存第{0}个数据'.format(i))
            i += 1
    else:
        # 获得每个文件需要有的行数
        chunksize = 1000000  # 先初始化的chunksize是100W
        data1 = pd.read_csv(open(filename), chunksize=chunksize, header=None, sep=',')
        num = 0
        for chunk in data1:
            num += len(chunk)
        chunksize = round(num / file_num + 1)

        # 需要存的file
        head, tail = os.path.splitext(filename)
        data2 = pd.read_csv(open(filename), chunksize=chunksize, header=0, sep=',')
        i = 0  # 定文件名
        for chunk in data2:
            chunk.to_csv('{0}_{1}{2}'.format(head, i, tail), index=False)
            print('保存第{0}个数据'.format(i))
            i += 1


if __name__ == '__main__':
    # 写入表格文件------------------------------
    # 测试数据生成
    di = {'name1': ['aaa', 'bbb'], 'age': ['18', '19']}
    li = [['name', 'age'], ['aaa', '16'], ['bbb', '16'], ['ccc', '16']]
    dic = [{'name1': 'aaa%d' % i} for i in range(0, 65545)]   
    # ----------
    for i in range(1, 3):
        write_file('xx/di.csv',di,'w')
        write_file('xx/di.xls', di, 'w')
        write_file('xx/di.xlsx', di, 'w')
        write_file('xx/li.csv', li, 'w')
        write_file('xx/li.xls', li, 'w')
        write_file('xx/li.xlsx', li, 'w')
        write_file('xx/dic.csv', dic, 'w')
        write_file('xx/dic.xls', dic, 'w')
        write_file('xx/dic.xlsx', dic, 'w')
    # 读取表格文件----------------------------
    result1 = Read_file('xx/li.xls')
    result2 = Read_file('xx/li.xlsx')
    result3 = Read_file('xx/li.csv')
    print(result1)
    print(result2)
    print(result3)
    # csv大文件分割---------------------------
    Csv_split('xx/dic.csv',3)            # 一个文件分成3份
