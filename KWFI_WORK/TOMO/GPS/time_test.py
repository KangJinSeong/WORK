import datetime as dt
import time
# ~ x = dt.datetime.today()
# ~ year = x.year
# ~ month = x.month
# ~ day = x.day
# ~ hour = x.hour
# ~ minute = x.minute
# ~ second = x.second

# ~ dt1 = dt.datetime(year,month,day, hour, minute, second, microsecond = 0)
# ~ print(dt1)
# ~ d = dt.timedelta(seconds = 0.016)
# ~ print(dt1 + d)

# ~ result = []
# ~ result.append(dt1)
# ~ for i in range(97):

	# ~ a = time.time()
	# ~ time.sleep(0.01)
	# ~ b = time.time()
	# ~ delta = b-a
	# ~ dt1 += dt.timedelta(seconds = delta)	
	# ~ result.append(dt1)

# ~ for j in range(len(result))	:
	# ~ print(result[j])

p = dt.datetime.now().second
while True:
	x = dt.datetime.now().second
	if p != x:
		a = dt.datetime.now()
		dt1 = dt.datetime(year = a.year, month = a.month, day = a.day, hour = a.hour, minute = a.minute, second = a.second, microsecond = 0)
		print(a)
		print(dt1)
	p = x

	
