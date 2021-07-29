
def Num_dict(path,start_num,end_num):
    '''
    功能：生成纯数字字典，如：1-1000=》0001,0002......1000
    :param path: 生成文件路径
    :param start_num: 开始
    :param end_num: 结束
    :return:
    '''
    li=[]
    for i in range(start_num, end_num+1):
        wc = len(str(end_num)) - len(str(i))
        li.append('%s%s' % ('0' * wc, i))
    with open(path,'w') as f:
        for i in li:
            f.write(i+'\n')
    f.close()
