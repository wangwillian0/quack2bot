# aqui existem vários comandos para organização e divulgação de coisas novas

import json

with open('config.json') as json_data_file:
	config = json.load(json_data_file)

def aulas(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['aulas'])


def grupos(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['grupos'])

# edita a mensagem presente em context.bot_data
def edit(update, context):
	chat_id = update.effective_chat.id

	# checa se o usuário tem permissão para a edição 
	if chat_id not in config['admin_chats']:
		context.bot.send_message(chat_id=chat_id, text=config['messages']['unauthorized'])
		return

	try:
		# raw_data = toda a estrutura da mensagem retornada pelo telegram quando o bot é chamado
		# text = texto da parte importante apos o comando
		# key = seção a ser editado
		# value = texto editado
		raw_data = update.message
		text = (raw_data.text.partition(' ')[2]).partition('\n')
		key = text[0]
		value = text[2]

		# checa se a seção é válida
		if key not in ['tarefas', 'aulas', 'grupos', 'avisos']:
			context.bot.send_message(chat_id=chat_id, text=config['messages']['syntax_error'])
			return

		# salva a mensagem no context.bot_data
		context.bot_data[key] = value

		# avisa para todo  do bot que a informação foi atualizada
		context.bot.send_message(chat_id=chat_id, text="A seção /" + key + " foi atualizada")
		print(">>> " + key + " updated by", raw_data['from_user']['id'])
	except:
		context.bot.send_message(chat_id=chat_id, text=config['messages']['syntax_error'])
