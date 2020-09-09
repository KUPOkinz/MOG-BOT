from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "*"
OWNER_IDS = [396766040182358017]


class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running bot...")
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("bot connected!")

	async def on_disconnect(self):
		print("bot disconnected!")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("Something went wrong!")

		channel = self.get_channel(752575907805528147)
		await channel.send("An error occured!")
		raise

	async def on_command_error(self, ctx, exc):
		if isinstance(exc, CommandNotFound):
			pass

		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(752575907012673569)
			print("bot ready!")

			channel = self.get_channel(752575907805528147)
			await channel.send("Now online!")

			embed = Embed(title="Now online!", description="MOG is now online!", 
						  colour=0xFF0000, timestamp=datetime.utcnow())
			fields = [("Name", "Value", True),
					  ("Another field", "This field is next to the other one.", True),
					  ("A non-inline field", "This field will appear of it's own row.", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_author(name="MOG", icon_url=self.guild.icon_url)
			embed.set_footer(text="This is a footer!")
			embed.set_thumbnail(url=self.guild.icon_url)
			embed.set_image(url=self.guild.icon_url)
			await channel.send(embed=embed)

			await channel.send(file=File("./data/images/profile.png"))

		else:
			print("bot reconnected!")

	async def on_message(self, message):
		pass


bot = Bot()