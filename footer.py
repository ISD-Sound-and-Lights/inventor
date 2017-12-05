import htmlify
from socket import gethostname as hostname
from time import time as unixTime


def showFooter():
	# Footer
	htmlify.dispHTML("br")
	htmlify.dispHTML("hr")
	heart = "<i class=\"fa fa-heart\" aria-hidden=\"true\" title=\"love\"></i>"
	so = "<i class=\"fa fa-stack-overflow\" aria-hidden=\"true\" title=\"StackOverflow\"></i>"
	tProfileLink = htmlify.getHTML("a", contents="Theo C", href="http://github.com/DyingEcho")
	iProfileLink = htmlify.getHTML("a", contents="Isaac L", href="http://github.com/il8677")
	htmlify.dispHTML("small", contents="Made with " + heart + " and " + so + " by " + tProfileLink + " and " + iProfileLink)
	renderTime = unixTime()
	htmlify.dispHTML("br")
	htmlify.dispHTML("small", contents="Rendered at " + str(round(renderTime)) + " by " + hostname())
