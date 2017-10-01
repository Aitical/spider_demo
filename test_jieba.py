import jieba
import collections

f = open('songTotal.txt')
ff = open('停用词.txt')
lst = []
for i in ff:
    lst.append(i[:-1])
lst.append(' ')
lst.append('\n')
lst.append('作词')
lst.append('作曲')
lst.append('the')
dd = list(jieba.cut(f.read()))
res = collections.Counter(dd)
total = res.most_common(100)
for i,j in total:
    if(i in lst):
        pass
    else:
        print(i,j)

