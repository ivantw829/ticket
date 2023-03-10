import json
from typing import Any

import aiofiles
import discord
from discord.ext import commands


class Open(commands.Cog):
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: Any) -> None:
        if payload.member.bot or payload.emoji.name != "ð©":
            return  # çµæéè¡
        path = "database/open.json"
        async with aiofiles.open(path, "r") as file:  # ä»¥readæ¨¡å¼éåæªæ¡
            data = json.loads(await file.read())  # è¼å¥æªæ¡è³æ
        guildID = str(payload.guild_id)
        if guildID not in data.keys() or payload.message_id != data[guildID]["message"]:
            return  # çµæéè¡
        guild = await self.bot.fetch_guild(payload.guild_id)  # æåç¾¤çµè³è¨
        channel = await self.bot.fetch_channel(payload.channel_id)  # æåç®åé »é
        message = await channel.fetch_message(payload.message_id)  # æåéåè¨æ¯
        category = await self.bot.fetch_channel(data[guildID]["category"])  # æåé¡å¥è³è¨
        await message.remove_reaction("ð©", payload.member)  # ç§»é¤è¢«æ·»å çåæ
        # è¨­ç½®é »éæ¬é
        overwrites = {
            payload.member: discord.PermissionOverwrite(read_messages=True),
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        # åµå»ºå®¢æé »é
        ticket = await guild.create_text_channel(
            name=f"ticket-{payload.member.name}", category=category, overwrites=overwrites
        )
        # å®¢æå®ééåµå¥è¨æ¯
        embed = discord.Embed(title=f"{payload.member} çå®¢æå®", description="è«è©³ç´°èªªææ¨çåé¡ä¸¦ç­å¾ç®¡çå¡èç")
        message = await ticket.send(embed=embed)  # å¨å®¢æå®å³éåå§è¨æ¯
        await message.add_reaction("ð")  # æ·»å ééåæ
        # æ°å¢ééTicketè¨æ¯è³æ
        async with aiofiles.open("database/close.json", "r") as file:  # ç¨readæ¨¡å¼éåè³ææªæ¡
            data = await json.loads(await file.read())  # è®åè³æ
            # æ´æ¹è³æå­å¸(è¤ç¿https://youtu.be/y7Wa7NaSKgs)
            data[str(ticket.id)] = message.id
        async with aiofiles.open("database/close.json", "w") as file:  # ç¨writeæ¨¡å¼éåè³ææªæ¡
            await file.write(json.dumps(data))  # ä¸å³æ´æ°å¾çè³æ
        await ticket.send(payload.member.mention, delete_after=0)  # å³éæç¤ºè¨æ¯


def setup(bot: discord.Bot) -> None:
    bot.add_cog(Open(bot))
