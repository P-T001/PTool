import os
import shutil



def List_file(path,Hz_list=None,Pc_list=None):
    '''
    功能：列出路径下的所有文件（不包括文件夹）
    :param path: 路径|str|相对路径/绝对路径
    :param Hz_list: 排除的后缀列表|list|['.csv']
    :param Pc_list: 排除的文件夹列表|list|['name']  如需排除单个绝对路径文件夹，可以在返回的列表中排除
    :return: 路径列表|list|路径取决于path是相对路径/绝对路径
    '''
    def File(path, lists, f_Pc_list):
        dirs = os.listdir(path)
        if len(dirs) > 0:
            for dir in dirs:
                dir_path='{}/{}'.format(path,dir) if path[-1] != "/" else '{}{}'.format(path,dir)
                if os.path.isdir(dir_path):
                    if f_Pc_list is None:
                        f_Pc_list=[]
                    if dir not in f_Pc_list:
                        File(dir_path, lists, f_Pc_list)
                else:
                    lists.append(dir_path)
            return lists
    new_file_li = []
    files = File(path, [], Pc_list)
    if files:
        if Hz_list is None:
            Hz_list = []
        for file in files:
            if os.path.splitext(file)[1] not in Hz_list:
                new_file_li.append(file)
    return new_file_li


def List_dir(path,Pc_list=None):
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


def Del_file(path,dir_status=None):
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
        
def Copy(path,out):
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
