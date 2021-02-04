import asyncio

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.contrib.formula1.view import BestLapView

from pyplanet.utils import times


class RaceManagement:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.SaisonNb = 2
		self.RaceNb = 1
		self.ActualModeID = 0
		self.ActualMode = "Essais publics"
		self.ActualRace = "Taipei"
		self.ActualRaceLapsNb = 50
		self.MapToDeleteAtNextMapStart = None
		self.FinishFlagShowed = False
		self.lap_record = 9999999
		self.lap_record_login = ''
		self.LapNbBeforeShowLapRecord = 3 # The Lap Record will be showed to streamers after lap number X

	async def on_start(self):
		self.app.context.signals.listen(mp_signals.map.map_begin, self.map_begin)
		self.app.context.signals.listen(tm_signals.start_countdown, self.start_countdown)
		self.app.context.signals.listen(tm_signals.finish , self.finish)
		# self.app.context.signals.listen(tm_signals.waypoint, self.finish)
		# self.app.context.signals.listen(tm_signals.scores , self.scores)
		# print("Actual Race : %s | Actual Race Laps Nb : %s | Actual Mode : %s | Actual Mode ID : %s" % (self.ActualRace, self.ActualRaceLapsNb, self.ActualMode, self.ActualModeID))
		# print(self.instance.map_manager.current_map.uid)
		self.BestLapView = BestLapView(self, manager=self.app.context.ui)
	
	# async def new_checkpoint(self, raw, *args, **kwargs):
		# print(self.app.RaceRanking.player_find_ranking(raw['login']))

	async def finish(self, raw, *args, **kwargs):
		# print(raw)
		if(raw['isendrace'] == True and self.FinishFlagShowed == False):
			await self.app.ToolbarAdmin.view.final_flag()
			self.FinishFlagShowed = True
			self.instance.ui_manager.properties.set_attribute('countdown', 'visible', True)
			await self.instance.ui_manager.properties.send_properties()
		if(raw['laptime'] < self.lap_record):
			self.lap_record = raw['laptime']
			self.lap_record_login = raw['login']
			if(len(raw['curracecheckpoints'])/(raw['checkpointinlap'] + 1) >= self.LapNbBeforeShowLapRecord and self.ActualModeID == 4):
				LapNb = int(raw['checkpointinrace'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				playerInfos = await self.app.instance.player_manager.get_player(self.lap_record_login)
				self.app.F1Logs.log('INFO', "New best lap from %s wth a time of %s" % (self.lap_record_login, self.lap_record), self.lap_record_login, LapNb, 'race.py', 'finish')
				self.BestLapView.best_lap_login = playerInfos.nickname
				self.BestLapView.best_lap_time = self.lap_record
				await self.BestLapView.display(player_logins=self.app.RaceInfos.StreamerLogins)
				await asyncio.sleep(10)
				await self.BestLapView.hide()
		if(self.ActualModeID == 4):
			LapNb = int(raw['checkpointinrace'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
			playerRankingDatas = self.app.RaceRanking.player_find_ranking(raw['login'])
			# print(playerRankingDatas)
			self.app.F1Logs.log_data("RACE|[]|%s|[]|LAP_FINISH|[]|%s|[]|%s|[]|%s|[]|%s|[]|%s" % (LapNb, raw['login'], playerRankingDatas['rank'], self.app.FuelGauge.MetersGauge[raw['login']],  playerRankingDatas['data']['nickname'], playerRankingDatas['data']['score']))

	async def start_countdown(self, *args, **kwargs):
		# print(self.ActualModeID)
		if self.ActualModeID == 4:
			# Reset datas course
			# self.app.F1Logs.reset_data()
			# Course, procédure de départ
			await asyncio.sleep(30)
			await self.app.ToolbarAdmin.view.start_procedure()

	async def map_begin(self, *args, **kwargs):
		self.FinishFlagShowed = False
		self.lap_record = 9999999
		self.lap_record_login = ''
		if self.MapToDeleteAtNextMapStart is not None:
			await self.instance.map_manager.remove_map(self.MapToDeleteAtNextMapStart)
			self.MapToDeleteAtNextMapStart = None
			# print(self.instance.map_manager.maps)
		if self.ActualModeID == 0:
			# Essais publics
			await self.app.instance.mode_manager.update_settings({'S_FinishTimeout': 420})
			await self.app.instance.mode_manager.update_settings({'S_AllowRespawn': True})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_settings({'S_TimeLimit': 300000})
			await self.app.instance.mode_manager.update_settings({'S_ForceLapsNb': 20})
			await self.app.instance.mode_manager.update_settings({'S_DelayBeforeNextMap': 30})
		elif self.ActualModeID == 1:
			# Essais libres
			await self.app.instance.mode_manager.update_settings({'S_AllowRespawn': True})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_settings({'S_TimeLimit': 900})
			await self.app.instance.mode_manager.update_settings({'S_ForceLapsNb': 99})
			await self.app.instance.mode_manager.update_settings({'S_DelayBeforeNextMap': 30})
		elif self.ActualModeID == 2:
			# Q1+Q2
			await self.app.instance.mode_manager.update_settings({'S_FinishTimeout': 240})
			await self.app.instance.mode_manager.update_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_settings({'S_TimeLimit': 450})
			await self.app.instance.mode_manager.update_settings({'S_ForceLapsNb': 3})
			await self.app.instance.mode_manager.update_settings({'S_DelayBeforeNextMap': 30})
		elif self.ActualModeID == 3:
			# Q3
			await self.app.instance.mode_manager.update_settings({'S_FinishTimeout': 120})
			await self.app.instance.mode_manager.update_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_settings({'S_TimeLimit': 330})
			await self.app.instance.mode_manager.update_settings({'S_ForceLapsNb': 3})
			await self.app.instance.mode_manager.update_settings({'S_DelayBeforeNextMap': 30})
		elif self.ActualModeID == 4:
			# Course
			await self.app.instance.mode_manager.update_settings({'S_FinishTimeout': 800})
			await self.app.instance.mode_manager.update_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_settings({'S_TimeLimit': 300000})
			await self.app.instance.mode_manager.update_settings({'S_ForceLapsNb': self.ActualRaceLapsNb})
			await self.app.instance.mode_manager.update_settings({'S_DelayBeforeNextMap': 60})
	
	async def set_mode(self, mode_id, mode_text, player):
		self.ActualModeID = mode_id
		self.ActualMode = mode_text
		
		# print(self.instance.map_manager.maps)
		MapsToDelete = []
		
		if self.ActualModeID == 0:
			# Essais publics
			await self.instance.mode_manager.set_next_script("Laps")
			await self.app.instance.mode_manager.update_next_settings({'S_FinishTimeout': 420})
			await self.app.instance.mode_manager.update_next_settings({'S_AllowRespawn': True})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_TimeLimit': 300000})
			await self.app.instance.mode_manager.update_next_settings({'S_ForceLapsNb': 20})
			await self.app.instance.mode_manager.update_next_settings({'S_DelayBeforeNextMap': 30})
			for map in self.instance.map_manager.maps:
				if map != self.instance.map_manager.current_map:
					MapsToDelete.append(map)
				else:
					self.MapToDeleteAtNextMapStart = map
			for map in MapsToDelete:
				await self.instance.map_manager.remove_map(map)
			try:
				await self.instance.map_manager.add_map("Downloaded/Black_laser.Map.Gbx", True, False)
			except:
				pass
			try:
				await self.instance.map_manager.add_map("Downloaded/Crater_Racing.Map.Gbx", True, False)
			except:
				pass
			try:
				await self.instance.map_manager.add_map("Downloaded/Vettel_Stadium.Map.Gbx", True, False)
			except:
				pass
		elif self.ActualModeID == 1:
			# Essais libres
			await self.instance.mode_manager.set_next_script("TimeAttack")
			await self.app.instance.mode_manager.update_next_settings({'S_AllowRespawn': True})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_TimeLimit': 900})
			await self.app.instance.mode_manager.update_next_settings({'S_ForceLapsNb': 99})
			await self.app.instance.mode_manager.update_next_settings({'S_DelayBeforeNextMap': 30})
			for map in self.instance.map_manager.maps:
				if map != self.instance.map_manager.current_map:
					MapsToDelete.append(map)
				else:
					self.MapToDeleteAtNextMapStart = map
			for map in MapsToDelete:
				await self.instance.map_manager.remove_map(map)
			try:
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Essai_1.Map.Gbx" % self.ActualRace, True, False)
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Essai_2.Map.Gbx" % self.ActualRace, True, False)
			except:
				self.instance.chat('$ff0Map already added !', self.app.RaceInfos.RefereeLogins)
				self.MapToDeleteAtNextMapStart = None
		elif self.ActualModeID == 2:
			# Q1+Q2
			await self.instance.mode_manager.set_next_script("Laps")
			await self.app.instance.mode_manager.update_next_settings({'S_FinishTimeout': 240})
			await self.app.instance.mode_manager.update_next_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_TimeLimit': 450})
			await self.app.instance.mode_manager.update_next_settings({'S_ForceLapsNb': 3})
			await self.app.instance.mode_manager.update_next_settings({'S_DelayBeforeNextMap': 30})
			for map in self.instance.map_manager.maps:
				if map != self.instance.map_manager.current_map:
					MapsToDelete.append(map)
				else:
					self.MapToDeleteAtNextMapStart = map
			for map in MapsToDelete:
				await self.instance.map_manager.remove_map(map)
			try:
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Q1.Map.Gbx" % self.ActualRace, True, False)
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Q2.Map.Gbx" % self.ActualRace, True, False)
			except:
				self.instance.chat('$ff0Map already added !', self.app.RaceInfos.RefereeLogins)
				self.MapToDeleteAtNextMapStart = None
		elif self.ActualModeID == 3:
			# Q3
			await self.instance.mode_manager.set_next_script("Laps")
			await self.app.instance.mode_manager.update_next_settings({'S_FinishTimeout': 120})
			await self.app.instance.mode_manager.update_next_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_TimeLimit': 330})
			await self.app.instance.mode_manager.update_next_settings({'S_ForceLapsNb': 3})
			await self.app.instance.mode_manager.update_next_settings({'S_DelayBeforeNextMap': 30})
			for map in self.instance.map_manager.maps:
				if map != self.instance.map_manager.current_map:
					MapsToDelete.append(map)
				else:
					self.MapToDeleteAtNextMapStart = map
			for map in MapsToDelete:
				await self.instance.map_manager.remove_map(map)
			try:
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Q3.Map.Gbx" % self.ActualRace, True, False)
			except:
				self.instance.chat('$ff0Map already added !', self.app.RaceInfos.RefereeLogins)
				self.MapToDeleteAtNextMapStart = None
		elif self.ActualModeID == 4:
			# Course
			await self.instance.mode_manager.set_next_script("Laps")
			await self.app.instance.mode_manager.update_next_settings({'S_FinishTimeout': 800})
			await self.app.instance.mode_manager.update_next_settings({'S_AllowRespawn': False})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpNb': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_WarmUpDuration': 0})
			await self.app.instance.mode_manager.update_next_settings({'S_TimeLimit': 300000})
			await self.app.instance.mode_manager.update_next_settings({'S_ForceLapsNb': self.ActualRaceLapsNb})
			await self.app.instance.mode_manager.update_next_settings({'S_DelayBeforeNextMap': 60})
			for map in self.instance.map_manager.maps:
				if map != self.instance.map_manager.current_map:
					MapsToDelete.append(map)
				else:
					self.MapToDeleteAtNextMapStart = map
			for map in MapsToDelete:
				await self.instance.map_manager.remove_map(map)
			try:
				await self.instance.map_manager.add_map("Downloaded/F1/%s/Course.Map.Gbx" % self.ActualRace, True, False)
			except:
				self.instance.chat('$ff0Map already added !', self.app.RaceInfos.RefereeLogins)
				self.MapToDeleteAtNextMapStart = None
		# print(self.MapToDeleteAtNextMapStart)
		# print(self.instance.map_manager.maps)

		await asyncio.gather(
			self.instance.chat('$ff0Change race mode to %s' % mode_text, self.app.RaceInfos.RefereeLogins),
			self.instance.map_manager.update_list(full_update=True),
			self.app.instance.command_manager.execute(player, '//skip')
		)