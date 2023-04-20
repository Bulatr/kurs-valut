'''
Основной модуль
'''
import telebot
import requests

TOKEN = "6084243976:AAH15Er4IvKQR17isVotjka8692lq8J5Fu8"
bot = telebot.TeleBot(TOKEN) # Вот мозги мне проело, нужно писать TeleBot а не Telebot

'''
ApiLayer
'''
TOKEN_API_LAYER = "dZ67KxZN8n2l6mtStwa5f0vXqqq5joIm"
payload = {}
url = "https://api.apilayer.com/fixer/convert?to=RUB&from=USD&amount=1"

payload = {}
headers= {
  "apikey": "dZ67KxZN8n2l6mtStwa5f0vXqqq5joIm"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text

'''
Обработка комманд старт и помощь
'''
@bot.message_handler(commands=["start","help"])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в следующем формате:\n <имя валюты>\
<в какую валюту перевести> <количество переводимой валюты>\n \
например:\n \
рубль доллар 1"
    bot.reply_to(message, text)

bot.polling(none_stop=True)
