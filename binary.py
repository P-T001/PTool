
def Payload_change1(payload):
    '''
    功能:"\xbb\xbb......"-》 "0xbb,0xbb......"
    :param payload: "\xbb\xbb......"|str 
    :return: "0xbb,0xbb......"|str
    '''
    s_li=payload.split("\\")
    new_li = []
    for x in s_li[1:]:
        new_li.append('0{}'.format(x.replace('"','').replace('\n','').replace(';','')))
    result = ','.join(new_li)
    return result + ','
    
    
def Payload_change2(payload_file):
    '''
    功能:msf生成的payload,每行都有双引号（"\xbb\xbb......"），结果输出成一行("0xbb,0xbb......")
    :param payload_file: Payload文件路径
    :return: 结果输出成一行("0xbb,0xbb......")
    '''
    payload=open(payload_file,'r')
    payload_result = ''.join(payload.readlines())
    s_li=payload_result.split("\\")
    new_li=[]
    for x in s_li[1:]:
        new_li.append('0{}'.format(x.replace('"','').replace('\n','').replace(';','')))
    result=','.join(new_li)
    return result+','
