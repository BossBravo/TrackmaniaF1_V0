from pyplanet.views import TemplateView
from pyplanet.apps.contrib.formula1.views.players import PlayerListView
from pyplanet.apps.contrib.formula1.views.meteo import MeteoAdminView
from pyplanet.apps.contrib.formula1.views.checklist import ChecklistView
from pyplanet.apps.contrib.formula1.views.maplist import MaplistView

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

import asyncio, time

from pyplanet.apps.contrib.formula1.view import FlagView
from pyplanet.apps.contrib.formula1.view import SoundF1ThemeView
from pyplanet.apps.contrib.formula1.view import SoundF1PodiumView
from pyplanet.apps.contrib.formula1.view import StartTimingView
from pyplanet.apps.contrib.formula1.view import CacheView


class ToolbarView(TemplateView):
	template_name = 'formula1/toolbar.xml'

	def __init__(self, app):
		super().__init__(app.context.ui)

		self.app = app
		self.id = 'race_control_toolbar'

		self.subscribe('bar_yellow_flag', self.yellow_flag)
		self.subscribe('bar_red_flag', self.red_flag)
		self.subscribe('bar_black_flag', self.player_list)
		self.subscribe('bar_final_flag', self.final_flag)
		self.subscribe('bar_safety_car', self.safety_car)
		self.subscribe('bar_start_procedure', self.start_procedure)
		self.subscribe('bar_set_cache', self.set_cache)
		self.subscribe('bar_meteo', self.meteo)
		self.subscribe('bar_checklist', self.checklist)
		self.subscribe('bar_maplist', self.maplist)
		
		self.flag_view = FlagView(self, manager=app.context.ui)
		self.sound_f1_theme_view = SoundF1ThemeView(self, manager=app.context.ui)
		self.sound_f1_podium_view = SoundF1PodiumView(self, manager=app.context.ui)
		self.start_timing_view = StartTimingView(self, manager=app.context.ui)
		self.cache_view = CacheView(self, manager=app.context.ui)
		
		self.StartProcedureLaunched = 0
		self.SafetyCarStatus = 0
		self.YellowFlagStatus = 0
		self.RaceRankingStartYellowFlag = {}
		
		self.ObjectsSafetyCarPlayers = {}
		
		self.app.context.signals.listen(mp_signals.flow.podium_start, self.podium_start)
		self.app.context.signals.listen(mp_signals.map.map_end, self.map_end)
		self.app.context.signals.listen(tm_signals.waypoint, self.new_checkpoint_safety_car)
		self.app.context.signals.listen(tm_signals.finish, self.new_checkpoint_safety_car)

	async def podium_start(self, *args, **kwargs):
		await self.flag_view.hide()
		await self.flag_view.setstatus(0)
		await self.sound_f1_theme_view.hide()
		if self.app.RaceManagement.ActualModeID == 0 or self.app.RaceManagement.ActualModeID == 4:
			await self.sound_f1_podium_view.display(player_logins=None)
		await self.start_timing_view.hide()
		status_cache = await self.cache_view.getstatus()
		await self.cache_view.hide()
		if status_cache == 1:
			await self.cache_view.setstatus(0)

	async def map_end(self, *args, **kwargs):
		await self.sound_f1_podium_view.hide()

	async def get_context_data(self):
		data = await super().get_context_data()
		data['game'] = self.app.instance.game.game
		return data

	async def yellow_flag(self, player, *args, **kwargs):
		status = await self.flag_view.getstatus()
		logins = None
		if status == 0:
			i = 0
			self.RaceRankingStartYellowFlag = {}
			for rank_player in self.app.RaceRanking.current_rankings:
				i += 1
				self.RaceRankingStartYellowFlag[i] = rank_player['login']
			self.flag_view.flag_sound_active = 1
			self.flag_view.flag_sound = "YellowFlag_NoOvertake"
			self.flag_view.flag_name = "yellow_flag"
			self.flag_view.text_1 = "$s$fc0Yellow Flag !"
			self.flag_view.text_2 = ""
			await self.flag_view.display(player_logins=logins)
			await self.flag_view.setstatus(1)
			self.YellowFlagStatus = 1
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|[]|%s|[]|YELLOW_FLAG|[]|ON" % (LapNb,))
		else:
			self.flag_view.flag_sound_active = 1
			self.flag_view.flag_sound = "GreenFlag"
			self.flag_view.flag_name = "green_flag"
			self.flag_view.text_1 = "$s$0a0Green flag, race is on !"
			self.flag_view.text_2 = ""
			await self.flag_view.setstatus(1)
			await self.flag_view.display(player_logins=logins)
			await asyncio.sleep(5)
			await self.flag_view.hide()
			await self.flag_view.setstatus(0)
			self.YellowFlagStatus = 0
			self.RaceRankingStartYellowFlag = {}
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|[]|%s|[]|YELLOW_FLAG|[]|OFF" % (LapNb,))

	async def red_flag(self, player, *args, **kwargs):
		status = await self.flag_view.getstatus()
		logins = None
		if status == 0:
			self.flag_view.flag_sound_active = 0
			self.flag_view.flag_name = "red_flag"
			self.flag_view.text_1 = "$s$d00Red Flag !"
			self.flag_view.text_2 = ""
			await self.flag_view.display(player_logins=logins)
			await self.flag_view.setstatus(1)
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|[]|%s|[]|RED_FLAG|[]|ON" % (LapNb,))
		else:
			await self.flag_view.hide()
			await self.flag_view.setstatus(0)
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|[]|%s|[]|RED_FLAG|[]|OFF" % (LapNb,))

	async def final_flag(self, player = None, *args, **kwargs):
		status = await self.flag_view.getstatus()
		logins = None
		if status == 0:
			First_NickName = self.app.RaceRanking.current_rankings[0]["nickname"]
			self.flag_view.flag_sound_active = 0
			self.flag_view.flag_name = "final_flag"
			self.flag_view.text_1 = "%s$g$z$s$3FC arrived first !" % First_NickName
			self.flag_view.text_2 = ""
			await self.flag_view.display(player_logins=logins)
			await self.flag_view.setstatus(1)
		else:
			await self.flag_view.hide()
			await self.flag_view.setstatus(0)

	async def player_list(self, player, *args, **kwargs):
		view = PlayerListView(self.app, player)
		await view.display()

	async def meteo(self, player, *args, **kwargs):
		view = MeteoAdminView(self.app, player)
		await view.display()
	
	async def checklist(self, player, *args, **kwargs):
		view = ChecklistView(self.app, player)
		await view.display()
	
	async def maplist(self, player, *args, **kwargs):
		view = MaplistView(self.app, player)
		await view.display()

	async def safety_car(self, player, *args, **kwargs):
		if len(self.app.RaceRanking.current_rankings) > 0:
			cps_first_pilot = self.app.RaceRanking.current_rankings[0]['cps']
		else:
			cps_first_pilot = 0
		if self.SafetyCarStatus == 0:
			i = 0
			self.RaceRankingStartYellowFlag = {}
			for rank_player in self.app.RaceRanking.current_rankings:
				i += 1
				self.RaceRankingStartYellowFlag[i] = rank_player['login']
			players = self.app.instance.player_manager.online
			for p in players:
				if not p.login in self.ObjectsSafetyCarPlayers:
					self.ObjectsSafetyCarPlayers[p.login] = FlagView(self, manager=self.app.context.ui)
				self.ObjectsSafetyCarPlayers[p.login].flag_sound_active = 1
				
				player_rank = self.app.RaceRanking.player_find_ranking(p.login)
				if player_rank['rank'] > 0:
					if cps_first_pilot - 14 >= player_rank['data']['cps'] :
						self.ObjectsSafetyCarPlayers[p.login].flag_sound = "SafetyCar_OvertakeOK"
						await self.ObjectsSafetyCarPlayers[p.login].setstatus(1)
						# print("%s Safety Car Overtake OK" % p.login)
					else:
						self.ObjectsSafetyCarPlayers[p.login].flag_sound = "SafetyCar_DoNotOvertake"
						await self.ObjectsSafetyCarPlayers[p.login].setstatus(0)
						# print("%s Safety Car Overtake NOK" % p.login)
				else:
					if cps_first_pilot >= 14:
						self.ObjectsSafetyCarPlayers[p.login].flag_sound = "SafetyCar_OvertakeOK"
						await self.ObjectsSafetyCarPlayers[p.login].setstatus(1)
						# print("%s Safety Car Overtake OK" % p.login)
					else:
						self.ObjectsSafetyCarPlayers[p.login].flag_sound = "SafetyCar_DoNotOvertake"
						await self.ObjectsSafetyCarPlayers[p.login].setstatus(0)
						# print("%s Safety Car Overtake NOK" % p.login)
				
				self.ObjectsSafetyCarPlayers[p.login].flag_name = "safety_car_flag"
				self.ObjectsSafetyCarPlayers[p.login].text_1 = "$s$fc0Yellow Flag !"
				self.ObjectsSafetyCarPlayers[p.login].text_2 = "$s$fc0SAFETY CAR !"
				await self.ObjectsSafetyCarPlayers[p.login].display(player_logins=[p.login])
				self.SafetyCarStatus = 1
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|SAFETY_CAR|ON|%s" % (LapNb,))
		elif self.SafetyCarStatus == 1:
			players = self.app.instance.player_manager.online
			for p in players:
				if not p.login in self.ObjectsSafetyCarPlayers:
					self.ObjectsSafetyCarPlayers[p.login] = FlagView(self, manager=self.app.context.ui)
				self.ObjectsSafetyCarPlayers[p.login].flag_sound_active = 1
				self.ObjectsSafetyCarPlayers[p.login].flag_sound = "SafetyCar_OffThisLap"
				self.ObjectsSafetyCarPlayers[p.login].flag_name = "safety_car_flag"
				self.ObjectsSafetyCarPlayers[p.login].text_1 = "$s$fc0Yellow Flag !"
				self.ObjectsSafetyCarPlayers[p.login].text_2 = "$s$0a0Safety car off on this lap !"
				await self.ObjectsSafetyCarPlayers[p.login].setstatus(0)
				await self.ObjectsSafetyCarPlayers[p.login].display(player_logins=[p.login])
				self.SafetyCarStatus = 2
		else:
			players = self.app.instance.player_manager.online
			for p in players:
				if not p.login in self.ObjectsSafetyCarPlayers:
					self.ObjectsSafetyCarPlayers[p.login] = FlagView(self, manager=self.app.context.ui)
				self.ObjectsSafetyCarPlayers[p.login].flag_sound_active = 1
				self.ObjectsSafetyCarPlayers[p.login].flag_sound = "GreenFlag"
				self.ObjectsSafetyCarPlayers[p.login].flag_name = "green_flag"
				self.ObjectsSafetyCarPlayers[p.login].text_1 = "$s$0a0Green flag, race is on !"
				self.ObjectsSafetyCarPlayers[p.login].text_2 = ""
				await self.ObjectsSafetyCarPlayers[p.login].setstatus(0)
				await self.ObjectsSafetyCarPlayers[p.login].display(player_logins=[p.login])
				self.SafetyCarStatus = 3
			await asyncio.sleep(5)
			for p in players:
				await self.ObjectsSafetyCarPlayers[p.login].hide(player_logins=[p.login])
			self.SafetyCarStatus = 0
			self.ObjectsSafetyCarPlayers = {}
			self.RaceRankingStartYellowFlag = {}
			if(self.app.RaceManagement.ActualModeID == 4):
				LapNb = int(self.app.RaceRanking.current_rankings[0]['cps'] / (self.app.FuelGauge.FirstCheckPointNumberPitStop + 3)) + 1
				self.app.F1Logs.log_data("RACE|SAFETY_CAR|OFF|%s" % (LapNb,))
	
	
	async def new_checkpoint_safety_car(self, raw, *args, **kwargs):
		if self.SafetyCarStatus > 0:
			if raw['login'] in self.ObjectsSafetyCarPlayers:
				if await self.ObjectsSafetyCarPlayers[raw['login']].getstatus() == 1:
					if len(self.app.RaceRanking.current_rankings) > 0:
						cps_first_pilot = self.app.RaceRanking.current_rankings[0]['cps']
					else:
						cps_first_pilot = 0
					player_rank = self.app.RaceRanking.player_find_ranking(raw['login'])
					if player_rank['rank'] > 0:
						if cps_first_pilot - 14 < player_rank['data']['cps'] :
							self.ObjectsSafetyCarPlayers[raw['login']].flag_sound = "SafetyCar_StayBehindNoOvertake"
							await self.ObjectsSafetyCarPlayers[raw['login']].setstatus(0)
							# print("%s Safety Car Overtake NOK" % raw['login'])
							await self.ObjectsSafetyCarPlayers[raw['login']].display(player_logins=[raw['login']])
					else:
						if cps_first_pilot < 14:
							self.ObjectsSafetyCarPlayers[raw['login']].flag_sound = "SafetyCar_StayBehindNoOvertake"
							await self.ObjectsSafetyCarPlayers[raw['login']].setstatus(0)
							# print("%s Safety Car Overtake NOK" % raw['login'])
							await self.ObjectsSafetyCarPlayers[raw['login']].display(player_logins=[raw['login']])

					
	async def start_procedure(self, player=None, *args, **kwargs):
		print("Start Launch procedure")
		if self.StartProcedureLaunched == 0:
			self.StartProcedureLaunched = 1
			start_time = time.time()
			print("--- %s seconds ---" % (time.time() - start_time))
			# F1 theme duration : 5min 22s
			await self.sound_f1_theme_view.display(player_logins=None)
			self.start_timing_view.timing_text = "Start in 5 mins"
			await self.start_timing_view.display(player_logins=None)
			await asyncio.sleep(22)
			print("--- %s seconds ---" % (time.time() - start_time))
			self.start_timing_view.timing_text = "Start in 5 mins"
			await self.start_timing_view.display(player_logins=None)
			await asyncio.sleep(60)
			print("--- %s seconds ---" % (time.time() - start_time))
			self.start_timing_view.timing_text = "Start in 4 mins"
			await self.start_timing_view.display(player_logins=None)
			await asyncio.sleep(60)
			print("--- %s seconds ---" % (time.time() - start_time))
			if self.StartProcedureLaunched == 1:
				self.start_timing_view.timing_text = "Start in 3 mins"
				await self.start_timing_view.display(player_logins=None)
				await asyncio.sleep(60)
				print("--- %s seconds ---" % (time.time() - start_time))
				if self.StartProcedureLaunched == 1:
					self.start_timing_view.timing_text = "Start in 2 mins"
					await self.start_timing_view.display(player_logins=None)
					await asyncio.sleep(60)
					print("--- %s seconds ---" % (time.time() - start_time))
					if self.StartProcedureLaunched == 1:
						for i in range (0,61):
							seconds_remaining = 60 - i
							if i < 60:
								self.start_timing_view.timing_text = "Start in %s seconds" % (seconds_remaining,)
							else:
								self.start_timing_view.timing_text = "GO !"
							await self.start_timing_view.display(player_logins=None)
							await asyncio.sleep(1)
							i += 1
						print("--- %s seconds ---" % (time.time() - start_time))
						await asyncio.sleep(2)
						print("--- %s seconds ---" % (time.time() - start_time))
						await self.start_timing_view.hide(player_logins=None)
						await self.sound_f1_theme_view.hide(player_logins=None)
						self.StartProcedureLaunched = 0

	async def set_cache(self, player, *args, **kwargs):
		status = await self.cache_view.getstatus()
		logins = None
		if status == 0:
			await self.cache_view.display(player_logins=logins)
			await self.cache_view.setstatus(1)
			await self.app.instance.chat('$o$s$3fcCache mode active !', player.login)
		else:
			await self.cache_view.hide()
			await self.cache_view.setstatus(0)
			await self.app.instance.chat('$o$s$3fcCache mode inactive !', player.login)