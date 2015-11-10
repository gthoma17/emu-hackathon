import MySQLdb, string, random, csv, sys, ConfigParser
from datetime import date
from dateutil.rrule import rrule, DAILY




def main():
	config = ConfigParser.ConfigParser()
	config.read("crimes.cfg")


	#db access info
	HOST = "localhost"
	USER = "root"
	PASSWD = ""
	DATABASE = "emu_crimes"
	
	# make a connection to the database
	db_connection = MySQLdb.connect(
	        host=HOST,
	        user=USER, 
	        passwd=PASSWD, 
	        )
	
	#create cursor
	cursor = db_connection.cursor()

	#create our database if it doesn't exist
	try:
		cursor.execute('use '+DATABASE)
	except:
		createDatabase(DATABASE, cursor)
	finally:
		cursor.execute('use '+DATABASE)

	createTables(cursor)
	controlCards = createControlCards("emails.txt")
	createCrimes(cursor, controlCards)


	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def createControlCards(filePath):
	allControlCards = []
	f = open(filePath, 'r')
	for line in f:
		if line != "\n":
			key = line.split(":")[0]
			value = line.split(":")[1]
			print key + " : " + value
			if key == "Date":
				thisDate = value
			if key == "Reported Crime":
				thisCrime = value
			if key == "on_campus":
				thisOnCampus = value
			if key == "Location":
				thisLocation = value
			if key == "email_text":
				thisText = value
		else:
			allControlCards.append([thisLocation, thisDate, thisCrime, thisOnCampus, thisText])
			thisDate = ""
			thisCrime = ""
			thisOnCampus = ""
			thisLocation = ""
			thisText = ""
	f.close()
	return allControlCards

def createTables(cursor):
	#create jobs table if it doesn't exist
	if not tblExists("crimes", cursor):
		createCrimesTbl(cursor)

def createDatabase(DATABASE, cursor): 
	#create our database
	print "Creating database: " +DATABASE
	cursor.execute('create database '+DATABASE)

def createCrimes(cursor, thingsToMake):
	print "creating data for table: crimes"
	#location TEXT(65535),
	#date TEXT(65535),
	#crime TEXT(65535),
	#on_campus TEXT(65535),
	#email_text TEXT(65535),
	addThing = """
	INSERT INTO crimes
		(id, location, date, crime, on_campus, email_text)
    VALUES
    	(NULL, {0}, {1}, {2}, {3}, {4})
	"""
	for thing in thingsToMake:
		thisThingAdd = addThing.format(sanitize(thing[0]), sanitize(thing[1]), sanitize(thing[2]), sanitize(thing[3]), sanitize(thing[4]))
		cursor.execute(thisThingAdd)

def createCrimesTbl(cursor):
	print "Creating table: crimes"
	cursor.execute("""
	CREATE TABLE crimes(
	  id INTEGER  NOT NULL AUTO_INCREMENT,
	  location TEXT(65535),
	  date TEXT(65535),
	  crime TEXT(65535),
	  on_campus TEXT(65535),
	  email_text TEXT(65535),
	  PRIMARY KEY(id)
	)
	""")
def tblExists(name, cursor):
	search_tbl = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = {0}"
	search_tbl = search_tbl.format(sanitize(name))
	cursor.execute(search_tbl)
	if cursor.fetchone()[0] == 1:
		return True
	else:
		return False
def tblEmpty(name, cursor):
	query = """SELECT * from {0} limit 1"""
	entry = cursor.execute(query.format(name))
	if not entry:
		return True
	else:
		return False
def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == "__main__":
	main()	