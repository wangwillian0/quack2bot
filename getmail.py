from googleapiclient.discovery import build
import base64
import pickle
import json

with open('config.json') as json_data_file:
        config = json.load(json_data_file)

# carrega as credenciais da API
creds = pickle.load( open(config['gmail_creds'], 'rb') )
service = build('gmail', 'v1', credentials=creds)


# retorna a lista de IDs dos emails com todas labels colocadas em label_ids 
def ListMessageIds(label_ids):
    response = service.users().messages().list(userId='me', labelIds=label_ids, maxResults=20).execute()

    msg_ids = []

    if(response['resultSizeEstimate'] == 0):
    	return msg_ids

    for message in response['messages']:
        msg_ids.append(message['id'])

    return msg_ids


# Extrai e formata o texto do email de uma forma estranha
# A seguinte formatação foi feita exclusivamente para funcionar com os emails do fórum E-disciplinas
def GetMessage(msg_id, part = 0):
    message = service.users().messages().get(userId='me', id=msg_id).execute() 
    try:
        content = message['payload']['parts'][part]['body']['data']
        result = base64.urlsafe_b64decode(content).decode('utf-8')
        
        pattern = '---------------------------------------------------------------------'
        aux = result.split(pattern)
        result = aux[0][0:2] + '#' + aux[0][2:9] + ' ' + aux[0][9:] + pattern + aux[1] + pattern
    except:
        print("email possivelmente mal formatado (?)")
        return

    return result


# Marca o email como lido fazendo alterações nos labels ligadas ao id do email
def MarcAsRead(msg_id):
	changes = {
		'removeLabelIds': ['UNREAD'],
		'addLabelIds': []
	}
	service.users().messages().modify(userId='me', id=msg_id, body=changes).execute()


def broadcast(context, message, chat_list):
    try:
        for chat_id in chat_list:
            try:
                context.bot.send_message(chat_id=chat_id, text=message)
            except Exception as ex:
                print("[Erro]: ", ex)
                for admin_id in config['admin_chats']:
                    context.bot.send_message(chat_id=admin_id, text="[admin]: Erro ao tentar transmitir uma messagem")
            print("<<<"+message+">>> foi enviada para todos os usuarios, restriction = ")
    except:
        print("erro ao tentar transmitir <<<"+message+">>> !!, restriction = ", restriction)



# A função que de fato é chamada pelo bot
def GetNewEmails(context):
    # tenta extrair a lista de ids dos emails
    # o reverse é para manter a ordem temporal correta dos emails
    for label in config['email_labels'].keys():
        try:
            msg_list = ListMessageIds([label, 'UNREAD'])
            msg_list.reverse()
            # print(msg_list, label)
        except:
            print("Erro em getmail.ListMessageIds()...")
            continue
        
        for msg_id in msg_list:
            MarcAsRead(msg_id)
            try:
                message = GetMessage(msg_id)
                if message == None:
                    continue
                chat_list = list(set(config['email_labels'][label]+config['admin_chats']))
                broadcast(context, message, chat_list)
            except:
                print("Erro no envio de um email")
