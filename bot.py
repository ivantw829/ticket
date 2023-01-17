import os

import decouple
import discord
from discord.ext import commands

bot = commands.Bot(help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready() -> None:
    print(f">>{bot.user}上線<<")
    game = discord.Game("Ticket 系統")
    await bot.change_presence(status=discord.Status.online, activity=game)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"✅   已加載 {filename}")
        except Exception as error:
            print(f"❎   {filename} 發生錯誤  {error}")

bot.run(decouple.config("TOKEN"))
