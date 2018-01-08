#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging

import assets
from assets import dispHTML, endTag, startTag

print("Content-Type: text/html;charset=utf-8\n")
print('<meta http-equiv="set-cookie" content="password="";>')
cgitb.enable()  # enable debugging
assets.showHeader()

# content
startTag("div", id="container")  # start container
dispHTML("h3", contents="Logout")
dispHTML("p", contents="You have been logged out.")
startTag("p")
dispHTML("a", href="main.py", contents="Return Home")
endTag("div")  # end container

# footer
assets.showFooter()
