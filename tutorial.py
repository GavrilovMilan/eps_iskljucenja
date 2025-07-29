import os
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()