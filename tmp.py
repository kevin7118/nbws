# encoding=utf-8
import urllib
import urllib2

INDEX_URL = 'http://publish.nbws.gov.cn/Index.shtml'
send_headers = {
 'Host': 'publish.nbws.gov.cn',
 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
}
para = {
	'ctl05': 'UpdatePanel5|imgbtnSearchDoctor',
	'__EVENTTARGET': '',
	'__EVENTARGUMENT': '',
	'__VIEWSTATE': 'LluWZdHB8LKbMyoo0VEx8m5VHnWdB+IBDGR/FM8A0kc+6tUSybeZ/TaMwYFl9TbSBLUlE+QY0FeRXTz/2kNT1S+Hpnw1tC+TjPU/Rw+feZcUBO2T',
	'__VIEWSTATEENCRYPTED': '',
	'__EVENTVALIDATION': '9RKLOOEueKG4XcM7/PlLhpCm1xwnfsDhBBQUIEcR/VyLB8JKyhwvLyvhmZSHcnCq6aES4FEwyG8OLfzM+5xP4I8xL4sE1fGIv4VWkqJAxNs+cb5BkMskjHdDV9Deu7hC+S6K/1rTuxrcBMQdGKAbXZHNI8CFW1JLeHMxHXBAbqa+9o51Q/GzgkxeQAWyoQ5QNFOHQ+FCVVEZLKeUTlA+WMYDSJI7rSvwfybgLYeOjfkUGgYqR5BGYYIWaHG6sAWoyIlshLEInvfUVguG+ewMNSsPncLNSkngoSr2wdRB576JFlxKw6IHjJiZ+g0OyYgrscTM38lzzY/8w5SshWP/XPzrnjVwT3ObM0jrGclBbJWPoIQwf3lO28iKfE6syfjAax20PyjNefV1uYVQxi0nmK4aBIOJRDEfyXmuzW9lFkOlYpyF9ZstXCYpydVicTeOzzy6/qSF+DmeSICWL17Q2BYk0WM1DFgtFZdsZsUFQazjxvVNbczw7a7BE/JrGjUq0RUZFXmjDf+uVSFlaeuBwH/S/jCTbBIvZNlUsK6L2R/4xt68498bCqrSmSwpr9n+uvWMF0kGWVIBCB+XmDjyniM+QqsnSDqL5zg8lg8mRuIaCrgk+Ah742mXUe4ycX4/rgHgAXnmteeJ5KKT6WJW9EFgYscVv7ZnP5EcUR+pWqmeeAMMzomdnRTIjL6E1+iRD8zBaUgmuQcmJrLJefek4NO+JC9Ojs04wcU8xMTkV/MvKqhNiyB/IKM4NA6YdAa/A3z5Hw==',
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
request = urllib2.Request(INDEX_URL, urllib.urlencode(para), send_headers)
response = urllib2.urlopen(request)
redirected = response.geturl()
print redirected
print response.read()
