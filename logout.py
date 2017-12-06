#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import footer
import header
import hashlib
import cgitb
from htmlify import *
import cgi


cgitb.enable()  # enable debugging

# header
header.showHeader()

# content
startTag("div", id="container")  # start container
dispHTML("h3", contents="Logout")
loginForm = cgi.FieldStorage()
startTag("form", id="login-form", method="POST", action="/cgi-bin/ic/main.py")  # login form
dispHTML("button", contents="To log out, click here.")
endTag("form")  # end login form
endTag("div")  # end containter


# footer
footer.showFooter()
