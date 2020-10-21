from discord.ext import commands
import discord
import json
import os

# Requires message intent for role remove

class RoleAssign(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.load()

    def save(self):
        with open('roleconfig.json', 'w') as fp:
            json.dump(self.watchedMessages, fp, indent=4)

    def load(self):
        if os.path.exists('roleconfig.json'):
            with open('roleconfig.json', 'r') as fp:
                self.watchedMessages = json.load(fp)
                self.watchedMessages = {int(x):self.watchedMessages[x] for x in self.watchedMessages}
        else:
            self.watchedMessages = {} # structure will be msgid = {emoji1:role1, emoji2:role2}
            self.save()

    @commands.command()
    async def createAssignMsg(self, ctx, *args):
        msg = await ctx.send('React to get the following roles!')
        self.watchedMessages[msg.id] = {}
        for i in range(1, len(args), 2):
            await msg.add_reaction(args[i])
            self.watchedMessages[msg.id][args[i]] = int(args[i-1][3:-1])

        await self.editmessage(msg)
        self.save()

    async def editmessage(self, msg):
        s = 'React to get the following roles!'
        for e in self.watchedMessages[msg.id]:
            r = discord.utils.get(msg.guild.roles, id = self.watchedMessages[msg.id][e])
            s += '\n{} : {}'.format(e, r.mention)
        await msg.edit(content = s)


    @commands.command()
    async def addRole(self, ctx, *args):
        msg = await ctx.channel.history().get(author = self.bot.user)
        for i in range(1, len(args), 2):
            await msg.add_reaction(args[i])
            self.watchedMessages[msg.id][args[i]] = int(args[i-1][3:-1])
        await self.editmessage(msg)

    @commands.command()
    async def removeRole(self, ctx, *args):
        msg = await ctx.channel.history().get(author = self.bot.user)
        for e in args:
            del self.watchedMessages[msg.id][e]
            await msg.clear_reaction(e)
        await self.editmessage(msg)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member == self.bot.user:
            return
        elif payload.message_id in self.watchedMessages:
            r = discord.utils.get(payload.member.guild.roles, id = self.watchedMessages[payload.message_id][str(payload.emoji)])
            await payload.member.add_roles(r)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.watchedMessages:
            g = self.bot.get_guild(payload.guild_id)
            m = g.get_member(payload.user_id)
            r = discord.utils.get(g.roles, id = self.watchedMessages[payload.message_id][str(payload.emoji)])
            await m.remove_roles(r)
