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

		formatter = logging.Formatter('%(asctime)s|%(filename)s:%(lineno)s|%(levelname)s|%(message)s')

		fh = logging.FileHandler('nbws.log')
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
		self.department_id = None
		self.department_name = None
		self.doctor_id = None
		self.doctor_name = None
		self.schedule_date = None
		self.schedule_apm = None
		self.schedule_num = None
		self.total = None
		self.remain = None
		self.stop_treat_flag = None
		self.yy_list = None
		self.yysjd = None
		self.yysjd_num = None
	
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
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['ret_code'] == 0:
				self.session_id = response_json['return_params']['session_id'].encode('utf-8')
				retval = 'success' 
				hint = 'session_id:%s' % self.session_id
				self.logger.debug(hint.decode('utf-8'))
			else:
				hint = '登录失败'
				self.logger.debug(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '无法获取sessionid'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval

	# 获取医院列表
	def get_hospital(self, hos_name):
		retval = 'fail'
		if self.session_id == None:
			hint = 'session_id 不存在'
			self.logger.error(hint.decode('utf-8'))
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
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['page_count'] != 0:
				hospitals = response_json['return_params']['list']
				for hospital in hospitals:
					if hospital['name'] == hos_name.decode('utf-8'):
						self.hospital_id = str(hospital['hospital_id'])
						self.hospital_name = hos_name
						retval = 'success'
						hint = '医院名称:%s, 医院编号:%s' % (self.hospital_name, self.hospital_id)
						self.logger.debug(hint.decode('utf-8'))
						break
				if retval == 'fail':
					hint = '未找到该医院, 请检查输入的医院名称'
					self.logger.error(hint.decode('utf-8'))
			else:
				hint = '获取医院列表失败'
				self.logger.error(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '获取医院列表失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval

	# 获取科室
	def get_department(self, dep_name):
		retval = 'fail'
		if self.hospital_id == None:
			hint = '该医院不存在'
			self.logger.error(hint.decode('utf-8'))
			return retval
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
		try:
			response = urllib2.urlopen(request)
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['page_count'] != 0:
				departments = response_json['return_params']['list']
				for department in departments:
					if department['department_name'] == dep_name.decode('utf-8'):
						self.department_name = dep_name
						self.department_id = department['department_id'].encode('utf-8')
						retval = 'success'
						hint = '科室名称:%s, 科室编号:%s' % (dep_name, self.department_id)
						self.logger.debug( hint.decode('utf-8'))
						break
				if retval == 'fail':
					hint = '未找到该科室, 请检查输入的科室名称'
					self.logger.error(hint.decode('utf-8'))
			else:
				hint = '获取科室列表失败'
				self.logger.error(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '获取科室列表失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval

	# 获取医生
	def get_doctor(self, doc_name):
		retval = 'fail'
		if self.department_id == None:
			hint = '该科室不存在'
			self.logger.error(hint.decode('utf-8'))
			return retval
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
		try:
			response = urllib2.urlopen(request)
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['page_count'] != 0:
				doctors = response_json['return_params']['list']
				for doctor in doctors:
					if doctor['doctor_name'] == doc_name.decode('utf-8'):
						self.doctor_name = doc_name
						self.doctor_id = doctor['doctor_id'].encode('utf-8')
						retval = 'success'
						hint = '医生姓名:%s, 医生编号:%s' % (self.doctor_name, self.doctor_id)
						self.logger.debug(hint.decode('utf-8'))
						break
				if retval == 'fail':
					hint = '未找到该医生, 请检查输入的医生姓名'
					self.logger.error(hint.decode('utf-8'))
			else:
				hint = '获取医生列表失败'
				self.logger.error(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '获取医生列表失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval

	# 获取医生坐诊时间
	def get_schedule(self, date, apm=None):
		retval = 'fail'
		if self.doctor_id == None:
			hint = '该医生不存在'
			self.logger.error(hint.decode('utf-8'))
			return retval
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
		try:
			response = urllib2.urlopen(request)
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['ret_code'] == 0:
				schedules = response_json['return_params']['list']
				for schedule in schedules:
					if schedule['schedule_date'] == date.decode('utf-8'):
						schedule_begtime = schedule['schedule_begtime'].encode('utf-8')
						time_set = schedule_begtime.split(' ')
						beginhour = int(time_set[1].split(':')[0])
						if (beginhour < 12 and apm == '上午') or (beginhour >= 12 and apm == '下午'):
							self.schedule_date = date
							self.schedule_apm = apm
							self.schedule_num = schedule['schedule_num'].encode('utf-8')
							self.total = int(schedule['rated_num'])
							self.remain = int(schedule['last_num'])
							self.stop_treat_flag = schedule['stop_treat_flag'].encode('utf-8')
							retval = 'success'
							hint = '坐诊时间: %s %s, 时间编号: %s, 总数: %s, 剩余: %s' % (self.schedule_date, self.schedule_apm, self.schedule_num, self.total, self.remain)
							self.logger.debug(hint.decode('utf-8'))
							break
				if retval == 'fail':
					hint = '该医生无当日坐诊安排，请确认所输日期'
					self.logger.error(hint.decode('utf-8'))
			else:
				hint = '获取该医生时间表失败'
				self.logger.error(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '获取该医生时间表失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval


	# 获取预约时间段
	def get_period(self):
		retval = 'fail'
		if self.schedule_num == None:
			hint = '无该日坐诊安排'
			self.logger.error(hint.decode('utf-8'))
			return retval
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
		try:
			response = urllib2.urlopen(request)
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0:
				if response_json['return_params']['ret_code'] == 0:
					self.yy_list = response_json['return_params']['list']
					retval = 'success'
					hint = '获取预约时间段成功'
					self.logger.debug(hint.decode('utf-8'))
				elif response_json['return_params']['ret_code'] == 1003:
					self.yy_list = []
					retval = 'success'
					hint = '该排班不存在预约时间段！'
					self.logger.debug(hint.decode('utf-8'))
				# if self.remain != 0:
				# 	self.yysjd = periods[self.total-self.remain]['yysjd'].encode('utf-8')
				# 	self.yysjd_num = periods[self.total-self.remain]['yysjd_num'].encode('utf-8')
				# 	retval = 'success'
				# 	hint = '时间段:%s, 时间编号:%s' % (self.yysjd, self.yysjd_num)
				# 	self.logger.debug(hint.decode('utf-8'))
				# else:
				# 	hint = '该时间段号已挂完'
				# 	self.logger.debug(hint.decode('utf-8'))
			else:
				hint = '获取预约时间段失败'
				self.logger.error(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '获取预约时间段失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval

	# 挂号
	def submit(self):
		retval = 'fail'
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
		try:
			response = urllib2.urlopen(request)
			response_json = json.loads(response.read())
			if response_json['return_code'] == 0 and response_json['return_params']['ret_code'] == 0:
				retval = 'success'
				hint = '挂号成功'
				self.logger.debug(hint.decode('utf-8'))
			else:
				hint = response_json['return_params']['ret_info'].encode('utf-8')
				self.logger.debug(hint.decode('utf-8'))
		except urllib2.URLError, e:
			if hasattr(e, 'code'):
				hint = 'Error Code: %s 服务器错误' % e.code
				self.logger.error(hint.decode('utf-8'))
			elif hasattr(e, 'reason'):
				hint = 'Reason Code: %s 网络不可达' % e.reason
				self.logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '挂号确认失败'
			self.logger.error(hint.decode('utf-8'))
		finally:
			return retval


if __name__ == '__main__':
	# f = open('config.txt')
	# line = f.readline()
	# params = line.split('|')
	# hos_name = params[0].decode('gbk').encode('utf-8')
	# dep_name = params[1].decode('gbk').encode('utf-8')
	# doc_name = params[2].decode('gbk').encode('utf-8')
	# date = params[3].decode('gbk').encode('utf-8')
	# apm = params[4].decode('gbk').encode('utf-8')
	# test = Nbws()
	# retval = test.login()
	# if retval == 'success':
	# 	retval = test.get_hospital(hos_name)
	# if retval =='success':
	# 	retval = test.get_department(dep_name)
	# if retval == 'success':
	# 	retval = test.get_doctor(doc_name)
	# if retval == 'success':
	# 	retval = test.get_schedule(date, apm)
	# if retval == 'success':
	# 	retval = 'fail'
	# 	while retval != 'success':
	# 		retval = test.get_period()
	# 		retval = test.submit()
	# 		if retval == 'success':
	# 			break
	test = Nbws()
	test.login()
	test.get_hospital('宁波市中医院')
	test.get_department('内科正主任')
	test.get_doctor('陈国云')
	test.get_schedule('2015-10-20', '上午')
	test.get_period()