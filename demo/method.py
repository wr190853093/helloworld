#coding:utf-8
from models import *

import csv
import json
# json.loads()   # json字符串  to 字典
# json.dumps()   # 字典to json字符串
def get_total(month):
    data = {
        "business_autoFans_J": [{"2016_08": 14}, {"2016_09": 15}, {"2016_10": 9}],
        "autoAX": [{"2016_08": 7}, {"2016_09": 32}, {"2016_10": 0}],
        "autoAX_admin": [{"2016_08": 5}, {"2016_09": 13}, {"2016_10": 2}],
    }
    total = 0
    for v in data.values():
        for d in v:
            if d.has_key(month):
                total += d.get(month, 0)

    return total

def get_login_stat(username,pwd):
    flag = False
    try:
        # filename = r'./data.csv'
        # with open(filename) as f:
        #     reader = csv.reader(f)
        #     row = list(reader)
        #     for d in row:
        #
        #         if d[0] == username and d[1] == pwd:
        #             flag = True
        author = User.objects.filter(username=username, pwd=pwd)
        print username,pwd
        print author
        if len(author):
            flag =True
    except Exception as e:
        print e.message

    return flag

if __name__ == '__main__':
    print  get_login_stat('zhangsan','12345')
    data = {
        "business_autoFans_J": [{"2016_08": 14}, {"2016_09": 15}, {"2016_10": 9}],
        "autoAX": [{"2016_08": 7}, {"2016_09": 32}, {"2016_10": 0}],
        "autoAX_admin": [{"2016_08": 5}, {"2016_09": 13}, {"2016_10": 2}],
    }
    data1 = json.dumps(data)
    print data1
    print type(data1)