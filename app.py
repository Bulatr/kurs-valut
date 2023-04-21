'''
Основной модуль
'''
import telebot
from config import TOKEN, keys
from extensions import APIException, ConvertedValute

bot = telebot.TeleBot(TOKEN) # Вот мозги мне проело, нужно писать TeleBot а не Telebot

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
    try:
        values = message.text.split(" ")
        ConvertedValute.count_values(values)
        base, quote, amount = values
        result = ConvertedValute.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду \n{e}")
    else:
        text = f"Цена {amount} {base} в {quote}: {result} {quote}"
        bot.reply_to(message, text)


bot.polling(none_stop=True)
