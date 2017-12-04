#!/usr/local/bin/python3
#  ^^^ this is bad practice, DON'T do as I did!
import cgitb  # debugging
import assets.footer as footer
import assets.header as header

cgitb.enable()  # enable debugging
loggedIn = False


# header
header.showHeader()


# content


# footer
footer.showFooter()