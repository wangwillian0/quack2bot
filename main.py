# No context.bot_data existe um dicionário (?) que pode armazenar informações do bot como um todo,
# é nesta estrutura que está todas as informações "editáveis" por usuários,
# não sei se é possível fazer algo melhor mas isso já dá conta de não apagar as informações depois
# que o bot é desligado

# config.json = arquivo de configurações
# botdb_file serve para salvar os dados de context.bot_data 


from telegram.ext import Updater, CommandHandler, DictPersistence
import datetime
import json
import manager
import getmail


with open('config.json') as json_data_file:
		config = json.load(json_data_file)
with open(config['botdb_file']) as json_data_file:
	botdb = json_data_file.read()


def autosave(context):
	with open(config['botdb_file'], 'w') as json_data_file:
		json.dump(context.bot_data, json_data_file, indent=2)
	# print("Autosaved !")

def start(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=config['messages']['start'])
        print(chat_id, "started !")
def help_(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=config['messages']['help'])
def quack(update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=config['messages']['quack'])



def main():
	# isso serve pra fazer a ligação com o telegram (?)
	upd = Updater(config['api_token'], use_context=True, persistence=DictPersistence(bot_data_json = botdb))

	# coloca as funções GetNewEmails e autosave para rodarem periodicamente
	# tz = timezone
	tz = datetime.timezone(datetime.timedelta(days=-1, seconds=75600), '-03')
	upd.job_queue.run_repeating(getmail.GetNewEmails, interval=config['email_delay'], first=0)
	upd.job_queue.run_repeating(autosave, interval=config['autosave_interval'], first=0)
	
	# coloca os comandos seguintes disponíveis para o usuario
	upd.dispatcher.add_handler(CommandHandler('start', start))
	upd.dispatcher.add_handler(CommandHandler('help', help_))
	upd.dispatcher.add_handler(CommandHandler('quack', quack))
	upd.dispatcher.add_handler(CommandHandler('aulas', manager.aulas))
	upd.dispatcher.add_handler(CommandHandler('grupos', manager.grupos))
	upd.dispatcher.add_handler(CommandHandler('edit', manager.edit))

	# deixa rodando as coisas (??)
	upd.start_polling()
	upd.idle()

# (??)
if __name__ == '__main__':
    main()
