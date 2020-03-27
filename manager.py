# aqui existem vários comandos para organização e divulgação de coisas novas
# possibilidade para integrar com nova funções. Ex.: criar lembretes automáticos na seção de tarefas
# as mensagens estão em formato Markdown

import json

with open('config.json') as json_data_file:
		config = json.load(json_data_file)

def tarefas(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['manager']['tarefas'], parse_mode='Markdown')


def aulas(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['manager']['aulas'], parse_mode='Markdown')


def grupos(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['manager']['grupos'], parse_mode='Markdown')


def avisos(update, context):
	chat_id = update.effective_chat.id
	message = ""
	context.bot.send_message(chat_id=chat_id, text=context.bot_data['manager']['avisos'], parse_mode='Markdown')


# edita a mensagem presente em context.bot_data['manager']
def edit(update, context):
	chat_id = update.effective_chat.id

	# checa se o usuário tem permissão para a edição 
	if chat_id not in config['admin_chats']:
		context.bot.send_message(chat_id=chat_id, text=config['messages']['unauthorized'])
		return

	# olha se existe lugar para editar as mensagens no caso de context.bot_data estar incompleto
	if 'manager' not in context.bot_data:
		context.bot_data['manager'] = {}

	try:
		# data = toda a estrutura da mensagem retornada pelo telegram quando o bot é chamado
		# text = texto da mensagem que chamou o bot. Ex.: "/edit avisos\nUm Aviso"
		# value = seção a ser editado
		data = update.message
		text = (data.text.partition(' ')[2]).partition('\n')
		value = text[0]
		text = text[2]

		# checa se a seção é válida
		if value not in ['tarefas', 'aulas', 'grupos', 'avisos']:
			context.bot.send_message(chat_id=chat_id, text=config['messages']['syntax_error'])
			return

		# salva a mensagem no context.bot_data
		context.bot_data['manager'][value] = text

		# avisa para todo usuário do bot que a informação foi atualizada
		for item in context.bot_data['active_ids']:
			context.bot.send_message(chat_id=item, text= "A seção " + value + " foi atualizado !")

		print(">>> " + value + " updated by ", data['from_user']['id'])

	except:
		context.bot.send_message(chat_id=chat_id, text=config['messages']['syntax_error'])
	
