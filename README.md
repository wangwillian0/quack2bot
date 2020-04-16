# quack2bot
Quack quack

## O que o bot faz ?

- Encaminhar emails contendo novos posts no fórum do E-disciplinas 
- Avisar sobre tarefas na véspera das datas de entrega
- Quack quack

## Dependências

É necessário a biblioteca da API do gmail e a API python-telegram-bot.

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
```
pip install python-telegram-bot
```

## Configurando

Para que o bot consiga selecionar corretamente os email sobre posts no fórum, é preciso criar um novo filtro no gmail, usando informações como o endereço de email do remetente e palavras chaves como _"fóruns"_ e palavras que não devem aparecer como _"mensagem que foi enviada para você em 'e-Disciplinas'"_, que normalmente caracteriza um email contendo uma nova mensagem pessoal recebida no fórum.

O arquivo `token.pickle` e as labels do filtro usado pelo bot podem ser obtidas usando o script `quickstart.py` encontrado na documentação da própria google:

https://developers.google.com/gmail/api/quickstart/python

Por causa da necessidade de fazer alterações nas labels, removendo a label de UNREAD dos emails já encaminhados, será necessário uma permissão um pouco acima do que somente a leitura dos emails. Para isso encontre o seguinte campo do código:
```
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
```

E altere para:
```
SCOPES = ['https://www.googleapis.com/auth/gmail.modify'']
```

Após a identificação da label associada ao filtro, os campos associados ao label no código do bot devem ser alteradas para a nova label e o arquivo `token.pickle` deve ser copiada para o mesmo diretório que o resto do bot.

O token da api do telegram é obtida na hora da criação do bot com o @BotFather no telegram
