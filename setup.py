from asyncio import events
import telebot
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import re
from bs4 import BeautifulSoup
import asyncio

TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'

bot = telebot.TeleBot(TOKEN)

button1 = telebot.types.InlineKeyboardButton(text="⚡Powered by", url='https://t.me/heyboy2004')
button2 = telebot.types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = telebot.types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = telebot.types.InlineKeyboardMarkup().add(
    telebot.types.InlineKeyboardButton('👨‍💻 Developed by', url='github.com/shinas101')
).add(button1).add(button2).add(button3)
keyboard2 = telebot.types.InlineKeyboardMarkup().add(button2).add(button3)

@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\nShare and Support💝",
        parse_mode='Markdown',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    tamilmv()
    bot.send_message(
        chat_id=message.chat.id,
        text="Select a Movie from the list 🙂 : ",
        reply_markup=makeKeyboard(),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id, text=f"Here's your Movie links 🎥", parse_mode='markdown')
    if call.data.isdigit() and int(call.data) < len(movie_list):
        movie_name = movie_list[int(call.data)]
        if movie_name in real_dict:
            for i in real_dict[movie_name]:
                bot.send_message(call.message.chat.id, text=f"{i}\n\n🤖 @Tamilmv\_movie\_bot", parse_mode='markdown')
        else:
            bot.send_message(call.message.chat.id, text="No links available for the selected movie.", parse_mode='markdown')
    bot.send_message(call.message.chat.id, text=f"🌐 Please Join Our Status Channel", parse_mode='markdown', reply_markup=keyboard2)

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

def tamilmv():
    mainUrl = 'https://www.1tamilmv.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    global movie_dict, real_dict, movie_list
    movie_dict = {}
    real_dict = {}
    movie_list = []

    web = requests.request("GET", mainUrl, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    linker = []
    badtitles = []

    for i in range(min(21, len(temps))):
        title = temps[i].findAll('a')[0].text.strip()
        badtitles.append(title)
        links = temps[i].find('a')['href']
        linker.append(links)

    movie_list = badtitles[:]
    num = 0

    for url in linker:
        html = requests.request("GET", url)
        soup = BeautifulSoup(html.text, 'lxml')
        mag = [i['href'] for i in soup.find_all('a', href=True) if i['href'].startswith('magnet')]
        filelink = [a['href'] for a in soup.findAll('a', {"data-fileext": "torrent"}, href=True)]
        alltitles = [title.find('span').text.strip() for title in soup.find_all('a') if title.find('span') and title.find('span').text.endswith('torrent')]

        for p in range(len(mag)):
            try:
                real_dict.setdefault(movie_list[num], [])
                formatted_title = alltitles[p] if p < len(alltitles) else "Unknown Title"
                formatted_filelink = filelink[p] if p < len(filelink) else "#"
                real_dict[movie_list[num]].append(
                    f"*{formatted_title}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({formatted_filelink})"
                )
            except IndexError as e:
                print(f"IndexError: {e}")
            except Exception as e:
                print(f"Error: {e}")

        num += 1

def main():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    main()
    
