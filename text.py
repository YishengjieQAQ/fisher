dict = {}

list= []

tuple = ()

zero = 0

none = None

list1 = [dict, list, tuple, zero, none]
[print('存在')if single else print('空', end='') for single in list1]