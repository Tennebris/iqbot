import sys

class iq:
	def getRank(api):
		ranking = api.get_leader_board('Worldwide',1,1000,0)
		dic = {}
		topUserId = []
		rank = []

		for i in ranking['result']['positional']:
			id = ranking['result']['positional'][i]['user_id']
			topUserId.append(id)
			rank.append(i)
		dic['userID'] = topUserId
		dic['rank'] = rank
		return dic

	def operar(api,valor,ativo,direct):
		try:
			status,opId = api.buy(valor,ativo,direct,1)
			if status:
				lucro = api.check_win_v3(opId)
				saida = ("Win" if lucro > 0 else "Loss")
				#print('ok')
				return (True,('Resultado: ',str(lucro),' ',saida))
			else:
				#print('not ok')
				return ((False),opId)
		except Exception as e:
			print(str(e))

