'''
Основной модуль
'''
import json
import requests
import telebot



TOKEN = "6084243976:AAH15Er4IvKQR17isVotjka8692lq8J5Fu8"
bot = telebot.TeleBot(TOKEN) # Вот мозги мне проело, нужно писать TeleBot а не Telebot

keys = {
    "рубль": "RUB",
    "доллар": "USD",
    "евро": "EUR",
    "юань": "CNY"
}


# ApiLayer
# Функция которая отправляет и получает данные с апи

def fixer(fixer_to: str, fixer_from: str, amount: float):

    TOKEN_API_LAYER = "dZ67KxZN8n2l6mtStwa5f0vXqqq5joIm"

    payload = {}
    url = f"https://api.apilayer.com/fixer/convert?to={fixer_to}&from={fixer_from}&amount={amount}"

    headers= {
        "apikey": TOKEN_API_LAYER
    }

    response = requests.get(url, headers=headers, data = payload)

    status_code = response.status_code
    if status_code == 200:
        result = response.json()
        return result["result"]

# fixer("RUB", "USD", 1)

# Обработка комманд старт и помощь

@bot.message_handler(commands=["start","help"])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в следующем формате:\n <имя валюты>\
<в какую валюту перевести> <количество переводимой валюты>\n \
например:\n \
рубль доллар 1\n \
Получить список доступных валют: /values"
    bot.reply_to(message, text)


# Список валют

@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message,):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


# Обработка сообщений
@bot.message_handler(content_types=["text"])
def convert_text(message: telebot.types.Message,):
    fixer_to, fixer_from, amount = message.text.split(" ")
    print(keys[fixer_to], keys[fixer_from], float(amount))
    result = fixer(keys[fixer_to], keys[fixer_from], float(amount))
    text = f"Цена {amount} {fixer_to} в {fixer_from}: {result}"
    bot.reply_to(message, text)


bot.polling(none_stop=True)
