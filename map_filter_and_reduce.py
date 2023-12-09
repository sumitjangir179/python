from functools import reduce

arr = [1,2,3,4,5,6]

def Square(x):
    return x * x

def Func(x):
    return x >= 3

def Sum(a,b):
    return a + b


map_func = list(map(Square,arr))
print(map_func)

filter_func = list(filter(Func,arr))
print(filter_func)

reduce_func = reduce(Sum,arr,0)
print(reduce_func)
