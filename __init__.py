from pyplanet.apps.config import AppConfig

from pyplanet.apps.contrib.formula1.toolbar import ToolbarRaceControl
from pyplanet.apps.contrib.formula1.gauge import Formula1GaugeApp
from pyplanet.apps.contrib.formula1.best_cps import BestCpTimes
from pyplanet.apps.contrib.formula1.live_rankings import LiveRankings
from pyplanet.apps.contrib.formula1.infos import Formula1Infos
from pyplanet.apps.contrib.formula1.ui import TMUIApp
from pyplanet.apps.contrib.formula1.meteo import MeteoManagement
from pyplanet.apps.contrib.formula1.race import RaceManagement
from pyplanet.apps.contrib.formula1.logs import F1Logs
# from pyplanet.apps.contrib.formula1.fia_auto_detection import FiaAutoDetection
# from pyplanet.apps.contrib.formula1.cheat_detection import CheatDetection

from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.core.events.manager import SignalManager

import asyncio

class Formula1(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ToolbarAdmin = ToolbarRaceControl(self)
		self.FuelGauge = Formula1GaugeApp(self)
		self.BestCps = BestCpTimes(self)
		self.RaceRanking = LiveRankings(self)
		self.RaceInfos = Formula1Infos(self)
		self.CustomUI = TMUIApp(self)
		self.Meteo = MeteoManagement(self)
		self.RaceManagement = RaceManagement(self)
		self.F1Logs = F1Logs(self)
		self.F1Logs.log('INFO', "=========================================================")
		self.F1Logs.log('INFO', "=====================F1 Plugin Start=====================")
		self.F1Logs.log('INFO', "=========================================================")
		# self.FiaAutoDetection = FiaAutoDetection(self)
		# self.CheatDetection = CheatDetection(self)

	async def on_start(self):
		# self.context.signals.listen(mp_signals.player.player_info_changed, self.player_info_changed)
		# self.context.signals.listen(tm_signals.waypoint, self.new_checkpoint)
		# self.context.signals.listen(tm_signals.finish, self.new_checkpoint)
		await super().on_start()
		await self.ToolbarAdmin.on_start()
		await self.FuelGauge.on_start()
		await self.BestCps.on_start()
		await self.RaceRanking.on_start()
		await self.RaceInfos.on_start()
		await self.CustomUI.on_start()
		await self.Meteo.on_start()
		await self.RaceManagement.on_start()
		# await self.FiaAutoDetection.on_start()
		# await self.CheatDetection.on_start()
		# await self.chargeServer()

	# async def new_checkpoint(self, raw, *args, **kwargs):
		# await self.instance.gbx('connectFakePlayer')
	
	async def chargeServer(self):
		await self.FuelGauge.chargeServer('bot')
		while True:
			await asyncio.sleep(0.1)
			await self.FuelGauge.new_checkpoint({'login':'bot', 'checkpointinlap':5, 'checkpointinrace':5, 'speed':195, 'distance':150})
			

	async def player_info_changed(self, is_spectator, *args, **kwargs):
		if is_spectator == True:
			await self.RaceRanking.on_stop()
		else:
			await self.RaceRanking.on_start()