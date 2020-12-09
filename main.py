import json
import sys
import time
import datetime
import random
import sqlite3
from iqoptionapi.stable_api import IQ_Option

import iqconfig
import db
import api as upload

api = IQ_Option('dev.alysson@gmail.com','nephilin890')
api.connect()

while True:
	if api.check_connect() == False:
		print("Erro ao conectar!")
		api.connect()
	else:
		print("Conectado com sucesso!")
		break

def main():
	opens = []

	opensPar = api.get_all_open_time()	
	for openPar in opensPar['binary']:
		if opensPar['binary'][openPar]['open'] == True:
			opens.append(openPar)

	name = 'live-deal-binary-option-placed' # live-deal-binary-option-placed
	active = opens[random.randint(0,len(opens)-1)]
	typeOP = 'turbo' # PT1M
	bufferSize = 10
	prev = 0

	tops = iqconfig.iq.getRank(api)
	api.subscribe_live_deal(name,active,typeOP, bufferSize)
	try: 
		while True:
			operacoes = api.get_live_deal(name,active,typeOP)
			if(time.strftime('%H') == '00' and int(time.strftime('%M')) >= 0):
				upload.sendForAPI()

			if len(operacoes) > 0 and operacoes[0]['user_id'] != prev:
				#print(json.dumps(operacoes[0],indent=1))	
				if len(tops['userID']) > 0:
					if operacoes[0]['user_id'] in tops['userID']:
						rankPosition = int()
						horaOP = str(datetime.datetime.now()).split('.')[0]

						for userID, rank in zip(tops['userID'],tops['rank']):
							if userID == operacoes[0]['user_id']:
								rankPosition = rank

						trade = active+" "+str(operacoes[0]['amount_enrolled'])+" "+operacoes[0]['direction']+" "+str(operacoes[0]['user_id'])+" "+rankPosition+" "+operacoes[0]['name']
						print(trade)

						retorno, result = iqconfig.iq.operar(api,operacoes[0]['amount_enrolled'],active,operacoes[0]['direction'])
						if not retorno:
							return False
						print(result)
						
						nome = ''

						array = trade.split()
						if len(array) > 6:
							nome = array[5]+" "+array[6]
						else:
							nome = array[5]			
						
						conn = sqlite3.connect('db/database.db')
						c = conn.cursor()
						
						if db.db.insert(c,(array[3],nome,rankPosition,array[0],result[3],array[2],str(horaOP))):
							conn.commit()
							conn.close()						
							#print('Gravado no DB \n')
						
						prev = operacoes[0]['user_id']
				else:
					print('aqui')
			
		api.unscribe_live_deal(name,active ,typeOP)
	
	except Exception as e:
		print('Erro', str(e))
		sys.exit()
def loop():
	i = 0
	while True:
		if not main():
			i = i + 1
			print('Mercado Fechado: Tentando outro')
			if i > 10:
				break

				
if(__name__=='__main__'):
	loop()

