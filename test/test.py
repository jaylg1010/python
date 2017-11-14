#_author:"gang"
#date: 2017/7/27


#简单的装饰函数
# import time
# import random
#
# #装饰器
# def timmer(func):
#     def wrapper():
#         start_time = time.time()
#         func()
#         end_time = time.time()
#         print('run time is %s' % (end_time - start_time))
#     return wrapper
#
# #被装饰函数
# def index():
#
#     time.sleep(random.randrange(1,5))

#     print('wlcome to index page')
#
# index = timmer(index)
# index()


#带装饰语法的装饰器
# import time
# import random
# def timmer(func):
#     def wapper():
#         start_time = time.time()
#         func()
#         end_time = time.time()
#         print('run time is %s'%(end_time - start_time))
#     return wapper
#
# def auth(fun):
#     def inner():
#         while True:
#             name = input('name :')
#             password = input('password: ')
#             if name == 'lugang' and password == '123':
#                 fun()
#             else:
#                 continue
#     return inner
# @auth
# @timmer   # index = timmer(index)
# def index():
#     time.sleep(random.randrange(1,5))
#     print('welcom to index page')
#
# index()



#带参数的装饰器
# import time
# import random
#
# def timmer(func):
#     def wapper(*args,**kwargs):
#         start_time = time.time()
#         func(*args,**kwargs)
#         end_time = time.time()
#         print('run time is %s'%(end_time - start_time))
#     return wapper
#
# @timmer
# def index(*args,**kwargs):
#     time.sleep(random.randrange(1,10))
#     print('welcome from index',args,kwargs)
#
# index((1234),**{'g':2,'k':3})


#有返回值的
# import time
# import random
#
# def timmer(func):
#     def wapper(*args,**kwargs):
#         start_time = time.time()
#         ret = func(*args,**kwargs)
#         end_time = time.time()
#         print('run time is %s'%(end_time - start_time))
#         retrun ret
#     return wapper
#
# @timmer
# def index(*args,**kwargs):
#     time.sleep(random.randrange(1,10))
#     print('welcome from index',args,kwargs)
#     return args,kwarfs
#
# index((1234),**{'g':2,'k':3})


#最基本的装饰器


# def wapper(func):
#     def inner(*args,**kwargs):
#         '''执行函数之前功能'''
#         ret = func(*args,**kwargs)
#         '''执行函数之后功能'''
#         return ret
#     return inner
# @wapper   #fun = wapper(fun)
# def fun(*args,**kwargs):
#     ret = print('from fun')
#     return ret
# fun()





# def wrapper1(func):
#     def inner():
#         print('wrapper1 ,before func')
#         func()
#         print('wrapper1 ,after func')
#     return inner
#
# def wrapper2(func):
#     def ww():
#         print('wrapper2 ,before func')
#         func()
#         print('wrapper2 ,after func')
#     return ww
#
# @wrapper2
# @wrapper1
# def f():
#     print('in f')
#
# f()
