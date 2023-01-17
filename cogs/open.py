import json

import discord
from discord.ext import commands


class Open(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:  # 檢測反應者是否為機器人
            return  # 如果是就結束運行(防止偵測機器人自己按的)
        if payload.emoji.name != "📩":  # 檢查是否為"開啟"emoji
            return  # 如果不是,結束運行
        path = "database/open.json"
        with open(path, "r") as file:  # 以read模式開啟檔案
            data = json.load(file)  # 載入檔案資料
        guildID = str(payload.guild_id)
        if guildID not in data.keys():  # 檢查群組是否有設置
            return  # 結束運行
        if payload.message_id != data[guildID]["message"]:  # 檢查是否是開啟訊息
            return  # 結束運行
        guild = await self.bot.fetch_guild(payload.guild_id)  # 抓取群組資訊
        channel = await self.bot.fetch_channel(payload.channel_id)  # 抓取目前頻道
        message = await channel.fetch_message(payload.message_id)  # 抓取開啟訊息
        # 抓取類別資訊
        category = await self.bot.fetch_channel(data[guildID]["category"])
        await message.remove_reaction("📩", payload.member)  # 移除被添加的反應
        # 設置頻道權限
        overwrites = {
            payload.member: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        # 創建客服頻道
        ticket = await guild.create_text_channel(
            name=f"ticket-{payload.member.name}", category=category, overwrites=overwrites
        )
        # 客服單關閉嵌入訊息
        embed = discord.Embed(title=f"{payload.member} 的客服單", description="請詳細說明您的問題並等待管理員處理")
        message = await ticket.send(embed=embed)  # 在客服單傳送初始訊息
        await message.add_reaction("🔒")  # 添加關閉反應
        # 新增關閉Ticket訊息資料
        with open("database/close.json", "r") as file:  # 用read模式開啟資料檔案
            data = json.load(file)  # 讀取資料
            # 更改資料字典(複習https://youtu.be/y7Wa7NaSKgs)
            data[str(ticket.id)] = message.id
        with open("database/close.json", "w") as file:  # 用write模式開啟資料檔案
            json.dump(data, file, indent=4)  # 上傳更新後的資料
        await ticket.send(payload.member.mention, delete_after=0)  # 傳送提示訊息


def setup(bot):
    bot.add_cog(Open(bot))
