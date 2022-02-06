# # # # # # # # print('f' in 'ifd')
# # # # # # # print('      ,./;\'\\[]<>?:\"|{}!@#$%^&*()-=_+，。《》、？；’：”！￥……')
# # # # # # a = '  ,./《，。、&'
# # # # # # for i in a:
# # # # # #     if i in '  ,./《，。、&':
# # # # # #         a=a.replace(i,'')
# # # # # # print(a)
# # # # # l=[1,2]
# # # # # l[0]=3
# # # # # l[1]=4
# # # # # print(l)
# # # # to_be_cut_str='jfldsa,.'
# # # # for symbol in to_be_cut_str:
# # # #     if symbol in ' ,./;\'\\[]<>?:\"|{}!@#$%^&*()-=_+，。《》、？；’：”！￥……':
# # # #         to_be_cut_str = to_be_cut_str.lower().replace(symbol, '')
# # # # print(to_be_cut_str)
# # # def f(a):
# # #     return a-1
# # #
# # # b = 3
# # #
# # # print(f(b))
# # a=1
# # b=2
# # def f(c,d):
# #     c+=5
# #     d+=5
# # f(a,b)
# # print(a,b)
# # print('\r' in 'fdaf')
# # l=[]
# # l.append(1)
# # print(l)
# # print('fsdaf'+','+'rwqr'+',')
# # print(*['dasd','dad','iuiu'])
# # import datetime
# # print(datetime.strptime)
# # import datetime
# # # print(datetime.datetime.now())
# # a=datetime.datetime.strptime('2022-02-02','%Y-%m-%d')
# # b=datetime.datetime.strptime('2021-05-02','%Y-%m-%d')
# # print(a-b)
# # print(type(a-b))
# # print(datetime.datetime.strftime(a-b))
# # def a():
# #     return 1,2
# # b,c=a()
# # d=a()
# # print(b)
# # print(c)
# # # print(d)
# # # print(type(d))
# # # print(type(d) is tuple)
# # l=[]
# # l.extend([1,2])
# # print(l)
# # l=['2020-01-01','2011-10-12','2011-10-02','2011-08-30','2010-12-30']
# # l.sort()
# # print(l)
# # import re
# # s= 'hj_汉字二_s19_hj1_+,.,hj汉字k18.,.'
# # m = re.sub(r'[\W_0-9a-z]+', '', s)
# # print(m)
# # print(6*2/3)
# # if True:
# #     a=1
# # else:
# #     a=2
# # a = 'aHG,,/.,K汉   字HJGH,.,^&^ \n*&，。，_汉字二__   J'
# # # print(a)
# # # print(re.sub(r'[\W_]+','',a))
# # r= re.compile(r'\bv\d+\.\d+\b|\b\d+.\d+\b|[0-9a-z]+')
# # b=r.findall(a.lower())
# # print(b)
# # a=[10,9,8,7,6,5,4,3,2,1]
# # b = [29,28,27,26]
# # for nb in b:
# #     for n in a:
# #         if n>2:
# #             if n>5:
# #                 if n==9:
# #                     print(n + nb)
# #                 break
# # s= 'hh'
# # s+='gg'+'/'
# # s+='uu'+'/'
# # print(s)
# # import pprint
# # a=[{"name":"自5000T南","color":"#FFFCB5","textColor":"#202428","id":"910507"},{"name":"自5000T北","color":"#FFEAB6","textColor":"#202428","id":"427548","borderColor":"#ECD084"},{"name":"自3500T南","color":"#FFD4FF","textColor":"#202428","id":"703449","borderColor":"#E6B6E6"},{"name":"自3500T中","color":"#FFDDE5","textColor":"#202428","borderColor":"#EDC4C1","id":"837801"},{"name":"自2500T","color":"#89D2EA","textColor":"#FFFFFF","borderColor":"#7BC0D6","id":"672193"},{"name":"IOB","color":"#9F8CF1","textColor":"#FFFFFF","borderColor":"#8F75E2","id":"605609"},{"name":"自5000T南辊底炉","color":"#EAA775","textColor":"#FFFFFF","borderColor":"#D59361","id":"629154"},{"name":"自5000T北辊底炉","color":"#C2C2C2","textColor":"#FFFFFF","borderColor":"#ADADAD","id":"351108"}]
# # pprint.pprint(a)
# # def a():
# #     print(1)
# #
# # a()
# # from difflib import SequenceMatcher
# # a = '离合器齿圈'
# # b = '离合器齿盘'
# # str1 = '上顶料流量阀'
# # str2 = '上顶料流量电磁阀'
# # print(SequenceMatcher(None,a,b).ratio())
# # print(SequenceMatcher(None,str1,str2).quick_ratio())
# # print(type(SequenceMatcher(None,a,b)))
# # if not [None]:
# #     print(1)
# # u = 'https://cloud.seatable.cn/workspace/189828/asset/2c3fa054-d74e-48ab-87d1-0d7b42a4f18c/images/2022-01/575a7079f3d3a357988906a7011fed8e.jpeg'
# # l = u.split('/')
# # print(l)
# # import os
# # # r = r'C:\compress_img\'
# # path = r'c:\noway'
# # # if not os.path.exists(path):
# # #     os.makedirs(path)
# # print(path +'\\'+ 'a\\bbb')
# # from PIL import Image
# # import os
# # p = r'C:\compress_img\uncompress\09565694hh49sa9w9pzs7t.jpg'
# # s = os.path.getsize(p)/1024
# # print(s)
# # print((1/s)**0.5/0.000515)
# # # print(type(s))
# # si = Image.open(p)
# # si.save(r'C:\compress_img\compressed\09565694hh49sa9w9pzs7t.jpg',quality = 60)
# #
# # sd = os.path.getsize(r'C:\compress_img\compressed\09565694hh49sa9w9pzs7t.jpg')/1024
# # print(sd)
# # y = 4000
# # x = (1/y)**0.67/0.00016
# # print(x)
# # y=2000
# # x = (1/y)**0.67/0.00016
# # print(x)
# # y=1000
# # x = (1/y)**0.67/0.00016
# # print(x)
# # def a(y,n,m):
# #     x1 = (1/y)**n/m
# #     x2 = (1/(y*2))**n/m
# #     x3 = (1 / (y * 3)) ** n / m
# #     x4 = (1 / (y * 4)) ** n / m
# #     x5 = (1 / (y * 5)) ** n / m
# #     print(x1,x2,x3,x4,x5,sep = '\n')
# #
# # n = 0.69
# # m=0.000106
# # a(1000,n,m)
# # import os
# # os.remove((r'C:\code\1.txt',r'C:\code\2.txt'))
#
# # a =1
# # def r(x):
# #     for i in range(3):
# #         x +=2
# #         print(x)
# # r(a)
# # a+=1
# # a+=1
# # # print(a)
# # # print([d for d in range(3)])
# # l =[1]
# # a = l.append(2)
# # print(a)
# # print(l)
# # import os
# # print(os.name)
# # print(os.getcwd())
# # print(os.listdir('.'))
# # l1 = [1]
# # l2=[2]
# # l=l1+l2
# # print(l)
# # print('12345'[:3])
# # print(type('12345'[:3]))
# # print(len(None))
# # print(None == False)
#
# # if not None:
# #     print(1)
#
# # l = [1,2]
# # l.remove(1)
# # print(l)
# # print(False and False)
# # a=None
# # b=None
# # if a==None and b==None:
# #     print(1)
# # # c= a and b
# # # print(c)
# #  \
# #                 or \
# #                 (single_dict['普通配件型号']==None and single_dict['重要、核心配件型号']==None)
# # l = [1,2,3,4,10,15,1,2,4]
# # for i in l[::-1]:
# #     if i <5:
# #         l.remove(i)
# # print(l)
# # None.strip()
# # if None:
# #     print(1)
# # elif None:
# #     print(2)
# # elif '2':
# #     print(3)
# # else:
# #     print(4)
# import re
# from difflib import SequenceMatcher
# from datetime import datetime
# from seatable_api import Account
#
# # 获取账户授权。
# email = '18909175158@163.com'
# password = 'sincere1027'
# server_url = 'https://cloud.seatable.cn/'
# account = Account(email, password, server_url)
# account.auth()
#
# '''
# 获取所有待处理数据
# '''
# # 获取两张表的base。
# model_base = account.get_base(189828, '配件管理总表')
# record_base = account.get_base(189828, '维修记录表')
#
# # 核心、重要配件 中需要获取的列的key。
# needful_common_model_keys = '_id,配件型号,配件名称,所属工段,所属设备,最近安装、维修日期,前10次故障日期'
# needful_special_model_keys = '_id,配件型号,所属工段,所属设备,最近安装、维修日期,前10次故障日期'
# # 获取 普通 和 重要配件 中所有行的上述列。
# existing_common_model_list = model_base.query('select ' + needful_common_model_keys + ' from 普通配件')
# existing_special_model_list = model_base.query('select ' + needful_special_model_keys + ' from 重要、核心配件')
# # 维修记录 中需要获取的列的key。
# needful_record_keys = '_id,所属工段,所属设备,普通配件型号,普通配件名称,重要、核心配件型号,故障日期,_ctime,是否已整理'
# # 获取 维修记录 和 图片版 中所有行的上述列。
# record_list = record_base.query('select ' + needful_record_keys + ' from 维修记录')
# pic_record_list = record_base.query('select ' + needful_record_keys + ' from 维修记录（图片版）')
# print(pic_record_list)
# import re
# model1 = 'fdsa——43ff545——21'
# en_regex = re.compile(r'\bv\d+\.\d+\b|\b\d+.\d+\b|[0-9a-z]+')
# model1_piece_list = en_regex.findall(model1.lower())
# print(model1_piece_list)
# from WeChatPYAPI import WeChatPYApi
# w = WeChatPYApi()
# num = w.start_wx()
# print(num)
# # print(msg)
# s='xcx.zhichiweiye.com,xcx.zhichiweiye.cn,jisuapp.zhichiweiye.com,jisuapp.zhichiweiye.cn,xcx.yingyonghao8.com'
# l=s.split(',')
# # print(l)
# l1=['tcp://'+i+';\n' for i in l]
# # print(l1)
# s1=''
# for i1 in l1:
#     s1+=i1
# print(s1)
# a='备料,自动线,锻压机,热处理,模锻,轻跨,精锻'
# al=a.split(',')
# # print(al)
# bl=['配件','维修详情','维修详情（图片）']
# for ai in al:
#     for bi in bl:
#         print(ai+bi)
welcome_str = '欢迎进入维修数据管理系统！\
\n点击下方链接进入功能页面，\
\n回复”1“或者”帮助“获取更多帮助，\
\n回复”2“或者”地址“重新获取功能页链接。'
print(welcome_str)