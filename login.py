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
loggedIn = False

# header
header.showHeader()

# content
startTag("div", id="containter")  # start container
dispHTML("h3", contents="Login")
loginForm = cgi.FieldStorage()
startTag("form", id="login-form", method="POST", action="/cgi-bin/ic/main.py")  # login form
dispHTML("p", contents="Password:", newLine=False)
dispHTML("input", type="password", name="password")
dispHTML("button", contents="submit")
endTag("form")  # end login form
endTag("div")  # end containter

if "password" not in loginForm:
	dispHTML("h5", contents="Please enter your password.")


# footer
footer.showFooter()