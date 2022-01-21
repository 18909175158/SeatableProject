#if False:
#	print(1)
#import re
#str1 = '\\n:\hes_9。，？！0+jd+7里￥领『￠【】』域…;……；（——《》）我们18hsjbsjja=hd'
#str2 = '你就（_（->（_（…,…**/_~）））HDG）鸡肉'
#for i in ' ,./;\'\\[]<>?:\"|{}!@#$%^&*()-=_+，。《》、？；’：”！￥……\n\t\r':
#	str2 = repr(str1).replace(i,'')
#print(str2)

#regex1=re.sub('\W+','',str2)
#regex2 = re.sub('_','',re.sub('\W+','',str2))
#mo=regex1.findall(str1)
#for u in mo:
#print(regex1)
#for u in regex2:
#	print(u)
#print(regex2.lower())
#print(type(regex2))
#print(len(regex2))

#str3 = 'abcdef'
#regex3 = re.compile('\w{2}')
#mo = regex3.findall(str3)
#print(mo)
import re
r=re.compile('[0-9a-zA-Z]+')
#s='\\n:\hes_9。，？！0+jd+7里￥领『￠【】』域…;……；（——《》）我们18hsjbsjja=hd你就（_（->（_（…,…**/_~）））HDG）鸡肉'
s='tsjdh-yeg12e_hdj_4587'

a=r.findall(s)
print(a)