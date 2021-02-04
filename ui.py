import asyncio
import aiohttp
import logging

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.contrib.command import Command
from pyplanet.utils import times

from pyplanet import __version__ as pyplanet_version

from pyplanet.apps.contrib.formula1.view import DiscordLogoView
from pyplanet.apps.contrib.formula1.view import CheckpointInfoView

from pyplanet.apps.contrib.local_records.models import LocalRecord
from pyplanet.apps.core.maniaplanet.models import Player

from pyplanet.apps.core.pyplanet.views.controller import ControllerView


class TMUIApp:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.discord_view = DiscordLogoView(self, manager=self.app.context.ui)
		
		self.discord_join_url = "https://discord.gg/wUEMWgG"
		self.discord_server_id = "528676128244629565"
		
		self.CheckpointInfosTimeOn = 5 # seconds
		
		self.ObjectsCheckpointInfos = {}
		self.BestLaps = {}
		self.map_record = 0
		self.controller_view = ControllerView(manager=self.app.context.ui)

	async def on_start(self):
		self.app.context.signals.listen(tm_signals.start_countdown, self.start_countdown)
		self.app.context.signals.listen(mp_signals.player.player_connect, self.on_connect)
		self.app.context.signals.listen(tm_signals.waypoint, self.new_checkpoint)
		self.app.context.signals.listen(tm_signals.finish, self.new_checkpoint)
		self.app.context.signals.listen(mp_signals.flow.podium_start, self.podium_start)
		self.app.context.signals.listen(mp_signals.map.map_begin, self.map_begin)
		await self.set_ui()
		
		await self.instance.command_manager.register(
			Command(command='discord', target=self.chat_discord, admin=False),
		)
		
		if self.app.RaceManagement.ActualModeID == 0:
			await self.discord_view.display(player_logins=None)
		else:
			await self.discord_view.hide(player_logins=None)
		
		await self.refresh_locals()

	async def map_begin(self, *args, **kwargs):
		if self.app.RaceManagement.ActualModeID == 0:
			await self.discord_view.display(player_logins=None)
		else:
			await self.discord_view.hide(player_logins=None)
		await self.set_ui()

	async def on_connect(self, player, *args, **kwargs):
		await self.set_ui()
		if self.app.RaceManagement.ActualModeID == 0:
			await self.discord_view.display(player_logins=[player.login])		

	async def podium_start(self, *args, **kwargs):
		await self.set_ui()
		self.ObjectsCheckpointInfos = {}
		self.BestLaps = {}
		self.map_record = 0

	async def start_countdown(self, player, *args, **kwargs):
		await self.set_ui()
		await self.refresh_locals()
	
	async def set_ui(self):		
		if self.app.RaceManagement.ActualModeID == 1 or self.app.RaceManagement.ActualModeID == 2 or self.app.RaceManagement.ActualModeID == 3:
			self.instance.ui_manager.properties.set_attribute('countdown', 'visible', True)
		else:
			self.instance.ui_manager.properties.set_attribute('countdown', 'visible', False)
		
		self.instance.ui_manager.properties.set_attribute('round_scores', 'pos', '-186.5 87. 150.')
		self.instance.ui_manager.properties.set_attribute('checkpoint_ranking', 'pos', '0. 84. 5.')
		self.instance.ui_manager.properties.set_visibility('checkpoint_ranking', False)
		self.instance.ui_manager.properties.set_attribute('multilap_info', 'pos', '145., 93.5, 5.')
		self.instance.ui_manager.properties.set_attribute('checkpoint_list', 'pos', '48. -52. 5.')
		self.instance.ui_manager.properties.set_visibility('checkpoint_list', False)
		self.instance.ui_manager.properties.set_visibility('checkpoint_time', False)
		self.instance.ui_manager.properties.set_attribute('speed_and_distance', 'pos', '0. -69. 5.')
		self.instance.ui_manager.properties.set_attribute('spectator_info', 'pos', '0. -82.5 5.')
		self.instance.ui_manager.properties.set_attribute('countdown', 'pos', '153. -60. 5.')
		self.instance.ui_manager.properties.set_attribute('map_info', 'pos', '40. 90. 150.')
		self.instance.ui_manager.properties.set_visibility('map_info', True)
		self.instance.ui_manager.properties.set_attribute('position', 'pos', '-120 85.5 201.')
		#self.instance.ui_manager.properties.set_attribute('position', 'pos', '-120 23.5 201.')
		self.instance.ui_manager.properties.set_visibility('position', True)		
		self.instance.ui_manager.properties.set_visibility('personal_best_and_rank', False)
		self.instance.ui_manager.properties.set_attribute('chrono', 'pos', '0. -80. -5.')
		self.instance.ui_manager.properties.set_visibility('chrono', False)
		self.instance.ui_manager.properties.set_visibility('chat_avatar', False)
		self.instance.ui_manager.properties.set_visibility('endmap_ladder_recap', False)
		self.instance.ui_manager.properties.set_visibility('scorestable', True)
		self.instance.ui_manager.properties.set_visibility('viewers_count', False)
		self.instance.ui_manager.properties.set_attribute('scorestable', 'alt_visible', True)
		self.instance.ui_manager.properties.set_attribute('chat', 'linecount', '5')
		await self.controller_view.hide()
		await self.instance.ui_manager.properties.send_properties()
		await self.instance.gbx('SetForceShowAllOpponents', 4)

	async def new_checkpoint(self, raw, *args, **kwargs):
		# print("Status Counter : %s" % self.instance.ui_manager.properties.get_visibility('speed_and_distance'))
		if not raw['login'] in self.ObjectsCheckpointInfos:
			self.ObjectsCheckpointInfos[raw['login']] = CheckpointInfoView(self, manager=self.app.context.ui)
		# print(self.ObjectsCheckpointInfos)
		if raw['login'] in self.BestLaps:
			# print("Checkpoint Record : %s" % times.format_time(int(self.BestLaps[raw['login']][1].split(',')[raw['checkpointinlap']])))
			# print("Current Checkpoint : %s" % times.format_time(int(raw['curlapcheckpoints'][raw['checkpointinlap']])))
			# print("Checkpoint Gap : %s" % times.format_time(int(raw['curlapcheckpoints'][raw['checkpointinlap']]) - int(self.BestLaps[raw['login']][1].split(',')[raw['checkpointinlap']])))
			# print("----------")
			self.ObjectsCheckpointInfos[raw['login']].lap_record = int(self.BestLaps[raw['login']][0])
			self.ObjectsCheckpointInfos[raw['login']].lap_time = int(raw['laptime'])
			self.ObjectsCheckpointInfos[raw['login']].lap_gap = int(raw['laptime']) - int(self.BestLaps[raw['login']][0])
			self.ObjectsCheckpointInfos[raw['login']].checkpoint_time = int(raw['curlapcheckpoints'][raw['checkpointinlap']])
			self.ObjectsCheckpointInfos[raw['login']].checkpoint_gap = int(raw['curlapcheckpoints'][raw['checkpointinlap']]) - int(self.BestLaps[raw['login']][1].split(',')[raw['checkpointinlap']])
			self.ObjectsCheckpointInfos[raw['login']].isFinishLine = raw['isendlap']
			await self.ObjectsCheckpointInfos[raw['login']].display(player_logins=[raw['login']])
			await asyncio.sleep(self.CheckpointInfosTimeOn)
			if raw['login'] in self.ObjectsCheckpointInfos:
				await self.ObjectsCheckpointInfos[raw['login']].hide(player_logins=[raw['login']])
		else:
			self.ObjectsCheckpointInfos[raw['login']].lap_record = 0
			self.ObjectsCheckpointInfos[raw['login']].lap_time = int(raw['laptime'])
			self.ObjectsCheckpointInfos[raw['login']].lap_gap = int(raw['laptime']) - 0
			self.ObjectsCheckpointInfos[raw['login']].checkpoint_time = int(raw['curlapcheckpoints'][raw['checkpointinlap']])
			self.ObjectsCheckpointInfos[raw['login']].checkpoint_gap = int(raw['curlapcheckpoints'][raw['checkpointinlap']]) - 0
			self.ObjectsCheckpointInfos[raw['login']].isFinishLine = raw['isendlap']
			await self.ObjectsCheckpointInfos[raw['login']].display(player_logins=[raw['login']])
			await asyncio.sleep(self.CheckpointInfosTimeOn)
			if raw['login'] in self.ObjectsCheckpointInfos:
				await self.ObjectsCheckpointInfos[raw['login']].hide(player_logins=[raw['login']])
		if raw['isendlap'] == True:
			# print(self.BestLaps)
			await self.refresh_locals()
		# print("----------")
		# print("----------")

	async def chat_discord(self, player, *args, **kwargs):
		users = await self.get_discord_users()
		if users:
			join_url_link = '$l[' + self.discord_join_url + ']Join our Discord$l! '
			message = '$ff0$i{}There are currently {} users and {} bots online.' \
				.format(join_url_link, users[0], users[1])
			await self.app.instance.chat(message, player)

	async def get_discord_users(self):
		url = "https://discordapp.com/api/guilds/" + self.discord_server_id + "/widget.json"

		with aiohttp.ClientSession(headers={'User-Agent': 'PyPlanet/{}'.format(pyplanet_version)}) as session:
			try:
				async with session.get(url) as response:
					data = await response.json()
					non_bot_users = []
					bots = []
					for i in data['members']:
						if 'bot' in i:
							bots.append(i)
						else:
							non_bot_users.append(i)
					online_users = len(non_bot_users)
					return [int(online_users), int(len(bots))]
			except Exception as e:
				logging.error('Error with retrieving Discord user list')
				logging.error(e)
				return False

	async def refresh_locals(self):
		# print("REFRESH LOCALS")
		record_list = await LocalRecord.objects.execute(
			LocalRecord.select(LocalRecord, Player)
				.join(Player)
				.where(LocalRecord.map_id == self.instance.map_manager.current_map.get_id())
				.order_by(LocalRecord.score.asc())
		)
		if len(record_list) >= 1:
			self.map_record = record_list[0].score
		else:
			self.map_record = 999999999
		for line in list(record_list):
			self.BestLaps[line.player.login] = [line.score, line.checkpoints]