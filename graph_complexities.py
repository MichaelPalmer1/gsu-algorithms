from matplotlib import pyplot as p
import numpy
import math
import re
n = 100

# quad = re.compile('^(\d+[a-z]\^2) [+-] (\d+[a-z]) [+-] (\d+)$')
# cube = re.compile('^(\d+[a-z]\^3) [+-] (\d+[a-z]\^2) [+-] (\d+[a-z]) [+-] (\d+)$')
exp = re.compile('\d*[a-z]\^(\d+)')
sexp = re.compile('(\d+)\^[a-z]')
lin = re.compile('(\d*)[a-z]')
log = re.compile('(log[(][a-z][)])')
con = re.compile('(\d+)')


def max_term(e):
	o = 0
	o_type = ''
	parts = e.split()

	for s in parts:
		if s == '+' or s == '-':
			continue
		else:
			print(s)
			if sexp.match(s):
				o = int(sexp.match(s).group(1))
				o_type = 'super'
			elif exp.match(s):
				x = int(exp.match(s).group(1))
				if o_type == 'super' or (o_type == 'exponent' and x <= o):
					continue
				o = x
				o_type = 'exponent'
			elif log.match(s):
				if o_type == 'super' or o_type == 'exponent' or o_type == 'linear':
					continue
				o_type = 'log'
				o = log.match(s).group(1)
			elif lin.match(s):
				if o_type == 'super' or o_type == 'exponent':
					continue
				o_type = 'linear'
			elif con.match(s):
				if o_type != '' and o_type != 'constant':
					continue
				o_type = 'constant'
	print("----")
	if o_type == 'super':
		print("O(%d^n)" % o)
	elif o_type == 'exponent':
		print("O(n^%d)" % o)
	elif o_type == 'linear':
		print("O(n)")
	elif o_type == 'log':
		print("O(%s)" % o)
	elif o_type == 'constant':
		print("O(1)")
	print("----")

	return o_type, o


ex = raw_input('Enter expression: ')
ot, o = max_term(ex)

# if ot != 'super':
# 	x = numpy.ones(n)
# 	y = numpy.ones(n)
# 	for i in range(n):
# 		x[i] = i
# 		y[i] = math.pow(2, x[i])
# 	p.plot(x, y, label='O(2^n)', color='blue')
if ot != 'exponent':
	x = numpy.ones(n)
	y = numpy.ones(n)
	for i in range(n):
		x[i] = i
		y[i] = math.pow(x[i], 2)
	p.plot(x, y, label='O(n^2)', color='blue')
if ot != 'linear':
	x = numpy.ones(n)
	y = numpy.ones(n)
	for i in range(n):
		x[i] = i
		y[i] = x[i]
	p.plot(x, y, label='O(n)', color='blue')
if ot != 'log':
	x = numpy.ones(n)
	y = numpy.ones(n)
	for i in range(n):
		x[i] = i
		y[i] = math.fabs(x[i] * numpy.log(x[i]))
	p.plot(x, y, label='O(log(n))', color='blue')
if ot != 'constant':
	x = numpy.ones(n)
	y = numpy.ones(n)
	for i in range(n):
		x[i] = i
		y[i] = 1
	p.plot(x, y, label='O(1)', color='blue')

x = numpy.ones(n)
y = numpy.ones(n)
if ot == 'super':
	for i in range(n):
		x[i] = i
		y[i] = math.pow(o, x[i])
	p.plot(x, y, label='O(%d^n)' % o, color='red')
elif ot == 'exponent':
	for i in range(n):
		x[i] = i
		y[i] = math.pow(x[i], o)
	p.plot(x, y, label='O(n^%d)' % o, color='red')
elif ot == 'linear':
	for i in range(n):
		x[i] = i
		y[i] = x[i]
	p.plot(x, y, label='O(n)', color='red')
elif ot == 'log':
	for i in range(n):
		x[i] = i
		y[i] = math.fabs(x[i] * numpy.log(x[i]))
	p.plot(x, y, label='O(log(n))', color='red')
elif ot == 'constant':
	for i in range(n):
		x[i] = i
		y[i] = 1
	p.plot(x, y, label='O(1)', color='red')

p.legend()
p.show()

exit()

slope = 0.5
intersection = 2
a = 1
b = 2
c = -2


for i in range(n):
	x[i] = i
	y[i] = math.fabs(slope * x[i] + intersection)

p.plot(x, y, label='n', color='green')

x = numpy.ones(n)
y = numpy.ones(n)
for i in range(n):
	x[i] = i
	y[i] = math.fabs(i * numpy.log(i))

p.plot(x, y, label='n log(n)', color='red')

x = numpy.ones(n)
y = numpy.ones(n)
for i in range(n):
	x[i] = i
	y[i] = math.fabs(a * x[i] * x[i] + b * x[i] + c)
p.plot(x, y, label='n^2', color='blue')

p.legend()
p.show()
