import sqlite3
import db
import json
import requests
from datetime import datetime


class interface:
	#data = ['1234','alysson','real','win','call','22-02-2001']
	def upload(data):
		payload = {}
		for item,i in zip(data,range(1,7)):
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
				payload['created_at'] = item

		requests.post('http://botiqoption.herokuapp.com/set-data',data=payload)
		print('ok')

