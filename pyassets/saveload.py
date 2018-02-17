from pyassets.htmlify import *


def dataDump(locations):
	import pickle
	try:
		dataFile = open(".config/autosave.bin", "wb")
		pickle.dump(locations, dataFile)
		dataFile.close()
	except (FileNotFoundError, PermissionError) as e:
		print(e)
		dispHTML("p", contents="Error in save:  Save file incorrectly configured!")


def getLocations():
	import traceback
	import pickle
	try:
		with open(".config/autosave.bin", "rb") as dataFile:
			return pickle.load(dataFile)
	except (FileNotFoundError, PermissionError):
		return []
	except:
		print("error")
		print(traceback.format_exc())
		return []