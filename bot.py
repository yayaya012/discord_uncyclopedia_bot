from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import pytz  
import random
from bs4 import BeautifulSoup
import requests

# BeautifulSoupで秀逸な記事の欄からランダムに渡す

# タイムゾーン設定（日本標準時）
JST = pytz.timezone('Asia/Tokyo')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="$",
    case_insensitive=True,
    intents=intents
)

def createUrl():
    res = requests.get('https://ansaikuropedia.org/wiki/Uncyclopedia:%E7%A7%80%E9%80%B8%E3%81%AA%E8%A8%98%E4%BA%8B')
    soup = BeautifulSoup(res.text, 'html.parser')

    lists = soup.find('div', {'class': 'column-width'})
    elements =  lists.find_all('li')
    titles = [li.find('a')['title'] for li in elements]

    return random.choice(titles)
    
@bot.event
async def on_ready():
    print("Bot is ready!")
    weekly_task.start()


@tasks.loop(weeks=1)
async def weekly_task():
    now = datetime.now(JST)
    if now.weekday() == 4:
        channel_id = 1006941771282010154
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(f'https://ansaikuropedia.org/wiki/{createUrl()}')

