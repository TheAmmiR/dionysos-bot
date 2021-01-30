import discord
import config
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.presences = True; intents.members = True

class HelpCommand(commands.HelpCommand):
	def __init__(self):
		super().__init__(command_attrs = {
				'name': 'хелп',
				'brief': 'Показывает это сообщение.',
				'aliases': ['help', 'меню', 'menu']
			})

	def format_command_aliases(self, command):
		if not (command.aliases):
			return

		return ', '.join(f'`{alias}`' for alias in command.aliases)

	async def send_bot_help(self, mapping):
		for key, value in mapping.items():
			mapping[key] = await self.filter_commands(value)

		embed = discord.Embed(colour = 0x289566, description = 'На территории барной стойки действует сухой закон, алкоголь не продаётся.',)
		
		for cog, commands in mapping.items():
			commands = list(set(commands))
			value = []
			for com in commands:
				value.append(f'`{self.context.prefix}{com.name}` - {self.format_command_aliases(com)}')
			embed.add_field(name = f'{cog.qualified_name if cog else "Прочее"}:', value = '\n'.join(value))
		embed.add_field(name = 'Сервер поддержки: ', value = '**https://discord.gg/A4NETzF**')

		await self.context.send(embed = embed)

def get_pre(bot, message):
	return ['a!', 'а!']

bot = commands.Bot(command_prefix = get_pre, intents = intents, status = discord.Status.dnd, activity = discord.Game(name = 'a!хелп'))
bot.help_command = HelpCommand()

@bot.event
async def on_ready():
	curr_dir = os.listdir()
	for file in curr_dir:
		if (file.endswith('cog.py')):
			try:
				bot.load_extension(file[:-3])
			except Exception as e:
				print(f'[{file.upper()}]: LOAD FAIL! {type(e).__name__}: {e}')
			else:
				print(f'[{file.upper()}]: LOAD SUCCESS')

@bot.event
async def on_guild_join(guild):
	channel = bot.get_channel(config.LOG_CHANNEL)
	await channel.send(config.JOIN_MSG.format(guild = guild, count = len(bot.guilds)))

@bot.event
async def on_guild_remove(guild):
	channel = bot.get_channel(config.LOG_CHANNEL)
	await channel.send(config.LEAVE_MSG.format(guild = guild, count = len(bot.guilds)))

@bot.event
async def on_member_update(before, after):
	channel = bot.get_channel(config.LOG_CHANNEL)
	if (after.id == bot.user.id):
		if (before.display_name != after.display_name):
			await channel.send(config.CHANGE_NICKNAME_MSG.format(guild = after.guild, new = after.display_name))

@bot.command(name = 'инвайт', aliases = ['invite'])
async def bot_invite(ctx):
	permissions = discord.Permissions(
			create_instant_invite = True,
			change_nickname = True,
			read_messages = True,
			send_messages = True,
			send_tts_messages = True,
			embed_links = True,
			attach_files = True,
			read_message_history = True,
			use_external_emojis = True,
			add_reactions = True
		)
	bot_id = bot.user.id
	await ctx.send(embed = discord.Embed(colour = 0x289566, description = f'Перейдите по следующей ссылке, что-бы пригласить бота на ваш сервер: https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions={permissions.value}&scope=bot'))

@bot.command(name = 'воут', aliases = ['vote'])
async def dblvote(ctx):
	await ctx.send('Привет, это Амир. Я вижу, что некоторым людям стало интересно, что из себя представляет мой бот, но, к сожалению, пока-что шампанское не доступно по техническим причинам. Простите, если уже успели почувствовать себя обманутыми. :)')
	await ctx.send(embed = discord.Embed(colour = 0x289566, description = f'Перейдите по следующей ссылке, что-бы проголосовать за бота: https://top.gg/bot/{bot.user.id}/vote'))

with open('token.txt', 'r') as file:
	token = file.read()
bot.run(token)