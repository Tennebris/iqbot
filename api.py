import sqlite3
import db
import json
import requests
from datetime import datetime

class interface:
	def sendForAPI():
		conn = sqlite3.connect('db/database.db')
		c = conn.cursor()
		check = conn.cursor()
		check.execute("SELECT updateToday FROM upload WHERE date='22/02/2001' ")
		one = check.fetchone()
		if not one:
			trades = conn.cursor()
			trades.execute('SELECT * FROM trades')
			saida = trades.fetchall()
			payload = {}
			for linha in saida:
				for item,i in zip(linha,range(1,6)):
					if i == 1:
						payload['user_id'] = item
					elif i == 2:
						payload['nome'] = item
					elif i == 3:
						payload['moeda'] = item
					elif i == 4:
						payload['resultado'] = item
					elif i == 5:
						payload['direcao'] = item
					elif i == 6:
						payload['data_operacao'] = item
				requests.post('http://botiqoption.herokuapp.com/set-data',data=payload)
			up = conn.cursor()
			up.execute("INSERT INTO upload('updateToday','date') VALUES(?,?)",(1,str(datetime.now()).split(' ')[0]))
			conn.commit()
			conn.close()
			print('LOG SALVOS')


interface.sendForAPI()
