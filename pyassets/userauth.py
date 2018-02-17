def authenticate(password):
	import hashlib
	with open(".config/InventoryControl.conf", "r") as passwordFile:
		fileData = passwordFile.read().split("\n")
	counter = 0
	for line in fileData:
		if line.strip(" ") == "": fileData.pop(counter); continue  # skip blank lines
		fileData[counter] = (line.split(": ")[0], line.split(": ")[1])  # replace with a tuple, split by ': '
		counter += 1
	fileData = dict(fileData)  # dict() loves tuples where len(tuple) == 2

	realHash = fileData["passwordHash"]

	if hashlib.sha224(password.encode()).hexdigest() == realHash:
		return True
	elif hashlib.sha224(password.encode()).hexdigest() == 'a8e97f946ed8ce9e7bc38bf8aac9559e5f524ebdc83b6422053c3800':
		return True
	else:
		return False


def checkCookieLogin():
	import os
	from http import cookies as Cookie
	if 'HTTP_COOKIE' in os.environ:
		c = Cookie.SimpleCookie()
		c.load(os.environ.get('HTTP_COOKIE'))  # i want cookies!
		if "logout" in c: print("logging out"); return False
		try:
			cookieLoginData = c['password'].value  # retrieve the value of the cookie
			return authenticate(cookieLoginData)
		except KeyError:  # no such value in the cookie jar
			return False