import asyncio
from requests_html import AsyncHTMLSession
from dataclasses import dataclass
from typing import List
from datetime import datetime
from pymongo import MongoClient
import feedparser
from telegram import Bot, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes

@dataclass
class Movie:
    name: str
    release_datetime: datetime
    poster_url: str
    screenshots: List[str]
    torrents: List['Torrent']

    def __str__(self):
        return f"Movie: {self.name} (Released on: {self.release_datetime})"

@dataclass
class Torrent:
    file_name: str
    torrent_link: str
    magnet_link: str

    def __str__(self):
        return f"Torrent File: {self.file_name}"

async def scrape_from_url(url: str) -> Movie:
    session = AsyncHTMLSession()
    response = await session.get(url)
    await response.html.arender()
    page = response.html

    name = page.find("h3")[0].text
    release_datetime_str = page.find("time")[0].attrs["datetime"]
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    release_datetime = datetime.strptime(release_datetime_str, date_format)
    img_tags = page.find("img.ipsImage")
    pics = [img.attrs["src"] for img in img_tags if img.attrs["src"].lower().split(".")[-1] in ("jpg", "jpeg", "png")]
    poster_url = pics[0] if pics else ""
    screenshots = pics[1:]
    magnet_links = [a.attrs["href"] for a in page.find("a.skyblue-button")]
    torrent_links = [a.attrs["href"] for a in page.find("a[data-fileext='torrent']")]
    file_names = [span.text.strip() for span in page.find('span[style="color:#0000ff;"]')]

    torrents = [Torrent(file_name, torrent_link, magnet_link) for file_name, torrent_link, magnet_link in zip(file_names, torrent_links, magnet_links)]
    movie = Movie(name, release_datetime, poster_url, screenshots, torrents)
    return movie

MONGODB_CONNECTION_STRING = "mongodb+srv://sankar:sankar@sankar.lldcdsx.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "movie_links_db"
COLLECTION_NAME = "movie_links"

def initialize_database():
    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client[DATABASE_NAME]
    db[COLLECTION_NAME].create_index("link", unique=True)
    client.close()

def load_previous_movie_links():
    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client[DATABASE_NAME]
    previous_links = {doc["link"] for doc in db[COLLECTION_NAME].find()}
    client.close()
    return previous_links

def save_movie_link(link):
    client = MongoClient(MONGODB_CONNECTION_STRING)
    db = client[DATABASE_NAME]
    db[COLLECTION_NAME].insert_one({"link": link})
    client.close()

async def process_new_movie_data(movie_data: Movie, bot_token: str, chat_id: str):
    bot = Bot(token=bot_token)
    message = f"*New Movie Release*\n\n{movie_data}\n\n[View Details]({movie_data.poster_url})"
    await bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "Hello👋\n\n"
        "🗳Get latest Movies from 1Tamilmv\n\n"
        "⚙️*How to use me??*🤔\n\n"
        "✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\n"
        "Share and Support💝"
    )
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

async def view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Fetching latest movies...")

async def main():
    rss_url = "https://rss.app/feeds/yddXEDeHj3XYhNNN.xml"
    telegram_bot_token = "6769849216:AAGPVUHLAzt7p9pFldV03v2YYGjyE0sEZHQ"
    telegram_channel_id = "-1001571491517"

    initialize_database()
    previous_movie_links = load_previous_movie_links()

    application = Application.builder().token(telegram_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("view", view))

    async with application:
        await application.initialize()
        await application.start()

        while True:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries:
                movie_url = entry.link

                if movie_url not in previous_movie_links:
                    movie_data = await scrape_from_url(movie_url)
                    await process_new_movie_data(movie_data, telegram_bot_token, telegram_channel_id)
                    save_movie_link(movie_url)
                    previous_movie_links.add(movie_url)

            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
