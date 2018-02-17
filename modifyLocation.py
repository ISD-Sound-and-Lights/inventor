import cgi
import cgitb
from pyassets import *

cgitb.enable()  # enable debugging
dataForm = cgi.FieldStorage()
locations = getLocations()

action = dataForm.getvalue("action")


if action == "create":
	name = dataForm.getvalue("loc-name")
	doAdd = True  # we will change this if we encounter any errors

	# first, we check the name is not already used
	for loc in locations:
		if loc.name == name:  # there was a match!
			dispHTML("h3", contents="You can't add a location with a name the same as one that exists already")
			doAdd = False

	if doAdd:  # no errors? add it!
		locations.append(Location(name))


dataDump(locations)