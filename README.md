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

O arquivo `token.pickle` e as labels do filtro usado pelo bot podem ser obtidas seguindo as instruções e alterando um pouco o script `quickstart.py` encontradas na documentação da própria google:

https://developers.google.com/gmail/api/quickstart/python

Para facilitar o processo você pode executar o código `listlabels.py` em vez do script da documentação da google.

Por fim, o token da api do telegram é obtida na hora da criação do bot com o @BotFather no telegram
