# coding=utf-8
class Test(object):
	def __init__(self):
		print 'init'

	def printa(self):
		try:
			aa = 'hello'
			self.bbb = aa
		except Exception, e:
			pass
		else:
			print self.a
		finally:
			pass

test = Test()
test.printa()
