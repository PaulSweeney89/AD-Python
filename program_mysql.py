import pymysql
#import tabulate



def get_films():
	"""
	Function to view films & actors
	"""
	db = pymysql.connect(host="localhost", user="root", password="root", db="MoviesDB", cursorclass=pymysql.cursors.DictCursor, port=3306)
	query = """	SELECT f.FilmName, a.ActorName
    				FROM Film f
				INNER JOIN FilmCast fc
    				ON f.FilmID = fc.CastFilmID
				INNER JOIN Actor a
    				ON fc.CastActorID = a.ActorID
				ORDER BY f.FilmName, a.ActorName;
			"""

	with db:
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()

		while True:
			rows = cursor.fetchmany(5)
			for row in rows:
				print(row["FilmName"], " : ", row["ActorName"])
			quit = input("-- Quit <q> --")
			if quit == "q":
				break



def get_actor(year, gender):
	"""
	Function to view actor, month of birth & gender
	"""
	db = pymysql.connect(host="localhost", user="root", password="root", db="MoviesDB", cursorclass=pymysql.cursors.DictCursor, port=3306)

	query = """	SELECT ActorName, MONTHNAME(ActorDOB), ActorGender
					FROM Actor
				WHERE YEAR(ActorDOB) = %s AND ActorGender = %s;
			"""

	with db:
		cursor = db.cursor()
		cursor.execute(query, (year, gender))
		db.commit()
		result = cursor.fetchall()

		return result



def get_studios():
	"""
	Function to view studios
	"""
	db = pymysql.connect(host="localhost", user="root", password="root", db="MoviesDB", cursorclass=pymysql.cursors.DictCursor, port=3306)


	query = "SELECT * FROM Studio ORDER BY StudioID;"

	with db:
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()
		result = cursor.fetchall()

		return result



def add_country(ID, name):
	"""
	Function to add a new country
	"""
	db = pymysql.connect(host="localhost", user="root", password="root", db="MoviesDB", cursorclass=pymysql.cursors.DictCursor, port=3306)

	query = """ INSERT INTO Country
				(CountryID, CountryName)
				VALUES (%s, %s)
			"""

	with db:
		try:
			cursor = db.cursor()
			cursor.execute(query, (ID, name))
			db.commit()
			print("Country:", ID, name, "added to database")
		except pymysql.err.IntegrityError:
			print("*** Error ***: ID and/or Name <", ID, ",", name, "already exists")



def get_filmsyn(ID):
	"""
	Function to retrieve Film Name & Synopsis with Film ID Input
	"""
	db = pymysql.connect(host="localhost", user="root", password="root", db="MoviesDB", cursorclass=pymysql.cursors.DictCursor, port=3306)
	

	query = """ SELECT FilmName, SUBSTRING(FilmSynopsis, 1, 30)
				FROM Film
				WHERE FilmID IN (%s)
			"""

	in_p=', '.join(list(map(lambda x: '%s', ID)))
	query = query % in_p

	with db:
		cursor = db.cursor()
		cursor.execute(query, (ID))
		db.commit()
		result = cursor.fetchall()

		return result