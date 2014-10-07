#! /usr/bin/python
# -*- coding:utf-8 -*-

def test(fin):
	b = fin.readline()
	print(b)



fin = open ('1.c', 'r')
a = fin.readline()
print (a)
test(fin)
c =fin.readline()
print(c)

fin.close()
