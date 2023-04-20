import telebot

TOKEN = "6084243976:AAH15Er4IvKQR17isVotjka8692lq8J5Fu8"
bot = telebot.Telebot(TOKEN)

@bot.message_handler(commands=["start","help"])
def start_help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду в следующем формате:\n <имя валюты>\
<в какую валюту перевести> <количество переводимой валюты>\n \
например:\n \
рубль доллар 1"
    bot.reply_to(message, text)
