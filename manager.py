# aqui existem vários comandos para organização e divulgação de coisas novas
# as mensagens estão em formato Markdown

import json
import utils
import datetime

with open('config.json') as json_data_file:
		config = json.load(json_data_file)

def CheckTarefas(context):
	try:
		now = datetime.datetime.now().astimezone()
		tz = datetime.timezone(datetime.timedelta(days=-1, seconds=75600), '-03')
		raw_text = context.bot_data['manager']['tarefas']
		raw_text = raw_text.partition('\n')
		d1 = []
		d2 = []
		d3 = []

		while raw_text[0] != '':
			try:
				text = raw_text[0].partition(' ')
				raw_text = raw_text[2].partition('\n')
				tarefa = text[2]
				date = text[0].partition('/')
				deadline = datetime.datetime(2020, int(date[2]), int(date[0]), tzinfo=tz)
				remain = deadline - now
				if remain.days == -1:
					d1.append(tarefa)
				elif remain.days == 0:
					d2.append(tarefa)
				elif remain.days == 1:
					d3.append(tarefa)
			except:
				print("data invalida ou informacao invalida")

		if len(d3) != 0:
			message = "Para daqui a *2* dias !!\n"
			for tarefa in d3:
				message += '-> '+tarefa+'\n'
			utils.broadcast(context, message)
		if len(d2) != 0:
			message = "Para *Amanhã* !!\n"
			for tarefa in d2:
				message += '-> '+tarefa+'\n'
			utils.broadcast(context, message)
		if len(d1) != 0:
			message = "⚠️  Para *Hoje* !!  ⚠️\n"
			for tarefa in d1:
				message += '-> '+tarefa+'\n'
			utils.broadcast(context, message)

	except:
		print("Erro desconhecido com CheckTarefas...\n")


def SortTarefas(context):
	try:
		raw_text = context.bot_data['manager']['tarefas']
		raw_text = raw_text.partition('\n')
		tarefas = []
		while raw_text[0] != '':
			text = raw_text[0].partition(' ')
			raw_text = raw_text[2].partition('\n')
			tarefa = text[2]
			date = text[0].partition('/')
			day = date[0]
			if int(day) < 10 and len(day) != 2:
				day = '0'+day
			month = date[2]
			if int(month) < 10 and len(month) != 2:
				month = '0'+month
			tarefas.append([month, day, tarefa])

		tarefas.sort()
		
		raw_text = ''
		for tarefa in tarefas:
			if tarefa[2][len(tarefa[2])-1] != '.':
				tarefa[2] += '.'
			raw_text += tarefa[1]+'/'+tarefa[0]+' '+tarefa[2]+'\n'

		context.bot_data['manager']['tarefas'] = raw_text
	except:
		print("Erro desconhecido com SortTarefas...\n")


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
		context.bot_data['manager'][key] = value

		if key == 'tarefas':
			SortTarefas(context)

		# avisa para todo usuário do bot que a informação foi atualizada
		utils.broadcast(context, "A seção /" + key + " foi atualizado !")
		print(">>> " + key + " updated by ", raw_data['from_user']['id'])

	except:
		context.bot.send_message(chat_id=chat_id, text=config['messages']['syntax_error'])
	
