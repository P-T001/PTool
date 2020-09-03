# -- coding: utf-8 --
import os
import time
import gevent
import pymysql
import datetime
import threading
from bg_class import BG
from queue import Queue
from gevent import monkey

class mysql_demo(object):
    __v = None
    def __init__(self,user,password,db=None,host="localhost",port=3306,charset="utf8",maxconn=5):
        self.user,self.password,self.db,self.host,self.port,self.charset=user,password,db,host,port,charset
        self.maxconn=maxconn
        self.now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_path='./log.txt'
        self.debug=True
        self.pool=Queue(self.maxconn)
        for i in range(self.maxconn):
            try:
                conn=pymysql.connect(host=self.host, port=self.port, db=self.db, user=self.user, password=self.password, charset =self.charset)
                conn.autocommit(True)
                self.pool.put(conn)
            except Exception as e:
                raise IOError(e)

    # 基层类功能--------------------------
    # 功能：获取单个实例|PS：不能生成多个实例，如果重新调用，获取原本的那个实例
    @classmethod
    def get_instance(cls,*args,**kwargs):
        if cls.__v:
            return cls.__v
        else:
            cls.__v = mysql_demo(*args, **kwargs)
            return cls.__v

    # 功能：关闭mysql连接池
    def close_pool_conn(self):
        for i in range(self.maxconn):
            self.pool.get().close()


    # 功能：执行sql查询语句|用于select，需要回显的
    def Exec_Select(self,sql,operation=None):
        '''
        :param sql: sql语句| str
        :param operation:数据列表|list|tuple| 如果sql语句中有%s，必须使用该参数方法，列表的列表中每个元素替换该%s，进行批量插入
        :return:
        '''
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                response=cursor.execute(sql,operation) if operation else cursor.execute(sql)
            except Exception as e:
                cursor.close()
                self.pool.put(conn)
                self.Debug_log('Exec_Select|{}|{}|{}'.format(e.__traceback__.tb_frame.f_globals["__file__"],e.__traceback__.tb_lineno,e))
            else:
                data=cursor.fetchall()
                cursor.close()
                self.pool.put(conn)
                return response,data
        except Exception as e:
            self.Debug_log('Exec_Select|获取连接池异常|{}|{}|{}'.format(e.__traceback__.tb_frame.f_globals["__file__"],e.__traceback__.tb_lineno,e))

    # 功能：执行sql语句|用于delete、update、insert等，回回显操作
    def Exec_sql(self,sql,operation=None):
        '''
        :param sql: mysql语句|str
        :param operation: 批量插入数据列表|list/tuple |如果sql语句中有%s，必须使用该参数方法，列表的列表中每个元素替换该%s，进行批量插入
        例：insert into {表名}({字段名}) values(%s,%s)    operation=[['值1','值2'],['值1','值2']]   # 进行一行行批量插入
        :return:  执行sql语句，无法回内容
        '''
        try:
            conn = self.pool.get()
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                if operation and (isinstance(operation[0],list) or isinstance(operation[0],tuple)):
                    response=cursor.executemany(sql,operation) if operation else cursor.execute(sql)
                else:
                    response=cursor.execute(sql,operation) if operation else cursor.execute(sql)
            except (Exception,OSError,TypeError) as e:
                cursor.close()
                self.pool.put(conn)
                self.Debug_log('游标异常|{}|{}|{}'.format(e.__traceback__.tb_frame.f_globals["__file__"],e.__traceback__.tb_lineno,e))
            else:
                cursor.close()
                self.pool.put(conn)
                return response
        except Exception as e:
            self.Debug_log('获取连接池异常|{}|{}|{}'.format(e.__traceback__.tb_frame.f_globals["__file__"],e.__traceback__.tb_lineno,e))
    # end-----------------
    # 基础类功能
    # 功能：批量插入表数据|
    def Insert(self,table_name,columns,data):
        '''
        :param table_name: 表名|str
        :param columns: 字段名列表|list
        :param data: 插入的数据|list in list |[[1,2],[3，4]]
        :return:
        '''
        try:
            insert_sql=r"insert into {}({}) values({})".format(table_name,','.join(tuple(columns)),','.join(tuple(('%s,'*len(data[0])).split(',')[:-1])) )
            self.Exec_sql(insert_sql,data)
        except Exception as e:
            self.Debug_log('Insert|{}|{}|{}'.format(e.__traceback__.tb_frame.f_globals["__file__"],e.__traceback__.tb_lineno,e))

    # 功能：创建表|
    def Create_table(self,  table_name, columns,Type=None):
        '''
        :param table_name: 创建的表名|str
        :param columns: 创建表的字段名列表|list|
        :param Type: 创建表的字段名数据类型|list|默认longtext
        :return:  True |False
        '''
        try:
            C_tables = 'CREATE TABLE IF NOT EXISTS ' + table_name + '(id INT PRIMARY KEY AUTO_INCREMENT'
            if Type and len(columns) == len(Type) and isinstance(Type,list):
                for N in range(0, len(columns)):
                    C_tables = C_tables + "," + "%s %s" % (columns[N], Type[N])
            else:
                for N in range(0, len(columns)):
                    C_tables = C_tables + "," + "%s %s" % (columns[N], 'longtext')
            C_tables = C_tables + ")"
            self.Exec_sql(C_tables)
            self.Debug_log("创建表{}成功".format(table_name))
            return True
        except:
            self.Debug_log("创建表{}失败".format(table_name))
            return False

    def Import_all(self,contain_list=None,exclude_add_list=None):
        '''
        :param contain_list:导出表名|list
        :param exclude_add_list:排除的库名|list
        默认导出所有库的所有表，默认的库除外
        :return:
        '''
        exclude_list=['information_schema','mysql','performance_schema','sys'] # 排除数据库
        if exclude_add_list:
            exclude_list.extend(exclude_add_list)
        db_result=self.Exec_Select('show databases')                           # 查询所有数据库名
        for res in db_result[1]:
            db=list(res.values())[0]
            if db not in exclude_list:
                tb_result=self.Exec_Select('show tables from {};'.format(db))  # 查询库的所有表名
                for tbs in tb_result[1]:
                    tb=list(tbs.values())[0]
                    path = './outfile/{}'.format(db)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    if contain_list==None or (contain_list==True and tb in contain_list):
                        result=self.Exec_Select('select * from {}.{}'.format(db,tb))  # 查询表的内容
                        if result[0]>0:
                            filename=path+'/{}.csv'.format(tb)
                            bg=BG()
                            bg.To_data(filename,result[1],'w')
    # 日志类功能---------------------
    # 功能：操作日志|
    def Log(self, log_writer):
        '''
        :param log_writer: 保存日志内容
        :return:
        '''
        with open(self.log_path, 'a+') as f_log:
            f_log.write('{}|{}\n'.format(self.now_time, log_writer))
        f_log.close()

    # 功能：debug日志|
    def Debug_log(self, log_con):
        '''
        :param log_con: 日志内容
        :return:
        '''
        if self.debug:
            print(log_con)
        else:
            self.Log(log_con)

# 生成测试数据
def test_data(num):
    s=[]
    for i in range(num):
        s.append(('张小凡%d'%i,'%d'%i))
    return s

# 多线程工作队列
def DXC(num,def_target,def_args):
    job_list = []
    for i in range(num):
        t = threading.Thread(target=def_target, args=def_args)
        t.start()
        job_list.append(t)
    # 加入工作队列
    for j in job_list:
        j.join()

# 线程测试|按顺序插入
def DXC_test():
    start = time.time()
    tes = mysql_demo.get_instance('root', 'root', 'web_log')
    data = test_data(100000)
    DXC(10,tes.Insert,('test',['name','age'],data))
    # 关闭连接池
    tes.close_pool_conn()
    print("totol time:",time.time()-start)

# 协程测试|同步插入
def XC_test():
    monkey.patch_all()
    num=10
    start = time.time()
    tes = mysql_demo.get_instance('root', 'root', 'web_log')
    job_list = []
    data = test_data(100000)
    for i in range(num):
        job_list.append(gevent.spawn(tes.Insert,'test',['name','age'],data))
        #print(job_list)
    gevent.joinall(job_list)
    tes.close_pool_conn()
    print("totol time:", time.time() - start)

# 正常插入
def test():
    start = time.time()
    data= test_data(100)
    tes = mysql_demo.get_instance('root', 'root', 'web_log')
    for i in range(10):
        tes.Insert('test',['name','age'],data)
    tes.close_pool_conn()
    print("totol time:", time.time() - start)

if __name__ == '__main__':
    # DXC_test()  # 3.4秒
    # XC_test()   # 3.4秒
    # test()      # 5.7秒
    tes = mysql_demo.get_instance('root', 'root')
    # result=pz.Exec_Select('show databases')
    tes.Import_all()
    # print(result)
    tes.close_pool_conn()
