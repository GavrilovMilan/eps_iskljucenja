import json
import os
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(commands=['iskljucenja'])
def iskljucenja(message):
    with open('iskljucenja.json', 'r', encoding='utf-8') as f:
        iskljucenja = json.load(f)
    # res = ''
    # for i in iskljucenja:
    #     res = res + f'{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}' + '\n'
    # bot.reply_to(message, res)
    bot.reply_to(message, 'Današnja najavljena isključenja za ogranak: Novi Sad')
    for i in iskljucenja:
        bot.reply_to(message, f'{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}')
    # bot.reply_to(message, message.text[13:])

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()