from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.apps.contrib.formula1.view import MeteoView


class MeteoManagement:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.MeteoCheckpointData = {}
		self.CheckpointNumberWithoutStart = 13
		self.MeteoText = [
			"Sun", # 0 = Sun
			"Clouds", # 1 = Clouds
			"Fog", # 2 = Fog
			"Rain", # 3 = Rain
			"Snow", # 4 = Snow
		]
		self.PlayersObjectMeteo = {}

	async def on_start(self):
		await self.initMeteo()
		self.app.context.signals.listen(tm_signals.start_countdown, self.start_countdown)
		self.app.context.signals.listen(tm_signals.waypoint, self.new_checkpoint)
		self.app.context.signals.listen(tm_signals.finish, self.new_checkpoint)
		self.app.context.signals.listen(mp_signals.flow.podium_start, self.podium_start)
		self.app.context.signals.listen(mp_signals.player.player_connect, self.on_connect)
		
		players = self.instance.player_manager.online
		
		for p in players:
			if not p.login in self.PlayersObjectMeteo:
				self.PlayersObjectMeteo[p.login] = MeteoView(self, manager=self.app.context.ui)

	async def on_connect(self, player, *args, **kwargs):
		if not player.login in self.PlayersObjectMeteo:
			self.PlayersObjectMeteo[player.login] = MeteoView(self, manager=self.app.context.ui)

	async def podium_start(self, *args, **kwargs):
		await self.initMeteo()

	async def start_countdown(self, player, *args, **kwargs):
		await self.initMeteo()

	async def new_checkpoint(self, raw, *args, **kwargs):
		CheckNb = raw['checkpointinlap'] + 1
		if CheckNb > 13:
			CheckNb = 0
		# print("%s, check n°%s, end = %s, CheckNb = %s" % (raw['login'], raw['checkpointinlap'], raw['isendlap'], CheckNb))
		if self.MeteoCheckpointData[CheckNb] > 0:
			if self.MeteoCheckpointData[CheckNb] == 1:
				self.PlayersObjectMeteo[raw['login']].meteo_name = "background_clouds.webm"
				self.PlayersObjectMeteo[raw['login']].meteo_image = 0
				self.PlayersObjectMeteo[raw['login']].meteo_video = 0
				self.PlayersObjectMeteo[raw['login']].meteo_sound = ""
				self.PlayersObjectMeteo[raw['login']].meteo_sound_active = 0
				self.PlayersObjectMeteo[raw['login']].grey_background = 0
				self.PlayersObjectMeteo[raw['login']].grey_background_color_value = "00000077"
			elif self.MeteoCheckpointData[CheckNb] == 2:
				self.PlayersObjectMeteo[raw['login']].meteo_name = "background_fog.png"
				self.PlayersObjectMeteo[raw['login']].meteo_image = 1
				self.PlayersObjectMeteo[raw['login']].meteo_video = 0
				self.PlayersObjectMeteo[raw['login']].meteo_sound = ""
				self.PlayersObjectMeteo[raw['login']].meteo_sound_active = 0
				self.PlayersObjectMeteo[raw['login']].grey_background = 1
				self.PlayersObjectMeteo[raw['login']].grey_background_color_value = "000000aa"
			elif self.MeteoCheckpointData[CheckNb] == 3:
				self.PlayersObjectMeteo[raw['login']].meteo_name = "background_rain.webm"
				self.PlayersObjectMeteo[raw['login']].meteo_image = 0
				self.PlayersObjectMeteo[raw['login']].meteo_video = 1
				self.PlayersObjectMeteo[raw['login']].meteo_sound = ""
				self.PlayersObjectMeteo[raw['login']].meteo_sound_active = 0
				self.PlayersObjectMeteo[raw['login']].grey_background = 1
				self.PlayersObjectMeteo[raw['login']].grey_background_color_value = "00000077"
			elif self.MeteoCheckpointData[CheckNb] == 4:
				self.PlayersObjectMeteo[raw['login']].meteo_name = "background_snowflake.webm"
				self.PlayersObjectMeteo[raw['login']].meteo_image = 0
				self.PlayersObjectMeteo[raw['login']].meteo_video = 1
				self.PlayersObjectMeteo[raw['login']].meteo_sound = ""
				self.PlayersObjectMeteo[raw['login']].meteo_sound_active = 0
				self.PlayersObjectMeteo[raw['login']].grey_background = 1
				self.PlayersObjectMeteo[raw['login']].grey_background_color_value = "00000077"
			else:
				self.PlayersObjectMeteo[raw['login']].meteo_name = "background_sun.webm"
				self.PlayersObjectMeteo[raw['login']].meteo_image = 0
				self.PlayersObjectMeteo[raw['login']].meteo_video = 0
				self.PlayersObjectMeteo[raw['login']].meteo_sound = ""
				self.PlayersObjectMeteo[raw['login']].meteo_sound_active = 0
				self.PlayersObjectMeteo[raw['login']].grey_background = 0
				self.PlayersObjectMeteo[raw['login']].grey_background_color_value = "00000077"
			await self.PlayersObjectMeteo[raw['login']].display(player_logins=[raw['login']])
		else:
			await self.PlayersObjectMeteo[raw['login']].hide(player_logins=[raw['login']])
	
	async def initMeteo(self):
		self.MeteoCheckpointData = {}
		for i in range(0,self.CheckpointNumberWithoutStart + 1):
			self.MeteoCheckpointData[i] = 0