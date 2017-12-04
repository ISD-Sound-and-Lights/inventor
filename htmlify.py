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

print("Content-Type: text/html;charset=utf-8")
print()

# head
dispHTML("head", contents=getHTML("script", src="https://use.fontawesome.com/344eca865b.js"))