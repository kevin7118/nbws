# coding=utf-8
import urllib
import urllib2
import cookielib
from pyquery import PyQuery as pq

HOST = 'http://publish.nbws.gov.cn'
INDEX_URL = 'http://publish.nbws.gov.cn/Index.shtml'
LOGIN_URL = 'http://publish.nbws.gov.cn/LoginFrame.shtml'
VALIDE_URL = 'http://publish.nbws.gov.cn/ValidateCode.shtml'
USERNAME = 'keChe'
PASSWORD = '0019d29ec656'
headers = {
 'Host': 'publish.nbws.gov.cn',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
}

cookie = cookielib.CookieJar()
cookiehand = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(cookiehand)
urllib2.install_opener(opener)

# 获取主页
response = urllib2.urlopen(INDEX_URL)
page = response.read()
d = pq(page)
index_viewstate = d('#__VIEWSTATE').attr('value')
index_eventvalidation = d('#__EVENTVALIDATION').attr('value')

print 'index_viewstate:%s' % index_viewstate
print 'index_eventvalidation:%s' % index_eventvalidation

# 获取登录页面
response = urllib2.urlopen(LOGIN_URL)
page = response.read()
d = pq(page)
login_viewstate = d('#__VIEWSTATE').attr('value')
login_eventvalidation = d('#__EVENTVALIDATION').attr('value')
print 'login_viewstate:%s' % login_viewstate
print 'login_eventvalidation:%s' % login_eventvalidation

# 获取验证码
response = urllib2.urlopen(VALIDE_URL)
f = open('tmp.jpg', 'wb')
f.write(response.read())
f.close()
valid_code = raw_input('请输入验证码')

# 登录
para = {
	'__VIEWSTATE': login_viewstate,
	'__EVENTVALIDATION': login_eventvalidation,
	'hiddenLogin': '',
	'rblInput': '3',
	'txtUserName': USERNAME,
	'txtPwd': PASSWORD,
	'tbValidateCode': valid_code,
	'imgbtnLogin.x': '33',
	'imgbtnLogin.y': '12'
	}
postdata = urllib.urlencode(para)
request = urllib2.Request(LOGIN_URL, postdata)
response = urllib2.urlopen(request)
page = response.read()
print '登录:%s' % response.getcode()
print page
d = pq(page)
login_viewstate = d('#__VIEWSTATE').attr('value')
login_eventvalidation = d('#__EVENTVALIDATION').attr('value')
print 'login_viewstate:%s' % login_viewstate
print 'login_eventvalidation:%s' % login_eventvalidation


# 查询医生信息
para = {
	'ctl05': 'UpdatePanel5|imgbtnSearchDoctor',
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'__VIEWSTATE': index_viewstate,
	'__VIEWSTATEENCRYPTED': '',
	'__EVENTVALIDATION': index_eventvalidation,
	'rblDate': 0,
	'ddlRegHospital': '',
	'ddlghzy': 2,
	'ChooseDept1$hfBtnOpenDeptText': '选择科室',
	'ChooseDept1$hfKsdm': '',
	'ChooseDept1$rblDeptDate': 1,
	'ChooseDept1$hfRblDeptDateValue': '1',
	'tbRegEmpName': '卓立甬',
	'hfZXKSDM': '',
	'__ASYNCPOST': 'true',
	'imgbtnSearchDoctor.x': 37,
	'imgbtnSearchDoctor.y': 13
}
request = urllib2.Request(INDEX_URL, urllib.urlencode(para), headers)
response = urllib2.urlopen(request)
data = response.read()
print data
print response.getcode()
data_set = data.split('|')
redirect_url = data_set[len(data_set)-2]
query_url = HOST + redirect_url
print query_url

# 获取查询结果
response = urllib2.urlopen(query_url)
print response.read()

# 注销
logout = raw_input('是否注销')
if logout == 'y':
	para = {
		'__EVENTTARGET': 'LbtnLogout',
		'__EVENTARGUMENT': '',
		'__VIEWSTATE': login_viewstate,
		'__EVENTVALIDATION': login_eventvalidation,
		'hiddenLogin': ''
	}
	request = urllib2.Request(LOGIN_URL, urllib.urlencode(para), headers)
	response = urllib2.urlopen(request)
	print response.read()











