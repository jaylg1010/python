#_author:"gang"
#date: 2017/12/7

l1=[1,2,3,4,5]
l2=[1,3,5]

l1set=set(l1)
l2set=set(l2)

print(l1set-l2set)
print(l2set-l1set)

if l2set-l1set:
    print(True)
else:
    print(False)