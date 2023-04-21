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

# Исключения
class ConvertException(Exception):
    pass

# ApiLayer
# Функция которая отправляет и получает данные с апи
class ConvertedValute:
    @staticmethod
    def fixer(fixer_to: str, fixer_from: str, amount: float)-> float:

        TOKEN_API_LAYER = "dZ67KxZN8n2l6mtStwa5f0vXqqq5joIm"
        try:
            amount = float(amount)
        except ValueError:
            bot.reply_to(message, "Не удалось обработать количество")
            raise ConvertException(f"Не удалось обработать количество {amount}")

        try:
            key_fixer_to = keys[fixer_to]
        except KeyError:
            raise ConvertException(f"Не удалось обработать валюту {fixer_to}")

        try:
            key_fixer_from = keys[fixer_from]
        except KeyError:
            raise ConvertException(f"Не удалось обработать валюту {fixer_from}")

        if key_fixer_to ==  key_fixer_from:
            bot.reply_to(message, "Одинаковые параметры")
            raise ConvertException("Одинаковые параметры")

        if amount == 0 :
            bot.reply_to(message, "Количество равно 0")
            raise ConvertException("Количество равно 0")

        if amount < 0 :
            bot.reply_to(message, "Количество меньше 0")
            raise ConvertException("Количество меньше 0")

        payload = {}
        url = f"https://api.apilayer.com/fixer/convert?to={key_fixer_to}&from={key_fixer_from}&amount={amount}"

        headers= {
            "apikey": TOKEN_API_LAYER
        }

        response = requests.get(url, headers=headers, data = payload)

        status_code = response.status_code
        if status_code == 200:
            result = response.json()
            return result["result"]
        else :
            return False
    
    @staticmethod
    def count_values( message: telebot.types.Message ,values: list)-> None:
        if len(values) > 3:
            bot.reply_to(message, "Слишком много параметров")
            raise ConvertException("Слишком много параметров")

        if len(values) < 3:
            bot.reply_to(message, "Слишком мало параметров")
            raise ConvertException("Слишком мало параметров")

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
    values = message.text.split(" ")
    ConvertedValute.count_values(message, values)
    fixer_to, fixer_from, amount = values
    result = ConvertedValute.fixer(fixer_from, fixer_to, amount)
    text = f"Цена {amount} {fixer_to} в {fixer_from}: {result} {fixer_from}"
    bot.reply_to(message, text)


bot.polling(none_stop=True)
