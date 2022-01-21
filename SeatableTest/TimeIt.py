def regex_time():
    a = 'aHG,,/.,K汉   字HJGH,.,^&^ \n*&，。，_汉字二__   J'
    reg1=r'\W+|_+'
    reg2=r'[\W_]+'
    reg3=r'[\W_0-9a-z]+'
    reg4=r'\w+|_+|[0-9]+|[a-z]+'
    return re.sub(reg2, '', a)

if __name__ == '__main__':
    import timeit,re

    t= timeit.Timer('regex_time()','from __main__ import regex_time')
    print(t.timeit(10000))