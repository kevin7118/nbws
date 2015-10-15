# coding=utf-8
from requests_futures.sessions import FuturesSession
from logger import logger
import requests
import json

class Nbws(object):
	api_url = 'http://nbpt.ucmed.cn/api/exec.htm'
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
		'User-Agent':  '1.2.0 (iPhone; iPhone OS 9.0; zh_CN)',
		'Accept-Encoding':' gzip',
		'Connection': 'close'
	}

	def __init__(self):
		self.session = FuturesSession()
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
		payload = {'requestData': data_json}
		try:
			response = self.session.post(Nbws.api_url, data=payload, headers=Nbws.headers).result()
			response_json = response.json()
			if response_json['return_code'] == 0 and response_json['return_params']['ret_code'] == 0:
				self.session_id = response_json['return_params']['session_id'].encode('utf-8')
				retval = 'success' 
				hint = 'session_id:%s' % self.session_id
				logger.debug(hint.decode('utf-8'))
			else:
				hint = '登录失败'
				logger.debug(hint.decode('utf-8'))
		except requests.RequestException, e:
				hint = '网络问题'
				logger.error(hint.decode('utf-8'))
		except KeyError, e:
			hint = '无法获取sessionid'
			logger.error(hint.decode('utf-8'))
		finally:
			return retval

if __name__ == '__main__':
		
		test = Nbws()
		test.login()