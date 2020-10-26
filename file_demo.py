import os
import re
import shutil
import chardet

def File_sample(path):
    '''
    功能：清楚了解路径中的目录、文件名、文件名（无后缀）、文件名后缀的取法
    :param path:文件路径
    :return:
    '''
    dir=os.path.dirname(path)  # 目录名
    filename=os.path.basename(path) # 文件名
    file=os.path.splitext(filename)[0] # 文件名，无后缀
    hz=os.path.splitext(filename)[1] # 后缀
    # 如果path路径不存在，但dir,filename,file,hz还是会根据path取出来
    print('路径：{} | 目录：{} | 文件名：{} | 文件名（无后缀）：{} | 文件名后缀：{}'.format(path,dir,filename,file,hz))
    # 如果dir不存在，则root，dirs,files为均为空，输出不显示
    for root,dirs,files in os.walk(dir):
        print(root,dirs,files)


def File_list(path, Pc_hz_list=None,Only_hz_list=None, Pc_path_list=None):
    '''
    功能：列出路径下的所有文件路径，可根据条件筛选（不包括文件夹）
    :param path: 路径|str|相对路径/绝对路径
    :param Pc_hz_list: 排除的后缀列表|list|['.csv']
    :param Only_hz_list: 需要的后缀列表|list|['.csv']
    :param Pc_path_list: 排除的文件夹列表|list|['name']  如需排除单个绝对路径文件夹，可以在返回的列表中排除
    :return: 路径列表|list|路径取决于path是相对路径/绝对路径
    '''

    def File(path, lists, f_Pc_list):
        dirs = os.listdir(path)
        if len(dirs) > 0:
            for dir in dirs:
                dir_path = '{}/{}'.format(path, dir) if path[-1] != "/" else '{}{}'.format(path, dir)
                if os.path.isdir(dir_path):
                    if f_Pc_list is None:
                        f_Pc_list = []
                    if dir not in f_Pc_list:
                        File(dir_path, lists, f_Pc_list)
                else:
                    lists.append(dir_path)
            return lists

    new_file_li = []
    files = File(path, [], Pc_path_list)
    if files:
        if Pc_hz_list is None:
            Pc_hz_list = []
        if Only_hz_list is None:
            Only_hz_list=[]
        for file in files:
            if os.path.splitext(file)[1] not in Pc_hz_list:
                if Only_hz_list:
                    if os.path.splitext(file)[1]  in Only_hz_list:
                        new_file_li.append(file)
                else:
                    new_file_li.append(file)
    return new_file_li


def Dir_list(path,Pc_list=None):
    '''
    功能：列出路径下的所有文件夹（不包括文件）
    :param path: 路径|str|相对路径/绝对路径
    :param Pc_list: 排除的文件夹列表|list|['name']  如需排除单个绝对路径文件夹，可以在返回的列表中排除
    :return: 路径列表|list|路径取决于path是相对路径/绝对路径
    '''
    def Dir(path,lists,d_Pc_list):
        dirs = os.listdir(path)
        if len(dirs) > 0:
            for dir in dirs:
                dir_path='{}/{}'.format(path,dir) if path[-1] != "/" else '{}{}'.format(path,dir)
                if os.path.isdir(dir_path):
                    if d_Pc_list is None:
                        d_Pc_list=[]
                    if dir not in d_Pc_list:
                        lists.append(dir_path)
                        Dir(dir_path, lists, d_Pc_list)

            return lists
    dir_list=Dir(path, [], Pc_list)
    return dir_list if dir_list else []


def Del_file_null(path):
    '''
    功能：移除路径下的所有空目录
    :param path: 路径
    :return: None
    '''
    files=os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if not os.listdir(file_path):  # 判断该目录不为空
            os.rmdir(file_path)


def Del_files(path,dir_status=None):
    '''
    功能:移除路径下的所有文件（文件和文件夹），删除的路径可以包含path
    :param path: 路径
    :param dir_status: path路径是否删除|bool|True：删除，False：不删除，默认False
    :return:None
    '''
    del_list=os.listdir(path)
    for f in del_list:
        file_path=os.path.join(path,f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    if dir_status:
        os.rmdir(path)
        
def Copys(path,out):
    '''
    功能：复制path路径下的所有文件（文件和文件夹）到out路径（该路径可以不存在）下
    :param path: 源路径|str
    :param out: 目标路径|str
    :return: None
    '''
    for files in os.listdir(path):
        name = os.path.join(path, files)
        back_name = os.path.join(out, files)
        if os.path.isfile(name):
            shutil.copy(name, back_name)
        else:
            if not os.path.isdir(back_name):
                os.makedirs(back_name)
            Copy(name, back_name)
            
def File_code(filename):
    '''
    功能：读取文件编码
    :param filename: 文件路径|str
    :return: 编码和数据|
    '''
    with open(filename,'rb') as f:
        data=f.read()
        en=chardet.detect(data).get("encoding")
        f.close()
        return en,data
            

def File_auto_rename(file_path):
    '''
    功能：判断是否存在同名文件，如果已存在返回重命名文件名添加”(0), (1), (2)….“之类的编号
    :param file_path:文件路径|str
    :return:重新命名的文件路径|str
    '''
    directory, file_name = os.path.split(file_path)
    while os.path.isfile(file_path):
        pattern = '(\d+)\)\.'
        if re.search(pattern, file_name) is None:
            file_name = file_name.replace('.', '(0).')
        else:
            current_number = int(re.findall(pattern, file_name)[-1])
            new_number = current_number + 1
            file_name = file_name.replace(f'({current_number}).', f'({new_number}).')
        file_path = os.path.join(directory + os.sep + file_name)
    return file_path

       
def File_to_code(src,dst,code):
    '''
    功能：单文件转换文件编码
    :param src: 源文件路径|str|如：./xxx1.txt
    :param dst: 转换后文件路径|str|如：./xxx2.txt
    :param code:转换编码|str|如：utf-8
    :return:
    '''
    en,data=File_code(src)
    if not os.path.isdir(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))
    if en!=code:
        with codecs.open(src,'r',en) as f1r:
            try:
                with codecs.open(dst, 'w', code) as f2w:
                    f2w.write(f1r.read())
            except Exception as E:
                print('{}|{}'.format(src,E))

def File_to_codes(src,dst,code):
    '''
    功能：批量转换文件编码
    :param src: 源目录路径|str|如：./src/
    :param dst: 转换后存放目录路径/str|如：./dst/
    :param code: 转换编码|str|如：utf-8
    :return: 
    '''
    filenames=File_list(src)
    if not os.path.isdir(dst):
        os.makedirs(dst)
    for file in filenames:
        File_to_code(file,'{}/{}'.format(dst,file.replace(src,'')),code)





def Test_time(target,log_file, arg=(), **m):
    '''
    功能：测试函数的运行时间
    :param target: 目标函数|变量|
    :param log_file: 日志文件路径|str|
    :param arg: 目标函数的参数|tuple
    :param m: 目标函数的参数|可不输入
    :return: 
    '''
    St = int(time.time())
    s = time.localtime(St)
    st = time.strftime("%Y-%m-%d %H:%M:%S", s)
    print("开始时间：%s "%st)
    target(*arg, **m)
    Et = int(time.time())
    e = time.localtime(Et)
    et = time.strftime("%Y-%m-%d %H:%M:%S", e)
    print("结束时间：%s "%et)
    print("用时：%d秒" % (Et-St))
    log_=open(log_file,"a")
    log_.write("开始时间：%s | 结束时间：%s | 用时：%d秒"%(st,et,(Et-St)))
    log_.close()
