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