import json
import os
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


def lat_to_cir(tekst):
    mapa = {
        'nj': 'њ', 'dž': 'џ', 'lj': 'љ',
        'NJ': 'Њ', 'DŽ': 'Џ', 'LJ': 'Љ',
        'Nj': 'Њ', 'Dž': 'Џ', 'Lj': 'Љ',
        'nJ': 'Њ', 'dŽ': 'Џ', 'lJ': 'Љ',
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'đ': 'ђ',
        'e': 'е', 'ž': 'ж', 'z': 'з', 'i': 'и', 'j': 'ј', 'k': 'к',
        'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р',
        's': 'с', 't': 'т', 'ć': 'ћ', 'u': 'у', 'f': 'ф', 'h': 'х',
        'c': 'ц', 'č': 'ч', 'š': 'ш',
        'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'Đ': 'Ђ',
        'E': 'Е', 'Ž': 'Ж', 'Z': 'З', 'I': 'И', 'J': 'Ј', 'K': 'К',
        'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р',
        'S': 'С', 'T': 'Т', 'Ć': 'Ћ', 'U': 'У', 'F': 'Ф', 'H': 'Х',
        'C': 'Ц', 'Č': 'Ч', 'Š': 'Ш'
    }

    for lat, cir in [('nj', 'њ'), ('dž', 'џ'), ('lj', 'љ'),
                     ('NJ', 'Њ'), ('DŽ', 'Џ'), ('LJ', 'Љ'),
                     ('Nj', 'Њ'), ('Dž', 'Џ'), ('Lj', 'Љ'),
                     ('nJ', 'Њ'), ('dŽ', 'Џ'), ('lJ', 'Љ')]:
        tekst = tekst.replace(lat,cir)

    return ''.join(mapa.get(c,c) for c in tekst)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(commands=['iskljucenja'])
def iskljucenja(message):
    with open('iskljucenja/iskljucenja.json', 'r', encoding='utf-8') as f:
        iskljucenja = json.load(f)

    if len(message.text) > 13:
        # Spaja više isključenja u jednu poruku (može nastati problem ukoliko je poruka duža od 4096 karaktera)
        res = ''
        print(message.text[13:])
        for i in iskljucenja:
            if lat_to_cir(message.text[13:]).upper() in i['ulice'].upper():
                res = res + f"{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}" + '\n'
        if res != '':
            bot.reply_to(message, res)
        else:
            bot.reply_to(message, 'Nema najavljenih isključenja struje za zadati filter')
    else:
        bot.reply_to(message, f"Sva najavljena isključenja za današnji dan")
        # Svako isključenje je jedna poruka
        for i in iskljucenja:
            bot.reply_to(message, f"{i['opstina']}: {i['vreme_od']} - {i['vreme_do']} | {i['ulice']}")

        # bot.reply_to(message, message.text[13:])

@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()