#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgi
import cgitb  # debugging

import assets
import footer
import header
from assets import dispHTML, endTag, startTag

print("Content-Type: text/html;charset=utf-8")
print()


cgitb.enable()  # enable debugging
loggedIn = False

# header
assets.showHeader()

# content
startTag("div", id="containter")  # start container
dispHTML("h3", contents="Login")
loginForm = cgi.FieldStorage()
startTag("form", id="login-form", method="POST", action="main.py")  # login form
dispHTML("p", contents="Password:", newLine=False)
dispHTML("input", type="password", name="password")
dispHTML("button", contents="submit")
endTag("form")  # end login form
endTag("div")  # end containter

if "password" not in loginForm:
	dispHTML("h5", contents="Please enter your password.")


# footer
assets.showFooter()