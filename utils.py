# ferramentas úteis aqui

from telegram.error import Unauthorized
import json

with open('config.json') as json_data_file:
        config = json.load(json_data_file)


# envia uma mensagem para todos os usuarios ativos
def broadcast(context, message, restriction={}, parse_mode='Markdown'):
	try:
		unauth_ids = []
		
		for chat_id in context.bot_data['active_ids']:
			try:
			    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
			except Unauthorized:
			    unauth_ids.append(chat_id)
			    print("não autorizado por ", chat_id)
			except:
				print("Erro desconhecido (?)")

			for chat_id in unauth_ids:
			    context.bot_data['active_ids'].remove(chat_id)
			    print(chat_id, " stopped!")

		for chat_id in unauth_ids:
			context.bot_data['active_ids'].remove(chat_id)
			print(chat_id, " stopped!")

		print("<<<"+message+">>> foi enviada para todos os usuarios, restriction = "+restriction)
	except:
		print("erro ao tentar transmitir <<<"+message+">>>, restriction = "+restriction)

