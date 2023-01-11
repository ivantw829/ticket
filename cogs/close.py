import discord
import os
import json
import asyncio
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class close(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        path = "database/close.json"
        if not os.path.isfile(path):  # 檢測是否有設置檔
            with open(path, "w") as file:  # 創建新的設置檔
                data = {}
                json.dump(data, file, indent=4)
        if payload.emoji.name != "🔒":  # 檢測是否是關閉reaction
            return  # 如果不是就結束運行
        with open(path, "r") as file:  # 開啟關閉訊息資料檔案
            data = json.load(file)  # 載入資料
        if not data[str(payload.channel_id)] == payload.message_id:  # 檢測該訊息是否是關閉訊息
            return  # 如果不是就結束運行
        channel = await self.bot.fetch_channel(payload.channel_id)  # 抓取該頻道資料
        await channel.send("Ticket將在10秒後刪除")
        await asyncio.sleep(10)  # 等待10秒鐘
        await channel.delete(reason=F"由 {payload.member} 關閉Ticket")
        with open(path, "w") as file:
            del data[str(payload.channel_id)]  # 移除關閉訊息資料中的該頻道資料
            json.dump(data, file)


def setup(bot):
    bot.add_cog(close(bot))
