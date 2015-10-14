# coding=utf-8
import traceback
import sys
tmp = {'a': 'aaa', 'b': 'bbb'}
try:
	print tmp['c']
except Exception, e:
	print  traceback.print_exc()
print 'hello'
