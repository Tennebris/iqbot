class db:
	def insert(cursor, values):
		cursor.execute("INSERT INTO trades VALUES (?,?,?,?,?,?,?)", values)
		return True
