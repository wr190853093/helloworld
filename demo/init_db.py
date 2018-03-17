#coding:utf-8
import os,django
import xlrd
from xlrd import xldate_as_datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helloworld.settings")
django.setup()

from demo.models import *

book = xlrd.open_workbook(u'./图书信息表.xls')
# 插入作者表
author_table = book.sheet_by_name(u'作者信息')
names = author_table.col_values(0)
col = author_table.ncols

for c in range(1,len(names)):
    Author(name=names[c]).save()

#插入作者信息表
for c in range(1,len(names)):
    name = author_table.col(0)[c].value
    author = Author.objects.get(name=name)
    sex = 1
    if author_table.col(1)[c].value== u'男':
        sex = 0
    phone = str.split(str(author_table.col(4)[c].value),'.')[0]
    AuthorDetails.objects.get_or_create(
        age= author_table.col(2)[c].value,
        sex=sex,
        email=author_table.col(3)[c].value,
        phone=phone,
        author=author
    )

# 插入出版社表
publisher_table = book.sheet_by_name(u'出版社信息')
for c in range(1,publisher_table.nrows):
    name = publisher_table.col(0)[c].value
    address = publisher_table.col(1)[c].value
    city = publisher_table.col(2)[c].value
    website = publisher_table.col(3)[c].value

    Publisher.objects.get_or_create(
        name= name,
        address= address,
        city= city,
        website= website
    )

# 插入图书信息表
book_table = book.sheet_by_name(u'图书信息')
for c in range(1,book_table.nrows):
    title = book_table.col(0)[c].value
    publisher = book_table.col(2)[c].value
    try:
        publisher_name = Publisher.objects.get(name=publisher)
    except Exception as e:
        print e.message
        print '未找到出版社为%s的数据' % publisher_name
    else:
        publication_data = xldate_as_datetime(book_table.col(3)[c].value,0)
        price = book_table.col(4)[c].value

        Book.objects.get_or_create(
            title=title,
            publisher= publisher_name,
            publication_data = publication_data,
            price = price
        )# get_or_create方法返回一个列表，第一个值是对象，第二个是个布尔值

        book_name = Book.objects.get(title=title)
        authors = str(book_table.col(1)[c].value)
        authors = str.split(authors,',')

        for i in authors:
            try:
                author = Author.objects.get(name=i)
                book_name.author.add(author)
                # author = Author.objects.filter(name=i)[]
                # book_name.author = author #会更新，不新增，只能创建一个关系
                # book_name.save()
            except Exception as e:
                print e.message
                print '未找到作者姓名为%s的数据' % i
