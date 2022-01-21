import Levenshtein
str1 = '上顶料流量阀'
str2 = '上顶料流量电磁阀'
sim = Levenshtein.distance(str1, str2)
print('Levenshtein similarity: ', sim)

# 4.计算莱文斯坦比
sim = Levenshtein.ratio(str1, str2)
print('Levenshtein.ratio similarity: ', sim)