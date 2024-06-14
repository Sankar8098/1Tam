import asyncio
import httpx
from bs4 import BeautifulSoup
import re
import telebot
from telebot import types

TOKEN = '6769849216:AAGxT73eYO9wmrlqZlZ73DmyN3Ls3CvH6dg'
bot = telebot.TeleBot(TOKEN)

# Function to fetch movie data asynchronously
async def tamilmv():
    mainUrl = 'https://www.1TamilMV.eu/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection':'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(mainUrl, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            linker = [link['href'] for link in soup.select('div.ipsType_break a')]
            movie_data = await asyncio.gather(*[scrape_movie_data(client, link) for link in linker[:21]])
            return movie_data
        except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
            print(f"Error fetching movie data: {e}")
            return []

async def scrape_movie_data(client, url):
    try:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        mag_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('magnet')]
        torrent_links = [a['href'] for a in soup.find_all('a', {'data-fileext': 'torrent'}, href=True)]
        movie_title = soup.find('title').text.strip()
        return {
            'title': movie_title,
            'magnet_links': mag_links,
            'torrent_links': torrent_links
        }
    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        print(f"Error scraping {url}: {e}")
        return None

# Example usage of asyncio in bot command
@bot.message_handler(commands=['view'])
async def start(message):
    await bot.send_message(message.chat.id, "Please wait for 10 seconds...")
    movie_data = await tamilmv()
    if movie_data:
        keyboard = types.InlineKeyboardMarkup()
        for idx, movie in enumerate(movie_data):
            keyboard.add(types.InlineKeyboardButton(text=movie['title'], callback_data=str(idx)))
        await bot.send_message(message.chat.id, "Select a Movie from the list:", reply_markup=keyboard)
    else:
        await bot.send_message(message.chat.id, "Failed to fetch movie data. Please try again later.")

# Callback query handling
@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    try:
        movie_idx = int(call.data)
        movie = movie_data[movie_idx]
        response_text = f"Here's your Movie links for {movie['title']}:\n\n"
        for magnet_link in movie['magnet_links']:
            response_text += f"Magnet Link: {magnet_link}\n"
        response_text += f"\n🤖 @Tamilmv_movie_bot"
        await bot.send_message(call.message.chat.id, response_text, parse_mode='markdown')
    except IndexError:
        await bot.send_message(call.message.chat.id, "Invalid selection. Please select a valid movie.")

# Main function to start the bot
def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
    
