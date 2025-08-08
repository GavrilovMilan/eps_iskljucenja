import json
import logging
import os
import telebot
from dotenv import load_dotenv
from datetime import datetime

import scraping
from metode import *


PERIOD_OSVEZAVANJA = 1 # Izražen u satima


if not os.path.isdir('logs'):
    os.mkdir('logs')
logger = logging.getLogger(__name__)
datum = datetime.today().strftime('%Y_%m_%d')
def log_user_message(handler):
    def wrapper(message):
        datum = datetime.today().strftime('%Y_%m_%d')
        logging.basicConfig(filename=f'logs/{datum}.log', level=logging.INFO, encoding='utf-8',
                            format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d.%m.%Y. %H:%M:%S')
        logger.info(f"UserID:{message.from_user.id}, {message.from_user.last_name} {message.from_user.first_name}: '{message.text}'")
        return handler(message)
    return wrapper


with open('iskljucenja.json', 'r', encoding='utf-8') as f:
    datum = json.load(f)[0]['datum_i_vreme_provere']
    dt = datetime.now().strftime('%d.%m.%Y. %H:%M:%S')
    if uporedi_datume(datum, dt).total_seconds() >= PERIOD_OSVEZAVANJA * 3600:
        scraping.scrape()
        logger.info('Osvežio podatke')


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
        polja_za_pretragu = ['ulice', 'opstina']
        for i in iskljucenja[1:]:
            if any(message.text[13:].upper() in cir_to_lat_osisano(i[p]).upper() for p in polja_za_pretragu):
                res = res + f"{i['datum']} {i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}" + '\n'
        if res != '':
            bot.reply_to(message, res)
        else:
            bot.reply_to(message, 'Nema najavljenih isključenja struje za zadati filter')
    else:
        bot.reply_to(message, f"Unesite mesto ili ulicu za koju želite da proverite najavljena isključenja.")


@bot.message_handler(func=lambda msg: True)
@log_user_message
def echo(message):
    if '/' not in message.text[0]:
        message.text = '/iskljucenja ' + message.text
        logger.info('Dodao /iskljucenja na početak poruke')
        iskljucenja(message)
    else:
        bot.reply_to(message, 'Nepoznata komanda.')


logger.info('Bot startovan')
print(1)

bot.infinity_polling()