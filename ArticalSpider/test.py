# -*- coding: utf-8 -*-

a = b'asdasd'
print(type(a))
print(isinstance(a, str))
print(isinstance(a, bytes))
b = a.decode('utf-8')
print(type(b))