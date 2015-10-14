# coding=utf-8
dx = u'零壹贰叁肆伍陆柒捌玖'
dw = ['', u'拾', u'佰', u'仟']
def print_num(num):
	result = ''
	i = 0
	while num > 0:
		cur = num % 10
		if cur == 0:
			if result and result[0] != u'零':
				result = u'零' + result
		else:
			result = dx[cur] + dw[i] + result
		num /= 10
		i += 1
	return result
a = 10100101
result = ''
if a == 0:
	result = u'零圆'
elif a == 10:
	result = u'拾圆'
elif a == -10:
	result = u'负拾圆'
else:
	if a < 0:
		a *= -1
		result = u'负'
	big = a / 10000
	small = a % 10000
	if big:
		if (big % 10 == 0 and small > 0) or (small < 1000 and small > 0):
			result += print_num(big) + u'万零' + print_num(small) + u'圆'
		else:
			result += print_num(big) + u'万' + print_num(small) + u'圆'
	else:
		result += print_num(small) + u'圆'
print result
