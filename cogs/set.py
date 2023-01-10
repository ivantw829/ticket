import discord
import json
import os
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command


class set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="設置Ticket")
    async def set_ticket(self, ctx,
                         頻道: Option(discord.TextChannel, "開啟訊息要發送至的頻道"),
                         類別: Option(discord.CategoryChannel, "Ticket開啟類別"),
                         標題: Option(str, "開啟訊息的標題", default="開啟 Ticket"),
                         內容: Option(str, "開啟訊息的內容", default="如果您需要聯繫管理員\n請點擊反應開啟Ticket")):
        await ctx.defer()  # 延遲回應
        embed = discord.Embed(title=標題, description=內容, color=0xFEE45C)
        message = await 頻道.send(embed=embed)  # 傳送開啟訊息
        await message.add_reaction("📩")  # 添加反應
        path = F"database/open.json"
        if not os.path.isfile(path):  # 檢測是否有設置檔
            with open(path, "w") as file:  # 創建新的設置檔
                data = {}
                json.dump(data, file, indent=4)
        with open(path, "r") as file:  # 以read模式開啟檔案
            data = json.load(file)  # 讀取檔案裡的資料
            data[str(ctx.guild.id)] = {
                "category": 類別.id,
                "message": message.id}  # 新增/更新字典資料
        with open(path, "w") as file:  # 以write模式開啟資料
            json.dump(data, file, indent=4)  # 上載更新後的資料
        await ctx.respond("已設置Ticket", ephemeral=True, delete_after=5)


def setup(bot):
    bot.add_cog(set(bot))
