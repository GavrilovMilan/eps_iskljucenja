import datetime
import json
import os
import telebot
from dotenv import load_dotenv

import scraping
from metode import *


def log_user_message(handler):
    def wrapper(message):
        print(f"Under development! UserID:{message.from_user.id}, {message.from_user.last_name} {message.from_user.first_name}: '{message.text}'")
        return handler(message)
    return wrapper


with open('iskljucenja.json', 'r', encoding='utf-8') as f:
    datum = json.load(f)
    dt = formatiraj_datum(datetime.date.today())
    # dt = f"{dt.day}.{'{:02d}'.format(dt.month)}.{dt.year}."
    if datum[0]['datum'] != dt:
        scraping.scrape()


load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['iskljucenja'])
@log_user_message
def iskljucenja(message):
    with open('iskljucenja.json', 'r', encoding='utf-8') as f:
        iskljucenja = json.load(f)

    if len(message.text) > 13:
        # Spaja više isključenja u jednu poruku (može nastati problem ukoliko je poruka duža od 4096 karaktera)
        res = ''
        # print(message.text[13:])
        polja_za_pretragu = ['ulice', 'opstina']
        for i in iskljucenja:
            if any(message.text[13:].upper() in cir_to_lat_osisano(i[p]).upper() for p in polja_za_pretragu):
                res = res + f"{i['datum']} {i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}" + '\n'
        if res != '':
            bot.reply_to(message, res)
        else:
            bot.reply_to(message, 'Nema najavljenih isključenja struje za zadati filter')
    else:
        bot.reply_to(message, f"Sva najavljena isključenja za današnji dan")
        # Svako isključenje je jedna poruka
        for i in iskljucenja:
            bot.reply_to(message, f"{i['datum']} {i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}")

        # bot.reply_to(message, message.text[13:])

@bot.message_handler(func=lambda msg: True)
@log_user_message
def echo(message):
    bot.reply_to(message, 'Nepoznata komanda.')


bot.infinity_polling()