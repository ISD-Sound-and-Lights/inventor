#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
print("Content-Type: text/html;charset=utf-8\n")
import cgi
import cgitb
from pyassets import *

cgitb.enable()  # enable debugging
dataForm = cgi.FieldStorage()
locations = getLocations()

try:
	loggedIn = authenticate(dataForm.getvalue("password"))
	if loggedIn:
		print('<meta http-equiv="set-cookie" content="password=' + cgi.escape(dataForm.getvalue("password")) + '";>')
except AttributeError:  # password == None
	loggedIn = checkCookieLogin()
except (FileNotFoundError, PermissionError):
	dispHTML("p", contents="Error in login: Config file missing or invalid perms set!")
	loggedIn = False
except IndexError as e:
	dispHTML("p", contents="Error in login: Config file incorrectly formatted!")
	loggedIn = False

# header
showHeader(loggedIn)

# content
startTag("div", id="containter")  # start container
if loggedIn:
	# item list
	startTag("div", id="items")
	dispHTML("h3", contents="Items")
	startTag("div", id="itemlist")
	for loc in locations:
		itemNameDisplay = "<div class='dropdown'>"
		itemNameDisplay += "<i class=\"fa fa-info\"></i>"
		itemNameDisplay += "<div class='dropdown-content'>"
		itemNameDisplay += "<a href=\"removeLocation.py?location=" + loc.name + "\"><i class=\"fa fa-fw fa-trash\" aria-hidden=\"true\"></i>Delete</a><br />"
		itemNameDisplay += "<a href=\"editLocation.py?location=" + loc.name + "\"><i class=\"fa fa-fw fa-pencil\" aria-hidden=\"true\"></i>Edit</a><br />"
		itemNameDisplay += "<a href=\"analyseLocation.py?location=" + loc.name + "\"><i class=\"fa fa-fw fa-info\" aria-hidden=\"true\"></i>Info</a><br />"
		itemNameDisplay += "</div>"
		itemNameDisplay += "</div>"
		itemNameDisplay += "<span class=\"locListSeparator\" /> "
		itemNameDisplay += getHTML("b", contents=loc.name)
		print(itemNameDisplay)
		for item in loc.items:
			startTag("p")
			print("<span class=\"itemListIndent\"/>")
			dispHTML("a", contents="<i class=\"fa fa-trash\" aria-hidden=\"true\"></i>",
					href="removeItem.py?location=" + loc.name + "&item=" + item.name)
			dispHTML("a", contents="<i class=\"fa fa-pencil\" aria-hidden=\"true\"></i>",
					href="editItem.py?location=" + loc.name + "&item=" + item.name)
			dispHTML("a", contents="<i class=\"fa fa-info\" aria-hidden=\"true\"></i>",
					href="analyseItem.py?location=" + loc.name + "&item=" + item.name)
			print("<span class=\"itemListSeparator\" /> " + str(item))
			endTag("p")
		if len(loc.items) == 0: dispHTML("br")
	endTag("div")  # end item list
	endTag("div")  # end items

	# item controls
	startTag("div", id="add-item")
	dispHTML("h3", contents="Add item")
	startTag("form", id="add-item-form", method="POST", action="main.py")  # login form
	dispHTML("p", contents="Name:", newLine=False)
	dispHTML("input", type="text", name="item-name")
	dispHTML("p", contents="Quantity:", newLine=False)
	dispHTML("input", type="number", name="item-quantity", min="1")
	dispHTML("br")
	startTag("select", name="item-loc")
	dispHTML("option", value="", disabled="disabled", selected="selected", contents="Location")
	for loc in locations:
		dispHTML("option", value=loc.name, contents=loc.name)
	endTag("select")
	dispHTML("button", contents="submit")
	endTag("form")  #  end login form
	endTag("div")  # end div id=add-item

	# item controls
	startTag("div", id="add-loc")
	dispHTML("h3", contents="Add location")
	startTag("form", id="add-loc-form", method="POST", action="main.py")  # login form
	dispHTML("p", contents="Name:", newLine=False)
	dispHTML("input", type="text", name="loc-name")
	dispHTML("button", contents="submit")
	endTag("form")  #  end login form
	endTag("div")  # end div id=add-item
else:
	dispHTML("h3", contents="Welcome to InventoryControl!")
	dispHTML("p", contents="IC is Sound and Lights' own inventory management system.")
	dispHTML("p", contents="It was developed by the Sound and Lights programming team, and is open source.")
	dispHTML("p", contents="Please login to continue.")
endTag("div")  # end container

# footer
showFooter()

dataDump(locations)
