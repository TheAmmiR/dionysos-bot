import discord
import tinydb
import menu
import random
import config
import dbl
import local
import start
from discord.ext import commands

class TopGG(commands.Cog, name = '{topggcog}'):
	def __init__(self, bot):
		self.bot = bot
		self.token = start.dbl_token
		self.dblpy = dbl.DBLClient(self.bot, self.token, autopost = True, webhook_path='http://95.179.167.177:8000/dblwebhook', webhook_auth='dionysos1', webhook_port = '8000')
		self.db = tinydb.TinyDB('user_votes.json')
		self.query = tinydb.Query()
		

	def take_vote(self, user):
		search = self.db.search(self.query.user == user)
		if (not search):
			return False
		else:
			search = search[0]
			votes = search['votes']
			if (votes < 1):
				return False
			else:
				self.db.update({'votes': votes - 1}, self.query.user == user)
				return True

	@commands.Cog.listener()
	async def on_dbl_vote(self, data):
		search = self.db.search(self.query.user == data['user'])
		if not (search):
			self.db.insert({'user': data['user'], 'votes': 1})
		else:
			search = search[0]
			votes = search['votes']
			self.db.update({'votes': votes + 1}, self.query.user == data['user'])
		print(data)

	@commands.command(name = 'шампанское', aliases = ['champagne', 'шампусик', 'шампунь'])
	async def order_champagne(self, ctx):
		locs = local.get_localized(ctx)
		if (self.take_vote(ctx.author.id)):
			embed = discord.Embed(
				colour = 0x289566,
				description = random.choice(menu.ORDER_PHRASES)
				)
			embed.set_image(url = random.choice(menu.CHAMPAGNE_PICS))
			embed.set_footer(text = random.choice(menu.CHAMPAGNE_FACTS))

			await ctx.send(embed = embed)
		else:
			await ctx.send(embed = discord.Embed(
					colour = 0xff5555,
					description = locs['novotes']
				))

def setup(bot):
	bot.add_cog(TopGG(bot))
