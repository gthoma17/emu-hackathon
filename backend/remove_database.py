import MySQLdb 
import ConfigParser




def main():
	config = ConfigParser.ConfigParser()
	config.read("backend.cfg")


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

	#delete our database
	dropDatabase(DATABASE, cursor)

	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()


def dropDatabase(DATABASE, cursor): 
	#create our database
	print "dropping database: " +DATABASE
	cursor.execute('drop database '+DATABASE)

if __name__ == "__main__":
	main()	