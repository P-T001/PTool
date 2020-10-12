# -*- coding: UTF-8 -*-
# 列出路径下的文件
import os


def List_file(path, Pc_hz_list=None,Only_hz_list=None, Pc_path_list=None):
    '''
    功能：列出路径下的所有文件（不包括文件夹）
    :param path: 路径|str|相对路径/绝对路径
    :param Pc_hz_list: 排除的后缀列表|list|['.csv']
    :param Only_hz_list: 需要的后缀列表|list|['.csv']
    :param Pc_path_list: 排除的文件夹列表|list|['name']  如需排除单个绝对路径文件夹，可以在返回的列表中排除
    :return: 路径列表|list|路径取决于path是相对路径/绝对路径
    可以通过from file_demo import List_file  # 进行更新该函数
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


def tar_x(path, outfile):
    '''
    功能：tar批量解压，只接受path的2层的文件，不然可能会出现文件夹名定位错的情况
    :param path: 批量解压的路径|str|
    :param outfile: 批量解压的输出路径|str
    :return:输出哪些文件解压成功
    '''
    HZ = ['.gz']  # txt 解压的后缀文件
    PC = []  # 排除的需要解压的文件夹
    gzs = List_file(path, Only_hz_list=HZ, Pc_path_list=PC)
    with open('log.txt', 'a+', encoding='utf-8') as log:
        for gz in gzs:
            dir = gz.replace(path, '')[0:gz.replace(path, '').rfind('/')]
            if dir != '/' or dir != '':
                gz_x_path = '{}/{}'.format(outfile, dir)
            else:
                gz_x_path = outfile
            if not os.path.exists(gz_x_path):
                os.system('mkdir -p %s' % gz_x_path)
            os.system('tar xzfv %s -C %s' % (gz, gz_x_path))
            log.write('%s 成功解压\n' % gz)
    log.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str, help='需要批量解压文件夹路径')
    parser.add_argument('-o', '--outfile', type=str, help='输出路径路径')
    args = parser.parse_args()
    tar_x(args.path, args.outfile)


