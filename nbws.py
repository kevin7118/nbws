# coding=utf-8
import urllib
import urllib2
import cookielib
import json
import logging

class Nbws(object):
	api_url = 'http://nbpt.ucmed.cn/api/exec.htm'
	header = {
		'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
		'User-Agent':  '1.2.0 (iPhone; iPhone OS 9.0; zh_CN)',
		'Accept-Encoding':' gzip',
		'Connection': 'close'
	}

	def __init__(self):
		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		# proxy_handler = urllib2.ProxyHandler({'http':'http://luweibo.nb:kevin7118@36.0.223.1:80'})

		opener = urllib2.build_opener(cookie_handler)
		urllib2.install_opener(opener)

		self.logger = logging.getLogger('mylogger')
		self.logger.setLevel(logging.DEBUG)

		formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s')

		fh = logging.FileHandler('test.log')
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(formatter)

		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		ch.setFormatter(formatter)

		self.logger.addHandler(fh)
		self.logger.addHandler(ch)

		self.session_id = None
		self.hospital_name = None
		self.hospital_id = None
	
	# 登录 
	def login(self, username='keChe', password='0019d29ec656'):
		retval = 'fail'
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
			    "login_name" : username,
			    "login_password" : password
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : "",
			"api_name" : "api.nbpt.user.login"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		try:
			response = urllib2.urlopen(request)
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				self.logger.error('Error Code: %s 服务器错误' % e.code)
			elif hasattr(e, 'reason'):
				self.logger.error('Reason Code: %s 网络不可达' % e.reason)
		else:
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['ret_code'] == 0:
				self.session_id = response_json['return_params']['session_id'].encode('utf-8')
				retval = 'success' 
				hint = 'session_id:%s' % self.session_id
				self.logger.debug(hint)
			else:
				self.logger.debug('登录失败')
		finally:
			return retval

	# 获取医院列表
	def get_hospital(self, hos_name):
		retval = 'fail'
		if self.session_id == None:
			retval = 'no session_id'
			self.logger.error('session_id 不存在')
			return retval
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
			  "city" : "宁波"
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.zwjk.find.hospital_app_by_city"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		try:
			response = urllib2.urlopen(request)
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				self.logger.error('Error Code: %s 服务器错误' % e.code)
			elif hasattr(e, 'reason'):
				self.logger.error('Reason Code: %s 网络不可达' % e.reason)
		else:
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['page_count'] != 0:
				hospitals = response_json['return_params']['list']
				for hospital in hospitals:
					if hospital['name'] == hos_name.decode('utf-8'):
						self.hospital_id = str(hospital['hospital_id'])
						self.hospital_name = hos_name
						retval = 'success'
						hint = '医院名称:%s, 医院编号:%s' % (self.hospital_name, self.hospital_id)
						self.logger.debug(hint)
						break
				if retval == 'fail':
					retval = 'wrong hos_name'
					self.logger.error('未找到该医院名')
			else:
				self.logger.error('获取医院列表失败')
		finally:
			return retval

	# 获取科室
	def get_department(self, dep_name):
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
				"page_size" : "1000",
				"hospital_name" : self.hospital_name,
				"hospital_id" : self.hospital_id,
				"page_no" : "1"
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.nbpt.department.list"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		response = urllib2.urlopen(request)
		response_json = json.loads(response.read())
		departments = response_json['return_params']['list']
		for department in departments:
			if department['department_name'] == dep_name.decode('utf-8'):
				self.department_name = dep_name
				self.department_id = department['department_id'].encode('utf-8')
				hint = '科室名称:%s, 科室编号:%s' % (dep_name, self.department_id)
				print hint.decode('utf-8')
				break

	# 获取医生
	def get_doctor(self, doc_name):
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
				"page_size" : "1000",
				"hospital_id" : self.hospital_id,
				"department_id" : self.department_id,
				"page_no" : "1"
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.nbpt.doctor.list"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		response = urllib2.urlopen(request)
		response_json = json.loads(response.read())
		doctors = response_json['return_params']['list']
		for doctor in doctors:
			if doctor['doctor_name'] == doc_name.decode('utf-8'):
				self.doctor_name = doc_name
				self.doctor_id = doctor['doctor_id'].encode('utf-8')
				hint = '医生姓名:%s, 医生编号:%s' % (self.doctor_name, self.doctor_id)
				print hint.decode('utf-8')
				break

	#选择时间
	def get_schedule(self, date, apm=None):
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
				"page_size" : "1000",
				"doctor_id" : self.doctor_id,
				"hospital_id" : self.hospital_id,
				"department_id" : self.department_id,
				"page_no" : "1"
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.nbpt.doctor.detail"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		response = urllib2.urlopen(request)
		response_json = json.loads(response.read())
		schedules = response_json['return_params']['list']
		for schedule in schedules:
			if schedule['schedule_date'] == date.decode('utf-8'):
				self.schedule_date = date
				self.schedule_num = schedule['schedule_num'].encode('utf-8')
				self.total = int(schedule['rated_num'])
				self.remain = int(schedule['last_num'])
				self.stop_treat_flag = schedule['stop_treat_flag'].encode('utf-8')
				hint = '时间编号:%s, 总数:%d, 剩余:%d' % (self.schedule_num, self.total, self.remain)
				print hint.decode('utf-8')
				break

	# 选择所挂号
	def get_period(self):
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
				"schedule_num" : self.schedule_num
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.nbpt.reservation.period.list"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		response = urllib2.urlopen(request)
		response_json = json.loads(response.read())
		periods = response_json['return_params']['list']
		self.yysjd = periods[self.total-self.remain]['yysjd'].encode('utf-8')
		self.yysjd_num = periods[self.total-self.remain]['yysjd_num'].encode('utf-8')
		hint = '时间段:%s, 时间编号:%s' % (self.yysjd, self.yysjd_num)
		print hint.decode('utf-8')

	# 挂号
	def submit(self):
		requestData = {
			"app_id" : "zsyy_android",
			"params" : {
				"schedule_date" : self.schedule_date,
				"yysjd" : self.yysjd,
				"schedule_num" : self.schedule_num,
				"yysjd_num" : self.yysjd_num
			},
			"client_version" : "1.2.0",
			"app_key" : "ZW5sNWVWOWhibVJ5YjJsaw==",
			"api_Channel" : "3",
			"client_mobile" : "",
			"user_type" : "3",
			"session_id" : self.session_id,
			"api_name" : "api.nbpt.reservation.submit"
		}
		data_json = json.dumps(requestData)
		data = {'requestData': data_json}
		request = urllib2.Request(Nbws.api_url, urllib.urlencode(data), Nbws.header)
		response = urllib2.urlopen(request)
		print response.read()

if __name__ == '__main__':

	test = Nbws()
	test.login()
	test.get_hospital('宁波市中医院')
	test.get_department('内科正主任')
	test.get_doctor('卓立甬')
	test.get_schedule('2015-10-22')
	test.get_period()
	test.submit()
	

