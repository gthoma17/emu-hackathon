from bs4 import BeautifulSoup
import re, requests, sys

reload(sys)  
sys.setdefaultencoding('utf8')

def main():
	warningDelimeter = re.compile("_{100,200}")
	warningDateRegex = re.compile("^.*(\b\d{1,2}\D{0,3})?\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?)\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2}).*")
	warningNumberRegex = re.compile("^.*\d{2}-\d{1,3},? .*$")
	warningNumberSplitRegex = re.compile("\d{2}-\d{1,3},? ")
	warningReportedCrime = re.compile(".*REPORTED CRIME.*(:|-).*")
	warningIncident = re.compile(".*INCIDENT.*(:|-).*")
	warningLocation = re.compile("(LOCATION):{1}")
	warningLocationRegexMain = re.compile(":\s.*([A-Z0-9]).*\s")
	warningLocationRegex = re.compile(".*\d{3,5}.*BLOCK OF")
	warningLocationRegexStrict = re.compile("\d{3,5}\s*BLOCK OF.*")
	warningLocationDirection = re.compile("(\(NORTH)|(\(SOUTH)|(\(WEST)|(\(EAST)|(AT APPROXIMATELY)|(NEXT)|(,\s)|(THE YPSI)|(YPSILANTI POLICE)|(IN THE CITY)|(.THE VICTIM)")


	timelyWarningsPage = requests.get("http://www.emich.edu/police/alerts/safetynotices/index.php")
	timelyWarnings = BeautifulSoup(timelyWarningsPage.text).findAll("div",attrs={'id':'textcontainer'})[0].text
	thisWarning = []
	allWarnings = []
	thisWarningDict = {}
	allWarningDicts = []
	debug = False
	inBody = False
	loc_dir = 0
	global loc_temp
	timelyLines = iter(timelyWarnings.splitlines())
	for line in  timelyLines:
		line = line.decode('utf-8')
		if warningDelimeter.match(line):
			allWarnings.append(thisWarning)
			if 'crime' not in thisWarningDict.keys():
				#print "\n".join(thisWarning)
				pass
			allWarningDicts.append(thisWarningDict)
			thisWarning = []
			thisWarningDict = {}
			debug = False
			inBody = False
		else:
			thisWarning.append(line)
		if warningNumberRegex.match(line) or '15-6' in line or '15-15' in line:
			if "update".upper() not in line.upper():
				if "15-03" in line:
					thisDate = "March 9, 2015"
				elif "15-9" in line:
					thisDate = "July 21, 2015"
				elif "15-8" in line:
					thisDate = "July 18, 2015"
				elif "15-15" in line:
					thisDate = "October 15, 2015"
				else:
					thisDate = line.partition(",")[-1]
				thisDate = thisDate.strip()
				thisWarningDict['date'] = thisDate
				#warningDates.append(thisDate)
		if warningReportedCrime.match(line.upper()) or warningIncident.match(line.upper()):
			tokens = line.replace(u'\xa0', "-").replace("-",":")
			tokens = tokens.replace(u'\u2013',"-").replace("-",":")
			tokens = tokens.replace(u'Date and time of incident',"")
			tokens = tokens.split(":")
			tokens = [x for x in tokens if x]
			upper_tokens = [token.upper().rstrip() for token in tokens]
			your_token = [token for token in tokens if 'OFF CAMPUS' in token.upper()]
			if your_token:
				thisWarningDict['onCampus'] = False
				your_token = None
			else:
				thisWarningDict['onCampus'] = True
			your_token = [token for token in tokens if 'STREET' in token.upper()]
			if your_token:
				thisWarningDict['location'] = your_token[0]
				your_token = None
			your_token = [token for token in tokens if 'GREEN LOT 1' in token.upper()]
			if your_token:
				thisWarningDict['location'] = your_token[0]
				your_token = None
			your_token = [token for token in tokens if warningLocationRegex.match(token.upper())]
			if your_token:
				thisWarningDict['location'] = your_token[0]
				your_token = None
			if "REPORTED CRIME" in upper_tokens:
				crime_int = upper_tokens.index("REPORTED CRIME") + 1
				thisWarningDict['crime'] = tokens[crime_int]
				while thisWarningDict['crime'] == ' ':
					crime_int = crime_int + 1
					thisWarningDict['crime'] = tokens[crime_int]
				if "City of Ypsilanti, Off Campus" in tokens[crime_int]:
					loc_index = tokens[crime_int].index(", City of Ypsilanti, Off Campus")
					thisWarningDict['crime'] = tokens[crime_int][:loc_index]
				inBody = True
				crime_int = None
				loc_index = None
			if "INCIDENT" in upper_tokens:
				crime_int = upper_tokens.index("INCIDENT") + 1
				thisWarningDict['crime'] = tokens[crime_int]
				while thisWarningDict['crime'] == ' ':
					crime_int +=1
					thisWarningDict['crime'] = tokens[crime_int]
				if "Location" in tokens[crime_int]:
					loc_index = tokens[crime_int].index("Location")
					thisWarningDict['crime'] = tokens[crime_int][:loc_index]
				inBody = True
				crime_int = None
				loc_index = None
				upper_tokens = None
			#print tokens
		if warningLocation.match(line.upper()):
			line = line.replace("Location:","")
			if 'location' not in thisWarningDict.keys():
				thisWarningDict['location'] = line
				#print line
		if inBody:
			if warningLocationRegex.match(line.upper()):
				string_hold = line + next(timelyLines)
				loc_hold = warningLocationRegexStrict.search(string_hold.upper()).group(0)
			else:
				loc_hold = None
			if loc_hold:
				loc_dir = warningLocationDirection.search(loc_hold.upper())
				if loc_dir:
					loc_ind = loc_dir.start()
					loc_hold = loc_hold[:loc_ind]
				else:
					loc_ind = 0;
				thisWarningDict['location'] = loc_hold
		if debug:
			print line
	for warning in allWarningDicts:
		print "____________________________________________________"
		print warning
if __name__ == "__main__":
	main()