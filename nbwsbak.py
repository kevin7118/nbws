# coding=utf-8
import urllib
import urllib2
import cookielib
from pyquery import PyQuery as pq


class Nbws(object):
	host = 'http://publish.nbws.gov.cn'
	index_url = 'http://publish.nbws.gov.cn/Index.shtml'
	login_url = 'http://publish.nbws.gov.cn/LoginFrame.shtml'
	validate_url = 'http://publish.nbws.gov.cn/ValidateCode.shtml'
	headers = {
		'Host': 'publish.nbws.gov.cn',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
	}

	def __init__(self):
		cookie = cookielib.CookieJar()
		cookiehand = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(cookiehand)
		urllib2.install_opener(opener)

	# 获取主页
	def get_index(self):
		request = urllib2.Request(Nbws.index_url, headers=self.headers)
		response = urllib2.urlopen(request)
		d = pq(response.read())
		self.index_vs = d('#__VIEWSTATE').attr('value')
		self.index_ev = d('#__EVENTVALIDATION').attr('value')
		print 'index_viewstate:%s' % self.index_vs
		print 'index_eventvalidation:%s' % self.index_ev

	# 获取登录页面
	def get_login(self):
		request = urllib2.Request(Nbws.login_url, headers=self.headers)
		response = urllib2.urlopen(request)
		d = pq(response.read())
		self.login_vs = d('#__VIEWSTATE').attr('value')
		self.login_ev = d('#__EVENTVALIDATION').attr('value')
		print 'login_viewstate:%s' % self.login_vs
		print 'login_eventvalidation:%s' % self.login_ev

	# 获取验证码
	def get_validate(self):
		request = urllib2.Request(Nbws.validate_url, headers=self.headers)
		response = urllib2.urlopen(request)
		f = open('tmp.jpg', 'wb')
		f.write(response.read())
		f.close()
		self.validate = raw_input('请输入验证码')

	# 登录
	def login(self, username='keChe', password='0019d29ec656'):
		self.get_index()
		self.get_login()
		self.get_validate()
		para = {
			'__VIEWSTATE': self.login_vs,
			'__EVENTVALIDATION': self.login_ev,
			'hiddenLogin': '',
			'rblInput': '3',
			'txtUserName': username,
			'txtPwd': password,
			'tbValidateCode': self.validate,
			'imgbtnLogin.x': '33',
			'imgbtnLogin.y': '12'
			}
		request = urllib2.Request(Nbws.login_url, urllib.urlencode(para), headers=self.headers)
		response = urllib2.urlopen(request)
		page = response.read()
		if '您好' in page:
			print '登录成功'
		else:
			print '登录失败'
		d = pq(page)
		self.login_vs = d('#__VIEWSTATE').attr('value')
		self.login_ev = d('#__EVENTVALIDATION').attr('value')
		print 'login_viewstate:%s' % self.login_vs
		print 'login_eventvalidation:%s' % self.login_ev

	# 注销
	def logout(self):
		para = {
			'__EVENTTARGET': 'LbtnLogout',
			'__EVENTARGUMENT': '',
			'__VIEWSTATE': self.login_vs,
			'__EVENTVALIDATION': self.login_ev,
			'hiddenLogin': ''
		}
		request = urllib2.Request(self.login_url, urllib.urlencode(para), self.headers)
		response = urllib2.urlopen(request)
		page = response.read()
		if '您好' in page:
			print '注销失败'
		else:
			print '注销成功'





