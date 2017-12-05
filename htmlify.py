def getHTML(tag, contents=None, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		construct += " " + paramName + "=" + paramContent
	if contents is not None:
		construct += ">" + contents + "</" + tag + ">"
	else:
		construct += ">" + "</" + tag + ">"
	return construct + "\n"


def dispHTML(tag, contents=None, **parameters):
	construct = getHTML(tag, contents=contents, **parameters)
	print(construct)


def startTag(tag, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		construct += " " + paramName + "=" + paramContent
	construct += ">"
	print(construct + "\n")


def endTag(tag):
	print("</" + tag + ">")
