import json

async def getOverallTitle(wins):
	with open('json/dueltitles.json') as f:
		divTitles = json.load(f)
	
	titleIntList = list(divTitles)

	if int(wins) < 100:
		return "None"
	elif int(wins) > 56000:
		return "Godlike X"
	else:
		for x in range(len(titleIntList)):
			if int(wins) > int(titleIntList[x]) and int(wins) < int(titleIntList[x+1]):
				return divTitles[titleIntList[x]]


async def getDivisionTitle(wins):
	with open('json/duelsdivtitles.json') as f:
		divTitles = json.load(f)
	
	titleIntList = list(divTitles)

	if int(wins) < 50:
		return "None"
	elif int(wins) > 28000:
		return "Godlike X"
	else:
		for x in range(len(titleIntList)):
			if int(wins) > int(titleIntList[x]) and int(wins) < int(titleIntList[x+1]):
				return divTitles[titleIntList[x]]

