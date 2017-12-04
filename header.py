import htmlify

def showHeader():
	# Title and menu
	title = htmlify.getHTML("h1", "InventoryControl")  # title
	menuItemHome = htmlify.getHTML("li", contents=htmlify.getHTML("a", contents="Home", href="/"))  # menu item 1 -- Home
	menuItemHelp = htmlify.getHTML("li", contents=htmlify.getHTML("a", contents="Help", href="/help"))  # menu item 2 -- Help
	menuItemLogin = htmlify.getHTML("li", contents=htmlify.getHTML("a", contents="Login", href="/login"))  # menu item 3 -- Login
	menu = menuItemHome + menuItemHelp + menuItemLogin  # construct a menu but don't output yet
	menu = htmlify.getHTML("div", contents=menu, id="menu")  # put menu into a div id="menu"
	header = title + menu  # get a header; don't oput yet.
	htmlify.dispHTML("div", contents=header, id="header")  # put header into div and oput
	htmlify.dispHTML("hr")
	htmlify.dispHTML("br")