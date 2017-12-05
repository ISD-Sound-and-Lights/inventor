#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import footer
import header
from htmlify import *

cgitb.enable()  # enable debugging
loggedIn = False


# header
header.showHeader()


# content
startTag("div", id="containter")  # start container
endTag("div")  # end containter



# footer
footer.showFooter()