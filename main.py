#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
from socket import gethostname as hostname
from time import time as unixTime
from htmlify import dispHTML, getHTML

# enable debugging
cgitb.enable()

loggedIn = False

print("Content-Type: text/html;charset=utf-8")
print()

# head
dispHTML("head", contents=getHTML("script", src="https://use.fontawesome.com/344eca865b.js"))

# Title and menu
title = getHTML("h1", "InventoryControl")  # title
menuItemHome = getHTML("li", contents=getHTML("a", contents="Home", href="/"))  # menu item 1 -- Home
menuItemHelp = getHTML("li", contents=getHTML("a", contents="Help", href="/help"))  # menu item 2 -- Help
menuItemLogin = getHTML("li", contents=getHTML("a", contents="Login", href="/login"))  # menu item 3 -- Login
menu = menuItemHome + menuItemHelp + menuItemLogin  # construct a menu but don't output yet
menu = getHTML("div", contents=menu, id="menu")  # put menu into a div id="menu"
header = title + menu  # get a header; don't oput yet.
dispHTML("div", contents=header, id="header")  # put header into div and oput
dispHTML("hr")
dispHTML("br")

# content


# Footer
dispHTML("br")
dispHTML("hr")
heart = "<i class=\"fa fa-heart\" aria-hidden=\"true\"></i>"
so = "<i class=\"fa fa-stack-overflow\" aria-hidden=\"true\"></i>"
tProfileLink = getHTML("a", contents="Theo C", href="http://github.com/DyingEcho")
iProfileLink = getHTML("a", contents="Isaac L", href="http://github.com/il8677")
dispHTML("small", contents="Made with " + heart + " and " + so + " by " + tProfileLink + " and " + iProfileLink)
renderTime = unixTime()
dispHTML("br")
dispHTML("small", contents="Rendered at " + str(round(renderTime)) + " by " + hostname())
