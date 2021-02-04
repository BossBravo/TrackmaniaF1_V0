from pyplanet.apps.contrib.formula1.views.toolbar import ToolbarView

from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals

from pyplanet.apps.contrib.formula1.view import GaugeView
from pyplanet.apps.contrib.formula1.view import BlackScreenView
from pyplanet.apps.contrib.formula1.view import SoundAlertLowFuelView
from pyplanet.apps.contrib.formula1.view import SoundAlertCriticalFuelView
from pyplanet.apps.contrib.formula1.view import SoundAlertEndPitStopView

from random import *
import asyncio

class Formula1GaugeApp:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet']

	GaugeFullQuantityMeters = 60000 # meters
	GaugePitStopPercentInOneSecond = 5 # %/s
	LoopValueRefreshPitStop = 250 #ms
	FirstCheckPointNumberPitStop = 11 # Start/Finish doesn't count, first checkpoint is n°0 | The 2 PitStop Checkpoints must be the last before the finish line !
	MaxSpeedInPitStop = 130 # km/h
	AlertPercent = 20 # Sound alert when fuel under x%
	CriticalPercent = 5 # Sound critical alert when fuel under x%
	MinLapBeforePitStopActivation = 1 # if = 1, PitStop will be activated at start of lap 2 (enf of lap 1 will not working)

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		
		self.view = ToolbarView(self.app)
		
		self.id = 'formula1_gauge'
		
		self.black_screen_view = BlackScreenView(self, manager=self.app.context.ui)
		self.sound_alert_low_fuel_view = SoundAlertLowFuelView(self, manager=self.app.context.ui)
		self.sound_alert_critical_fuel_view = SoundAlertCriticalFuelView(self, manager=self.app.context.ui)
		self.sound_alert_end_pitstop_view = SoundAlertEndPitStopView(self, manager=self.app.context.ui)
		
		self.MetersGauge = {}
		self.ObjectsGauge = {}
		self.PitStopGained = {}
		self.AlertedGauge = {}
		self.CriticalAlertedGauge = {}
		self.MetersStartPitStop = {}
		self.PitStopOpenedPilotsAlerted = []
		self.PilotsInPitStop = []
		self.NbPilotsPitStopInRace = {}

	async def on_start(self):
		
		players = self.instance.player_manager.online
		
		for p in players:
			if not p.login in self.MetersGauge:
				self.MetersGauge[p.login] = self.GaugeFullQuantityMeters
			if not p.login in self.ObjectsGauge:
				self.ObjectsGauge[p.login] = GaugeView(self, manager=self.app.context.ui)
				self.ObjectsGauge[p.login].meters = self.MetersGauge[p.login]
				await self.ObjectsGauge[p.login].display(player_logins=[p.login])
				
		await self.black_screen_view.hide(player_logins=None)
		
		self.app.context.signals.listen(tm_signals.start_countdown, self.start_countdown)
		self.app.context.signals.listen(tm_signals.waypoint, self.new_checkpoint)
		self.app.context.signals.listen(tm_signals.finish, self.new_checkpoint)
		self.app.context.signals.listen(tm_signals.give_up, self.reset_gauge_player)
		self.app.context.signals.listen(mp_signals.flow.podium_start, self.podium_start)
		self.app.context.signals.listen(mp_signals.player.player_connect, self.on_connect)
		self.app.context.signals.listen(mp_signals.player.player_info_changed, self.player_info_changed)
		# print("Gauges on start : %s" % self.MetersGauge)

	async def player_info_changed(self, player_login, is_spectator, *args, **kwargs):
		if player_login in self.ObjectsGauge:
			if is_spectator == True:
				await self.ObjectsGauge[player_login].hide(player_logins=[player_login])
			else:
				await self.ObjectsGauge[player_login].display(player_logins=[player_login])

	async def on_connect(self, player, *args, **kwargs):
		if not player.login in self.MetersGauge:
			self.MetersGauge[player.login] = self.GaugeFullQuantityMeters
		if not player.login in self.ObjectsGauge:
			self.ObjectsGauge[player.login] = GaugeView(self, manager=self.app.context.ui)
			self.ObjectsGauge[player.login].meters = self.MetersGauge[player.login]
			await self.ObjectsGauge[player.login].display(player_logins=[player.login])

	async def chargeServer(self, login, *args, **kwargs):
		if not login in self.MetersGauge:
			self.MetersGauge[login] = self.GaugeFullQuantityMeters
		if not login in self.ObjectsGauge:
			self.ObjectsGauge[login] = GaugeView(self, manager=self.app.context.ui)
			self.ObjectsGauge[login].meters = self.MetersGauge[login]
			await self.ObjectsGauge[login].display(player_logins=[login])

	async def podium_start(self, *args, **kwargs):
		for login in self.ObjectsGauge:
			await self.ObjectsGauge[login].hide(player_logins=[login])
		await self.black_screen_view.hide(player_logins=None)
		self.MetersGauge = {}
		self.ObjectsGauge = {}
		self.PitStopGained = {}
		self.AlertedGauge = {}
		self.CriticalAlertedGauge = {}
		self.MetersStartPitStop = {}
		self.PitStopOpenedPilotsAlerted = []
		self.PilotsInPitStop = []
		self.NbPilotsPitStopInRace = {}
	
	async def new_checkpoint(self, raw, *args, **kwargs):
		LapNb = int(raw['checkpointinrace'] / (self.FirstCheckPointNumberPitStop + 3)) + 1
		if not raw['login'] in self.PitStopGained :
			self.PitStopGained[raw['login']] = 0
		PitStopOpened = 1
		if ((self.FirstCheckPointNumberPitStop + 2) * self.MinLapBeforePitStopActivation) > raw['checkpointinrace']:
			PitStopOpened = 0
		if PitStopOpened == 1 and raw['login'] not in self.PitStopOpenedPilotsAlerted:
			self.PitStopOpenedPilotsAlerted.append(raw['login'])
			await self.instance.chat('$o$s$0a0Pit stop is now open !' , raw['login'])
		if raw['checkpointinlap'] == self.FirstCheckPointNumberPitStop and raw['speed'] <= self.MaxSpeedInPitStop:
			if PitStopOpened == 1:
				self.app.F1Logs.log('INFO', "player is in pitstop mode (Gauge Meters : %sm | Speed : %skm/h)" % (int(self.MetersGauge[raw['login']]), raw['speed']), raw['login'], LapNb, 'gauge.py', 'new_checkpoint')
				if(self.app.RaceManagement.ActualModeID == 4):
					self.app.F1Logs.log_data("RACE|[]|%s|[]|PITSTOP_IN|[]|%s|[]|%s|[]|%s" % (LapNb, raw['login'], int(self.MetersGauge[raw['login']]), raw['speed']))
				if not raw['login'] in self.PilotsInPitStop:
					self.PilotsInPitStop.append(raw['login'])
				if not raw['login'] in self.NbPilotsPitStopInRace:
					self.NbPilotsPitStopInRace[raw['login']] = 1
				else:
					self.NbPilotsPitStopInRace[raw['login']] += 1
				await self.update_gauge(raw['login'], raw['distance'])
				await self.filling_gauge(raw['login'], raw['distance'])
				await self.sound_alert_low_fuel_view.hide(player_logins=[raw['login']])
				await self.sound_alert_critical_fuel_view.hide(player_logins=[raw['login']])
				await self.sound_alert_end_pitstop_view.display(player_logins=[raw['login']])
			else:
				tempValue = self.MinLapBeforePitStopActivation + 1
				await self.instance.chat('$o$s$a00Pit stop closed until lap %s' % (tempValue,) , raw['login'])
		elif raw['checkpointinlap'] == (self.FirstCheckPointNumberPitStop + 1) and raw['speed'] <= self.MaxSpeedInPitStop and PitStopOpened == 1:
			if raw['login'] in self.PilotsInPitStop:
				self.app.F1Logs.log('INFO', "player is out of pitstop mode (Gauge Meters : %sm | Speed : %skm/h)" % (int(self.MetersGauge[raw['login']]), raw['speed']), raw['login'], LapNb, 'gauge.py', 'new_checkpoint')
				if(self.app.RaceManagement.ActualModeID == 4):
					self.app.F1Logs.log_data("RACE|[]|%s|[]|PITSTOP_OUT|[]|%s|[]|%s|[]|%s" % (LapNb, raw['login'], int(self.MetersGauge[raw['login']]), raw['speed']))
				if raw['login'] in self.PilotsInPitStop:
					self.PilotsInPitStop.remove(raw['login'])
		else:
			await self.update_gauge(raw['login'], raw['distance'])
		if self.MetersGauge[raw['login']] < 1 :
			self.ObjectsGauge[raw['login']].checks_since_blackscreen += 1
		if self.ObjectsGauge[raw['login']].checks_since_blackscreen > 2:
			for RefereeLogin in self.app.RaceInfos.RefereeLogins:
				await self.app.instance.chat('$o$s$C40Black screen cheater detected ! => %s' % raw['login'], RefereeLogin)
				self.app.F1Logs.log('WARNING', "cheater player detected (black screen)", raw['login'], file='gauge.py', function='new_checkpoint')
			
		# print(self.PitStopGained)
		# print("Gauges on checkpoint : %s" % self.MetersGauge)
		# print(raw)

	async def update_gauge(self, login, distance, *args, **kwargs):
		Meters = (self.GaugeFullQuantityMeters - distance + self.PitStopGained[login])
		if Meters < 0:
			Meters = 0
			if not login in self.PilotsInPitStop:
				await self.black_screen_view.display(player_logins=[login])
		else:
			await self.black_screen_view.hide(player_logins=[login])
		if (((Meters) < (self.AlertPercent / 100 * self.GaugeFullQuantityMeters)) and not login in self.AlertedGauge and not login in self.PilotsInPitStop) :
			self.AlertedGauge[login] = 1
			await self.sound_alert_low_fuel_view.display(player_logins=[login])
		else:
			if ((Meters >= (self.AlertPercent / 100 * self.GaugeFullQuantityMeters)) and login in self.AlertedGauge):
				del self.AlertedGauge[login]
		if (((Meters) < (self.CriticalPercent / 100 * self.GaugeFullQuantityMeters)) and not login in self.CriticalAlertedGauge and not login in self.PilotsInPitStop) :
			self.CriticalAlertedGauge[login] = 1
			await self.sound_alert_critical_fuel_view.display(player_logins=[login])
		else:
			if ((Meters >= (self.CriticalPercent / 100 * self.GaugeFullQuantityMeters)) and login in self.CriticalAlertedGauge):
				del self.CriticalAlertedGauge[login]
		self.MetersGauge[login] = Meters
		self.ObjectsGauge[login].meters = self.MetersGauge[login]
		# await self.ObjectsGauge[login].hide(player_logins=[login])
		await self.ObjectsGauge[login].display(player_logins=[login])

	async def start_countdown(self, player, *args, **kwargs):
		if not player.login in self.MetersGauge:
			self.MetersGauge[player.login] = self.GaugeFullQuantityMeters
		if not player.login in self.ObjectsGauge:
			self.ObjectsGauge[player.login] = GaugeView(self, manager=self.app.context.ui)
		if not player.login in self.PitStopGained :
			self.PitStopGained[player.login] = 0
		self.PitStopGained[player.login] = 0
		self.ObjectsGauge[player.login].meters = self.MetersGauge[player.login]
		await self.ObjectsGauge[player.login].hide(player_logins=[player.login])
		await self.ObjectsGauge[player.login].display(player_logins=[player.login])

	async def reset_gauge_player(self, player, *args, **kwargs):
		self.ObjectsGauge[player.login].meters = self.MetersGauge[player.login]
		await self.ObjectsGauge[player.login].hide(player_logins=[player.login])
		await self.ObjectsGauge[player.login].display(player_logins=[player.login])
		await self.black_screen_view.hide(player_logins=[player.login])
		await self.sound_alert_low_fuel_view.hide(player_logins=[player.login])
		await self.sound_alert_critical_fuel_view.hide(player_logins=[player.login])

	async def filling_gauge(self, login, distance):
		# print("%s begin pit" % (login,))
		self.MetersStartPitStop[login] = self.PitStopGained[login]
		meters_max_pit_stop = self.GaugeFullQuantityMeters - float(self.MetersGauge[login])
		while (float(self.MetersGauge[login])) < self.GaugeFullQuantityMeters:
			await asyncio.sleep(self.LoopValueRefreshPitStop / 1000)
			if not login in self.PilotsInPitStop:
				break
			self.PitStopGained[login] += self.LoopValueRefreshPitStop / 1000 * self.GaugePitStopPercentInOneSecond / 100 * self.GaugeFullQuantityMeters
			if (self.PitStopGained[login] - self.MetersStartPitStop[login]) >= meters_max_pit_stop:
				self.PitStopGained[login] = self.MetersStartPitStop[login] + meters_max_pit_stop
			await self.update_gauge(login, distance)
		if login in self.PilotsInPitStop:
			await self.sound_alert_end_pitstop_view.display(player_logins=[login])
		# print("%s gain cet arrêt : %s" % (login, self.PitStopGained[login] - self.MetersStartPitStop[login]))
		# print("%s gain total stands : %s" % (login, self.PitStopGained[login]))


	async def get_pilots_in_pitstop(self):
		return self.PilotsInPitStop

	async def getColorProgressBar(self, Percent):
		if Percent > 97:
			color = '0f0'
		elif Percent > 94:
			color = '1f0'
		elif Percent > 91:
			color = '2f0'
		elif Percent > 88:
			color = '3f0'
		elif Percent > 85:
			color = '4f0'
		elif Percent > 82:
			color = '5f0'
		elif Percent > 79:
			color = '6f0'
		elif Percent > 76:
			color = '7f0'
		elif Percent > 73:
			color = '8f0'
		elif Percent > 70:
			color = '9f0'
		elif Percent > 67:
			color = 'af0'
		elif Percent > 63:
			color = 'bf0'
		elif Percent > 60:
			color = 'cf0'
		elif Percent > 57:
			color = 'df0'
		elif Percent > 53:
			color = 'ef0'
		elif Percent > 50:
			color = 'ff0'
		elif Percent > 47:
			color = 'ff0'
		elif Percent > 44:
			color = 'fe0'
		elif Percent > 40:
			color = 'fd0'
		elif Percent > 37:
			color = 'fc0'
		elif Percent > 33:
			color = 'fb0'
		elif Percent > 30:
			color = 'fa0'
		elif Percent > 27:
			color = 'f90'
		elif Percent > 24:
			color = 'f80'
		elif Percent > 20:
			color = 'f70'
		elif Percent > 17:
			color = 'f60'
		elif Percent > 14:
			color = 'f50'
		elif Percent > 11:
			color = 'f40'
		elif Percent > 8:
			color = 'f30'
		elif Percent > 5:
			color = 'f20'
		elif Percent > 2:
			color = 'f10'
		elif Percent > 0:
			color = 'f00'
		else:
			color = 'f00'
		return color

	def getColorProgressBarNotAwait(self, Percent):
		if Percent > 97:
			color = '0f0'
		elif Percent > 94:
			color = '1f0'
		elif Percent > 91:
			color = '2f0'
		elif Percent > 88:
			color = '3f0'
		elif Percent > 85:
			color = '4f0'
		elif Percent > 82:
			color = '5f0'
		elif Percent > 79:
			color = '6f0'
		elif Percent > 76:
			color = '7f0'
		elif Percent > 73:
			color = '8f0'
		elif Percent > 70:
			color = '9f0'
		elif Percent > 67:
			color = 'af0'
		elif Percent > 63:
			color = 'bf0'
		elif Percent > 60:
			color = 'cf0'
		elif Percent > 57:
			color = 'df0'
		elif Percent > 53:
			color = 'ef0'
		elif Percent > 50:
			color = 'ff0'
		elif Percent > 47:
			color = 'ff0'
		elif Percent > 44:
			color = 'fe0'
		elif Percent > 40:
			color = 'fd0'
		elif Percent > 37:
			color = 'fc0'
		elif Percent > 33:
			color = 'fb0'
		elif Percent > 30:
			color = 'fa0'
		elif Percent > 27:
			color = 'f90'
		elif Percent > 24:
			color = 'f80'
		elif Percent > 20:
			color = 'f70'
		elif Percent > 17:
			color = 'f60'
		elif Percent > 14:
			color = 'f50'
		elif Percent > 11:
			color = 'f40'
		elif Percent > 8:
			color = 'f30'
		elif Percent > 5:
			color = 'f20'
		elif Percent > 2:
			color = 'f10'
		elif Percent > 0:
			color = 'f00'
		else:
			color = 'f00'
		return color