import asyncio
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'

bot = telebot.TeleBot(TOKEN)

button1 = types.InlineKeyboardButton(text="⚡ Powered by", url='https://t.me/heyboy2004')
button2 = types.InlineKeyboardButton(text="🔗 Gdrive channel", url='https://t.me/GdtotLinkz')
button3 = types.InlineKeyboardButton(text="📜 Status channel", url='https://t.me/TmvStatus')
keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('👨‍💻 Developed by', url='https://github.com/shinas101')).add(button1).add(button2).add(button3)
keyboard2 = types.InlineKeyboardMarkup().add(button2).add(button3)

@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(chat_id=message.chat.id,
                     text=f"Hello! 👋\n\n🗳 Get latest Movies from 1Tamilmv\n\n⚙️ *How to use me?* 🤔\n\n"
                          f"✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\n"
                          f"Share and Support! 💝",
                     parse_mode='Markdown',
                     reply_markup=keyboard)

@bot.message_handler(commands=['view'])
def start(message):
    bot.send_message(message.chat.id, text="*Please wait for 10 seconds*", parse_mode='Markdown')
    asyncio.create_task(fetch_and_send_movies(message.chat.id))

async def fetch_and_send_movies(chat_id):
    try:
        movie_list, real_dict = await tamilmv()
        markup = makeKeyboard(movie_list)
        await bot.send_message(chat_id=chat_id,
                               text="Select a Movie from the list 🙂 : ",
                               reply_markup=markup,
                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text=f"Error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    asyncio.create_task(send_movie_links(call.message.chat.id, call.data))

async def send_movie_links(chat_id, movie_key):
    try:
        await bot.send_message(chat_id=chat_id, text="Here's your Movie links 🎥 ", parse_mode='markdown')
        for link in real_dict[movie_key]:
            await bot.send_message(chat_id=chat_id, text=link, parse_mode='markdown')
        await bot.send_message(chat_id=chat_id,
                               text=f"🌐 Please Join Our Status Channel",
                               parse_mode='markdown',
                               reply_markup=keyboard2)
    except KeyError:
        await bot.send_message(chat_id=chat_id, text="Movie not found.")

def makeKeyboard(movie_list):
    markup = types.InlineKeyboardMarkup()
    for key, value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value, callback_data=f"{key}"))
    return markup

async def tamilmv():
    mainUrl = 'https://www.1TamilMV.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection': 'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    movie_dict = {}
    real_dict = {}
    movie_list = []

    web = requests.get(mainUrl, headers=headers)
    soup = BeautifulSoup(web.text, 'html.parser')
    
    num = 0
    temps = soup.find_all('div', {'class': 'ipsType_break ipsContained'})

    for i in range(21):
        title = temps[i].find_all('a')[0].text.strip()
        movie_dict[title] = None
        movie_list.append(title)
        links = temps[i].find('a')['href']
        content = str(links)
        html = requests.get(content)
        soup = BeautifulSoup(html.text, 'html.parser')
        alltitles = []
        for i in soup.find_all('a', {'data-fileext': 'torrent', 'href': True}):
            alltitles.append(i['href'])
        real_dict[title] = alltitles

    return movie_list, real_dict

def main():
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        print("Bot stopped.")
    finally:
        print("Closing bot...")
        bot.stop_polling()
        bot.polling(none_stop=False)
        bot.polling()
        
if __name__ == '__main__':
    main()
