from seatable_api import Base, context
import pprint

server_url = context.server_url or 'https://cloud.seatable.cn'
api_token = context.api_token or '6ae59ed31314c62891fd69fc9426f813b6d690cf'

base = Base(api_token, server_url)
base.auth()

appd=[]
dict={}
ba=base.list_rows('入口地址')
# pprint.pprint(ba)
for d in ba:
    dict[d['名称']] = d['链接']
pprint.pprint(dict)

# pprint.pprint(a)
# a='备料,自动线,锻压机,热处理,模锻,轻跨,精锻'
# al=a.split(',')
# # print(al)
# bl=['普通配件','重要配件','维修详情','维修详情（图片）']
# for ai in al:
#     for bi in bl:
#         appd.append({'名称':ai+bi})
# base.batch_append_rows('视图',appd)
# pprint.pprint(appd)
# c='_id,_ctime,普通配件型号,故障日期,是否已整理'
# d= base.query('select * from 维修记录')
# pprint.pprint(d)
# a=base.query('select * from 维修记录')
# print(a)
# print(a[0].keys())
# print(a[0]['_ctime'][:10])

# b=''
# for k in list(a[0].keys()):
#     b+=k+','
# print(b)

# pprint.pprint(base.list_rows('维修记录(图片版)'))
# pprint.pprint(base.get_metadata())

# import re
# from difflib import SequenceMatcher
# from datetime import datetime
# from seatable_api import Account

# 获取账户授权。
# email = '18909175158@163.com'
# password = 'sincere1027'
# server_url = 'https://cloud.seatable.cn/'
# account = Account(email, password, server_url)
# account.auth()

# 获取两张表的base。
# model_base = account.get_base(189828, '配件管理总表')
# record_base = account.get_base(189828, '维修记录表')
# print(record_base)
# key_list = []
# col_list = base.list_columns('维修记录(图片版)')
# for col in col_list:
#     if col['type'] == 'image':
#         key_list.append(col['name'])
# print(key_list)
# print(base.list_rows('维修记录')[2]['故障名'])
# print(type(base.list_rows('锻造车间')))
# a = base.list_rows('锻造车间')
# print(a[-3]['前5次故障日期'])
# print(type(a[-3]['前5次故障日期']))
# pprint.pprint(a)
# b= base.list_rows('后台数据')
# pprint.pprint(b)
# print(row['型号'])
# base.delete_row('锻造车间', 'Yso05vy9QW2bIbZARhI8Og')
#
# from seatable_api import Account
#
# email = '18909175158@163.com'
# password = 'sincere1027'
# server_url = 'https://cloud.seatable.cn/'
# account = Account(email, password, server_url)
# account.auth()
#
# a=account.list_workspaces()
# pprint.pprint(a)
