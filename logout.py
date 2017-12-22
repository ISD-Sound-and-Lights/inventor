#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import footer
import header
from htmlify import *


print("Content-Type: text/html;charset=utf-8\n")
print('<meta http-equiv="set-cookie" content="password="";>')
cgitb.enable()  # enable debugging
header.showHeader()

# content
startTag("div", id="container")  # start container
dispHTML("h3", contents="Logout")
dispHTML("p", contents="You have been logged out.")
startTag("p")
dispHTML("a", href="/cgi-bin/ic/main.py", contents="Return Home")
endTag("div")  # end container


# footer
footer.showFooter()
