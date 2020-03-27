import json

with open('config.json') as json_data_file:
		config = json.load(json_data_file)


def start(update, context):
	chat_id = update.effective_chat.id

	if 'active_ids' not in context.bot_data:
		context.bot_data['active_ids'] = []

	if chat_id in context.bot_data['active_ids']:
		return

	context.bot_data['active_ids'].append(chat_id)

	context.bot.send_message(chat_id=chat_id, text=config['messages']['essentials']['start'])
	print(chat_id, " started!")

def stop(update, context):
	chat_id = update.effective_chat.id

	if 'active_ids' not in context.bot_data:
		context.bot_data['active_ids'] = []

	context.bot_data['active_ids'].remove(chat_id)

	context.bot.send_message(chat_id=chat_id, text=config['messages']['essentials']['stop'])
	print(chat_id, " stopped!")


def help_(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=config['messages']['essentials']['help'], parse_mode='Markdown')


def quack(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id=chat_id, text=config['messages']['essentials']['quack'])