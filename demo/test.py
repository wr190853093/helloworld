#coding:utf-8

import xlrd

book = xlrd.open_workbook(u'./图书信息表.xls')
author_table = book.sheet_by_name(u'作者信息')

col = author_table.ncols

names = author_table.col_values(0)
for c in range(1,len(names)):
    data = {}
    # for i in range(0, col):
    data['name'] = author_table.col(0)[c].value
    data['sex'] = author_table.col(1)[c].value
    data['age'] = author_table.col(2)[c].value
    data['email'] = author_table.col(3)[c].value
    data['phone'] = author_table.col(4)[c].value

        # print author_table.row(c)[i].value,
        # data[author_table.row(0)[i]] = author_table.row(c)[i].value
    print data