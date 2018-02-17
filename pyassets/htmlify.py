def getHTML(tag, contents=None, newLine=True, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		if type(paramContent) == str:
			construct += " " + paramName + "=\"" + paramContent + "\""
	if contents is not None:
		construct += ">" + contents + "</" + tag + ">"
	else:
		construct += ">" + "</" + tag + ">"
	if newLine:
		return construct + "\n"
	else:
		return construct


def dispHTML(tag, contents=None, **parameters):
	construct = getHTML(tag, contents=contents, **parameters)
	print(construct)


def startTag(tag, **parameters):
	construct = "<" + tag
	for paramName, paramContent in parameters.items():
		if type(paramContent) == str:
			construct += " " + paramName + "=\"" + paramContent + "\""
	construct += ">"
	print(construct + "\n")


def endTag(tag):
	print("</" + tag + ">")