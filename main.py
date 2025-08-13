import logging
import telebot
from dotenv import load_dotenv

import scraping
from metode import *


PERIOD_OSVEZAVANJA = 1 # Izražen u satima


potrebni_dir_dok()


logger = logging.getLogger(__name__)
datum = datetime.today().strftime('%Y_%m_%d')
logging.basicConfig(filename=f'logovi/{datum}.log', level=logging.INFO, encoding='utf-8',
                            format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d.%m.%Y. %H:%M:%S')


def log_user_message(handler):
    def wrapper(message):
        datum = datetime.today().strftime('%Y_%m_%d')
        logging.basicConfig(filename=f'logovi/{datum}.log', level=logging.INFO, encoding='utf-8',
                            format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%d.%m.%Y. %H:%M:%S')
        logger.info(f"UserID:{message.from_user.id}, {message.from_user.last_name} {message.from_user.first_name}: '{message.text}'")
        return handler(message)
    return wrapper


if os.path.exists('podaci/iskljucenja.json'):
    with open('podaci/iskljucenja.json', 'r', encoding='utf-8') as f:
        datum = json.load(f)[0]['datum_i_vreme_provere']
        dt = datetime.now().strftime('%d.%m.%Y. %H:%M:%S')
        if uporedi_datume(datum, dt).total_seconds() >= PERIOD_OSVEZAVANJA * 3600:
            scraping.scrape()
            logger.info('Osvežio podatke')
else:
    scraping.scrape()
    logger.info('Nije postojao dokument iskljucenja.json, osveženi podaci')


load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['iskljucenja'])
@log_user_message
def iskljucenja(message):
    chat_id = message.chat.id
    if not check_korisnik(chat_id):
        print('Korisnik ne postoji, dodajem novog korisnika')
        add_korisnik(message.json['from'])

    with open('podaci/iskljucenja.json', 'r', encoding='utf-8') as f:
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


@bot.message_handler(commands=['dodaj'])
@log_user_message
def dodaj(message):
    print('TODO')


@bot.message_handler(func=lambda msg: True)
@log_user_message
def echo(message):
    if '/' not in message.text[0]:
        message.text = '/iskljucenja ' + message.text
        logger.info('Dodao /iskljucenja na početak poruke')
        iskljucenja(message)
    else:
        bot.reply_to(message, 'Nepoznata komanda.')

print('Bot startovan')

bot.infinity_polling()