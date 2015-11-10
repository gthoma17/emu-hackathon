import web, ConfigParser, json, string, random, socket, urllib, datetime
from os import path
from identitytoolkit import gitkitclient

#prepare to read config
config = ConfigParser.ConfigParser()
root = path.dirname(path.realpath(__file__))

config.read(path.join(root, "crimes.cfg"))


urls = (
	"/", "index",
	"/crimes", "crimes",
	"/crimes/(.*)", "select_crime",
	)

app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "host"), port=int(config.get("Database", "port")), user=config.get("Database", "user"), pw=config.get("Database", "password"), db=config.get("Database", "name"))
def set_headers():
    web.header('Access-Control-Allow-Origin',      '*')
app.add_processor(web.loadhook(set_headers))

class index:
	def GET(self): 
		return "Shhhh... the database is sleeping."
	def POST(self):
		return "Shhhh... the database is sleeping."
class select_crime:
	def GET(self, crime):
		theseCrimes = db.select('crimes', where="crime like '%"+crime+"%'")
		#August 13, 2013
		holdCrimes = []
		for crime in theseCrimes:
			crimeDate = crime['date'].split()
			if len(crimeDate) > 0:
				crimeDate[1].replace(',', '')
				if len(crimeDate[1]) == 1:
					crimeDate[1] = "0" + crimeDate[1]
				crime['datetime'] = datetime.datetime.strptime(" ".join(crimeDate), "%B %d, %Y")
				holdCrimes.append(crime)
		holdCrimes.sort(key=lambda item:item['datetime'], reverse=True)
		return json.dumps(list(makeDumpable(holdCrimes)))
	def POST(self):
		return "Shhhh... the database is sleeping."

class crimes:
	def GET(self): 
		allCrimes = db.select('crimes')
		#August 13, 2013
		holdCrimes = []
		for crime in allCrimes:
			crimeDate = crime['date'].split()
			if len(crimeDate) > 0:
				crimeDate[1].replace(',', '')
				if len(crimeDate[1]) == 1:
					crimeDate[1] = "0" + crimeDate[1]
				crime['datetime'] = datetime.datetime.strptime(" ".join(crimeDate), "%B %d, %Y")
				holdCrimes.append(crime)
		holdCrimes.sort(key=lambda item:item['datetime'], reverse=True)


		return json.dumps(list(makeDumpable(holdCrimes)))
	def POST(self):
		return "Shhhh... the database is sleeping."
def makeDumpable(inList):
	for crime in inList:
		for thing in crime:
			if type(crime[thing]) is datetime.date or \
				type(crime[thing]) is datetime.datetime:
				crime[thing] = str(crime[thing])
	return inList
if __name__ == "__main__":
	app.run()
