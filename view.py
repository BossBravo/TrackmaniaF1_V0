from pyplanet.views import TemplateView
from pyplanet.views.generics.list import ManualListView
from pyplanet.views.generics.widget import TimesWidgetView
from pyplanet.utils import times
import math


class FlagView(TemplateView):
	template_name = 'formula1/flag.xml'
	flag_name = "Default_Flag_Name"
	flag_sound = "Default_Flag_Sound"
	flag_sound_active = 0
	text_1 = "Default_Text_1"
	text_2 = "Default_Text_2"

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'flag'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		context.update({
			'flag_name': self.flag_name,
			'flag_sound': self.flag_sound,
			'flag_sound_active': self.flag_sound_active,
			'text_1': self.text_1,
			'text_2': self.text_2
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class BestLapView(TemplateView):
	template_name = 'formula1/best_lap.xml'
	best_lap_login = "default_login_best_lap"
	best_lap_time = 0

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'flag'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		context.update({
			'best_lap_login': self.best_lap_login,
			'best_lap_time': times.format_time(self.best_lap_time)
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class SoundF1ThemeView(TemplateView):
	template_name = 'formula1/sound_f1_theme.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'sound_f1_theme'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class SoundF1PodiumView(TemplateView):
	template_name = 'formula1/sound_podium.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'sound_f1_podium'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class StartTimingView(TemplateView):
	template_name = 'formula1/start_timing.xml'
	timing_text = "Default_Text"

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'start_timing'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		context.update({
			'timing_text': self.timing_text
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class CacheView(TemplateView):
	template_name = 'formula1/cache.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'cache'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class GaugeView(TemplateView):
	template_name = 'formula1/gauge.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'gauge'
		self.status = 0
		self.meters = 0
		self.checks_since_blackscreen = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		locPercent = int(self.meters / self.app.GaugeFullQuantityMeters * 100)
		if locPercent > 100:
			locPercent = 100
		locMeters = self.meters / 1000
		locRatio = self.meters / self.app.GaugeFullQuantityMeters
		locColor = await self.app.getColorProgressBar(locPercent)
		context.update({
			'color': "%s" % locColor,
			'ratio': "%.2f" % locRatio,
			'percent': "%s" % locPercent,
			'km': "%.2f" % locMeters
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class BlackScreenView(TemplateView):
	template_name = 'formula1/black_screen.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'black_screen'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class SoundAlertLowFuelView(TemplateView):
	template_name = 'formula1/sound_alert_low_fuel.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'sound_alert_low_fuel'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class SoundAlertEndPitStopView(TemplateView):
	template_name = 'formula1/sound_alert_end_pitstop.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'sound_alert_end_pitstop'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class SoundAlertCriticalFuelView(TemplateView):
	template_name = 'formula1/sound_alert_critical_fuel.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'sound_alert_critical_fuel'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value


class BestCpTimesWidget(TimesWidgetView):
	widget_x = -160
	widget_y = 90
	size_x = 38
	size_y = 55.5
	title = 'Best Sectors'

	template_name = 'formula1/widget_top.xml'

	def __init__(self, app, best_cp_times):
		super().__init__(app.context.ui)
		self.app = app
		self.manager = self.app.context.ui
		self.id = 'formula1_widget_bestcps'
		self.logins = []
		self.action = self.action_cptimeslist
		self.best_cp_times = best_cp_times

	async def get_player_data(self):
		self.logins = []
		for pcp in self.best_cp_times:
			self.logins.append(pcp.player.login)
		data = await super().get_all_player_data(self.logins)
		cps = {}
		for idx, player in enumerate(self.app.instance.player_manager.online):
			list_cps = []
			for pcp in self.best_cp_times:
				list_time = {
					'index': pcp.cp,
					'color': "$0f3" if player.login == pcp.player.login else "$ff0",
					'cptime': times.format_time(pcp.time),
					'nickname': pcp.player.nickname,
					'login': pcp.player.login
				}
				list_cps.append(list_time)
			cps[player.login] = {'cps': list_cps}

		data.update(cps)
		return data

	async def action_cptimeslist(self, player, **kwargs):
		view = CpTimesListView(self.app)
		# await view.display(player=player.login)
		return view


class CpTimesListView(ManualListView):
	title = 'Best Sector times in current race'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Statistics'

	fields = [
		{
			'name': '#',
			'index': 'index',
			'sorting': True,
			'searching': False,
			'width': 10,
			'type': 'label'
		},
		{
			'name': 'Player',
			'index': 'player_nickname',
			'sorting': False,
			'searching': True,
			'width': 70
		},
		{
			'name': 'Time',
			'index': 'record_time',
			'sorting': True,
			'searching': False,
			'width': 30,
			'type': 'label'
		},
	]

	def __init__(self, app):
		super().__init__(self)
		self.app = app
		self.manager = app.context.ui
		self.provide_search = False

	async def get_data(self):
		items = []
		list_times = self.best_cp_times
		for pcp in list_times:
			items.append({
				'index': pcp.cp,
				'player_nickname': pcp.player.nickname,
				'record_time': times.format_time(pcp.time)
			})

		return items


class LiveRankingsWidget(TimesWidgetView):
	widget_x = -160
	widget_y = 20
	# widget_y_players = 20
	widget_y_players = 82
	widget_y_referees = 82
	size_x = 48.5
	size_y = 55.5
	top_entries_referee = 5
	top_entries_podium = 5
	top_entries_players = 3
	record_amount_referee = 50
	record_amount_podium = 50
	record_amount_players = 16
	title = 'Race Ranking'
	
	template_name = 'formula1/live_rankings.xml'

	def __init__(self, self_parent, app):
		super().__init__(app.context.ui)
		self.app = app
		self.manager = self.app.context.ui
		self.id = 'formula1_widgets_liverankings'
		self.parent = self_parent
		
		self.format_times = True
		self.display_cpdifference = True
		
		self.subscribe('spectate_player__0', self.spectate_player)
		self.subscribe('spectate_player__1', self.spectate_player)
		self.subscribe('spectate_player__2', self.spectate_player)
		self.subscribe('spectate_player__3', self.spectate_player)
		self.subscribe('spectate_player__4', self.spectate_player)
		self.subscribe('spectate_player__5', self.spectate_player)
		self.subscribe('spectate_player__6', self.spectate_player)
		self.subscribe('spectate_player__7', self.spectate_player)
		self.subscribe('spectate_player__8', self.spectate_player)
		self.subscribe('spectate_player__9', self.spectate_player)
		self.subscribe('spectate_player__10', self.spectate_player)
		self.subscribe('spectate_player__11', self.spectate_player)
		self.subscribe('spectate_player__12', self.spectate_player)
		self.subscribe('spectate_player__13', self.spectate_player)
		self.subscribe('spectate_player__14', self.spectate_player)
		self.subscribe('spectate_player__15', self.spectate_player)
		self.subscribe('spectate_player__16', self.spectate_player)
		self.subscribe('spectate_player__17', self.spectate_player)
		self.subscribe('spectate_player__18', self.spectate_player)
		self.subscribe('spectate_player__19', self.spectate_player)
		self.subscribe('spectate_player__20', self.spectate_player)
		self.subscribe('spectate_player__21', self.spectate_player)
		self.subscribe('spectate_player__22', self.spectate_player)
		self.subscribe('spectate_player__23', self.spectate_player)
		self.subscribe('spectate_player__24', self.spectate_player)
		self.subscribe('spectate_player__25', self.spectate_player)
		self.subscribe('spectate_player__26', self.spectate_player)
		self.subscribe('spectate_player__27', self.spectate_player)
		self.subscribe('spectate_player__28', self.spectate_player)
		self.subscribe('spectate_player__29', self.spectate_player)
		self.subscribe('spectate_player__30', self.spectate_player)
		self.subscribe('spectate_player__31', self.spectate_player)
		self.subscribe('spectate_player__32', self.spectate_player)
		self.subscribe('spectate_player__33', self.spectate_player)
		self.subscribe('spectate_player__34', self.spectate_player)
		self.subscribe('spectate_player__35', self.spectate_player)
		self.subscribe('spectate_player__36', self.spectate_player)
		self.subscribe('spectate_player__37', self.spectate_player)
		self.subscribe('spectate_player__38', self.spectate_player)
		self.subscribe('spectate_player__39', self.spectate_player)
		self.subscribe('spectate_player__40', self.spectate_player)
		self.subscribe('spectate_player__41', self.spectate_player)
		self.subscribe('spectate_player__42', self.spectate_player)
		self.subscribe('spectate_player__43', self.spectate_player)
		self.subscribe('spectate_player__44', self.spectate_player)
		self.subscribe('spectate_player__45', self.spectate_player)
		self.subscribe('spectate_player__46', self.spectate_player)
		self.subscribe('spectate_player__47', self.spectate_player)
		self.subscribe('spectate_player__48', self.spectate_player)
		self.subscribe('spectate_player__49', self.spectate_player)
		self.subscribe('spectate_player__50', self.spectate_player)

	async def spectate_player(self, player, *args, **kwargs):
		index_to_spectate = int(args[0].split('__')[2]) - 1
		records = list(self.parent.current_rankings[:self.record_amount_referee])
		players = self.app.instance.player_manager.online
		if player.login in self.app.RaceInfos.RefereeLogins or player.login in self.app.RaceInfos.StreamerLogins:
			isSpectator = False
			for p in players:
				if p.login == player.login:
					isSpectator = p.flow.is_spectator
					break;
			if player.login == 'boss-bravo':
				print("%s click on %s for spectate (actually spec : %s)" % (player.login,records[index_to_spectate]['login'],isSpectator))
				if(isSpectator == False):
					await self.app.instance.gbx('ForceSpectator', player.login, 1)
				await self.app.instance.gbx('forceSpectatorTarget', player.login, records[index_to_spectate]['login'], 0)
				# print("1")
				# player_object = await self.app.instance.player_manager.get_player(str(player))
				# print(player_object)
				# if not player_object['is_spectator_bool']:
					# await self.app.instance.gbx('ForceSpectator', player, 1)
					# print("20")
				# else:
					# print("21")
				# await self.app.instance.gbx('forceSpectatorTarget', player, records[index_to_spectate]['login'], 0)
				# print("3")

	def get_widget_records(self, player=None):
		list_records = list()
				
		player_index = len(self.parent.current_rankings) + 1
		if player:
			player_record = [x for x in self.parent.current_rankings if x['login'] == player.login]
		else:
			player_record = list()

		if len(player_record) > 0:
			# Set player index if there is a record
			player_index = (self.parent.current_rankings.index(player_record[0]) + 1)
		
		if player.login in self.app.RaceInfos.RefereeLogins or player.login in self.app.RaceInfos.StreamerLogins:
			top_entries = self.top_entries_referee
			record_amount = self.record_amount_referee
			self.widget_y = self.widget_y_referees
		else:
			top_entries = self.top_entries_players
			record_amount = self.record_amount_players
			self.widget_y = self.widget_y_players
		
		records = list(self.parent.current_rankings[:top_entries])
		
		custom_start_index = 0
		# print(len(self.parent.current_rankings))
		# print(player_index)
		# if(player.login == 'boss-bravo'):
			# self.app.F1Logs.log('DEBUG', "player index : %s | len(self.parent.current_rankings) : %s | top_entries : %s" % (player_index, len(self.parent.current_rankings), top_entries), player.login, -1, 'view.py', 'LiveRankingsWidget.get_widget_records')
		if self.app.instance.performance_mode:
			# Performance mode is turned on, get the top of the whole widget.
			records += self.parent.current_rankings[top_entries:record_amount]
			custom_start_index = (top_entries + 1)
		else:
			if player_index > len(self.parent.current_rankings):
				# No personal record, get the last records
				records_start = (len(self.parent.current_rankings) - record_amount + top_entries)
				# If start of current slice is in the top entries, add more records below
				if records_start < top_entries:
					records_start = top_entries
				
				records += list(self.parent.current_rankings[records_start:])
				custom_start_index = (records_start + 1)
			else:
				if player_index <= top_entries:
					# Player record is in top X, get following records (top entries + 1 onwards)
					records += self.parent.current_rankings[top_entries:record_amount]
					custom_start_index = (top_entries + 1)
				else:
					# Player record is not in top X, get records around player record
					# Same amount above the record as below, except when not possible (favors above)
					records_to_fill = (record_amount - top_entries)
					start_point = ((player_index - math.ceil((records_to_fill - 1) / 2)) - 1)
					end_point = ((player_index + math.floor((records_to_fill - 1) / 2)) - 1)
					
					# If end of current slice is outside the list, add more records above
					if end_point > len(self.parent.current_rankings):
						end_difference = (end_point - len(self.parent.current_rankings))
						start_point = (start_point - end_difference)
					# If start of current slice is in the top entries, add more records below
					if start_point < top_entries:
						start_point = top_entries
					
					records += self.parent.current_rankings[start_point:(start_point + records_to_fill)]
					custom_start_index = (start_point + 1)
		
		index = 1
		best = None
		for record in records:
			if self.display_cpdifference and index == 1:
				best = record
			
			list_record = dict()
			list_record['index'] = index
			
			list_record['color'] = '$fff'
			list_record['bgcolor'] = '00000070'
			if index <= top_entries:
				list_record['color'] = '$ff0'
				list_record['bgcolor'] = '00000070'
			if index == player_index:
				# list_record['color'] = '$0f3'
				list_record['bgcolor'] = '00ff3370'
			
			list_record['nickname'] = record['nickname']
			list_record['login'] = record['login']
			
			if list_record['login'] in self.app.FuelGauge.PilotsInPitStop:
				list_record['PitStop'] = 1
			else:
				list_record['PitStop'] = 0
			
			if 'finish' in record:
				if record['finish']:
					list_record['PilotFinished'] = 1
				else:
					list_record['PilotFinished'] = 0
			else:
				list_record['PilotFinished'] = 0
			
			if 'giveup' in record:
				if record['giveup']:
					list_record['PilotGiveUp'] = 1
				else:
					list_record['PilotGiveUp'] = 0
			else:
				list_record['PilotGiveUp'] = 0
				
			list_record['BestLapLogin'] = self.app.RaceInfos.BestLapLogin
			
			if list_record['login'] in self.app.RaceInfos.SpectatorLogins:
				list_record['isSpectator'] = 1
			else:
				list_record['isSpectator'] = 0
			
			if list_record['login'] in self.app.RaceInfos.PlayersPenalties:
				list_record['hasPenalty'] = 1
			else:
				list_record['hasPenalty'] = 0
			
			if self.format_times:
				list_record['score'] = times.format_time(int(record['score']))
			else:
				list_record['score'] = int(record['score'])
			
			list_record['cp_difference'] = None
			list_record['cp_difference_unit'] = "cp"
			
			if self.display_cpdifference and 'cps' in best and 'cps' in record:
				list_record['cp_difference'] = (best['cps'] - record['cps'])
				
				if index > 1 and not record['finish']:
					# Calculate difference to first player
					best_cp = best['cp_times'][(record['cps'] - 1)]
					current_diff = (record['score'] - best['cp_times'][(record['cps'] - 1)])
					list_record['score'] = '+ ' + times.format_time(int(current_diff))
				
				if 'finish' in record:
					if record['finish']:
						list_record['score'] = '$i' + str(list_record['score'])
					elif record['giveup']:
						list_record['score'] = '$iDNF'
				else:
					list_record['score'] = ''
			
			if list_record['cp_difference'] is not None:
				if list_record['cp_difference'] > 14:
					list_record['cp_difference'] = int(list_record['cp_difference']/14)
					if list_record['cp_difference'] > 1:
						list_record['cp_difference_unit'] = "laps"
					else:
						list_record['cp_difference_unit'] = "lap"
			
			if player.login in self.app.RaceInfos.RefereeLogins or player.login in self.app.RaceInfos.StreamerLogins:
				list_record['show_extra_infos'] = 1
			else:
				list_record['show_extra_infos'] = 0
			
			if list_record['login'] in self.app.FuelGauge.MetersGauge:
				list_record['gauge_percent'] = int(self.app.FuelGauge.MetersGauge[list_record['login']] / self.app.FuelGauge.GaugeFullQuantityMeters * 100)
				list_record['gauge_ratio'] = self.app.FuelGauge.MetersGauge[list_record['login']] / self.app.FuelGauge.GaugeFullQuantityMeters
				list_record['gauge_ratio2'] = self.app.FuelGauge.MetersGauge[list_record['login']] / self.app.FuelGauge.GaugeFullQuantityMeters * 12
				locColor = self.app.FuelGauge.getColorProgressBarNotAwait(list_record['gauge_percent'])
				list_record['gauge_color'] = locColor
			else:
				list_record['gauge_percent'] = 0
				list_record['gauge_ratio'] = 0
				list_record['gauge_ratio2'] = 0
				locColor = self.app.FuelGauge.getColorProgressBarNotAwait(0)
				list_record['gauge_color'] = locColor
			
			if list_record['login'] in self.app.FuelGauge.NbPilotsPitStopInRace:
				list_record['nb_times_pitstop'] = self.app.FuelGauge.NbPilotsPitStopInRace[list_record['login']]
			else:
				list_record['nb_times_pitstop'] = 0
			
			if 'finish' in record:
				if record['finish']:
					list_record['gauge_on'] = 1
				elif record['giveup']:
					list_record['gauge_on'] = 0
			else:
				list_record['gauge_on'] = 0
			
			if index == top_entries:
				index = custom_start_index
			else:
				index += 1
			
			list_records.append(list_record)
		return list_records

	async def get_context_data(self):
		current_script = await self.app.instance.mode_manager.get_current_script()
		if 'TimeAttack' in current_script:
			self.format_times = True
			self.display_cpdifference = False
		elif 'Laps' in current_script:
			self.format_times = True
			self.display_cpdifference = True
		else:
			self.format_times = False
			self.display_cpdifference = False
		data = await super().get_context_data()
		if self.app.instance.performance_mode:
			data['times'] = self.get_widget_records()
		return data

	async def get_player_data(self):
		data = await super().get_player_data()

		# If in performance mode, ignore this method.
		if self.app.instance.performance_mode:
			return dict()
		else:
			for player in self.app.instance.player_manager.online:
				data[player.login] = dict(times=self.get_widget_records(player))
			return data


class DiscordLogoView(TemplateView):
	widget_x = 0
	widget_y = 90
	size_x = 50
	size_y = 50
	template_name = 'formula1/discord_logo.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'discord__logo'

	async def get_context_data(self):
		context = await super().get_context_data()
		context.update({
			'discord_url': self.app.discord_join_url
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)


class CheckpointInfoView(TemplateView):
	template_name = 'formula1/checkpoint_infos.xml'

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'formula1__checkpoint_infos'
		self.lap_record = 0
		self.lap_time = ""
		self.lap_gap = ""
		self.checkpoint_time = ""
		self.checkpoint_gap = ""
		self.isFinishLine = False
		self.isLapRecord = False
		self.isMapRecord = False
		self.showGap = False

	async def get_context_data(self):
		context = await super().get_context_data()
		if self.lap_gap > 0 :
			locLapColor = "ff000090"
			locLapGap = "+%s" % times.format_time(self.lap_gap)
		else:
			locLapColor = "00aa0090"
			locLapGap = "-%s" % times.format_time(1 - self.lap_gap)
		if self.checkpoint_gap > 0 and self.lap_record > 0 :
			locCheckpointColor = "ff000090"
			locCheckpointGap = "+%s" % times.format_time(self.checkpoint_gap)
		elif self.lap_record > 0:
			locCheckpointColor = "00aa0090"
			locCheckpointGap = "-%s" % times.format_time(1 - self.checkpoint_gap)
		else:
			locCheckpointColor = "00aa0090"
			locCheckpointGap = "-%s" % times.format_time(self.checkpoint_gap)
		# print("Map Record : %s" % times.format_time(self.app.map_record))
		# print("Lap Record : %s" % times.format_time(self.lap_record))
		# print("Lap Time : %s" % times.format_time(self.lap_time))
		# print("Is Finish Line : %s" % self.isFinishLine)
		# print("------")
		if self.isFinishLine == True and self.lap_record == 0:
			self.lap_record = self.lap_time
			self.isLapRecord = True
		elif self.isFinishLine == True and self.lap_record > self.lap_time:
			self.lap_record = self.lap_time
			self.isLapRecord = True
			# print("Lap Record")
			if self.lap_time < self.app.map_record:
				self.isMapRecord = True
				# print("Map Record")
		else:
			self.isLapRecord = False
			self.isMapRecord = False
		if self.lap_record > 0:
			self.showGap = True
		else:
			self.showGap = False
		context.update({
			'lap_time': times.format_time(self.lap_time),
			'lap_record': times.format_time(self.lap_record),
			'lap_gap': locLapGap,
			'lap_color': locLapColor,
			'checkpoint_time': times.format_time(self.checkpoint_time),
			'checkpoint_gap': locCheckpointGap,
			'checkpoint_color': locCheckpointColor,
			'isFinishLine': self.isFinishLine,
			'isLapRecord': self.isLapRecord,
			'isMapRecord': self.isMapRecord,
			'showGap': self.showGap
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)


class MeteoView(TemplateView):
	template_name = 'formula1/meteo.xml'
	meteo_name = "Default_Meteo_Name"
	meteo_sound = "Default_Meteo_Sound"
	meteo_sound_active = 0
	meteo_image = 1
	meteo_video = 1
	grey_background = 1
	grey_background_color_value = "00000077"

	def __init__(self, app, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.app = app
		self.id = 'meteo'
		self.status = 0

	async def get_context_data(self):
		context = await super().get_context_data()
		context.update({
			'meteo_name': self.meteo_name,
			'meteo_sound': self.meteo_sound,
			'meteo_sound_active': self.meteo_sound_active,
			'meteo_image': self.meteo_image,
			'meteo_video': self.meteo_video,
			'grey_background': self.grey_background,
			'grey_background_color_value': self.grey_background_color_value
		})
		return context

	async def display(self, **kwargs):
		return await super().display(**kwargs)

	async def getstatus(self):
		return self.status

	async def setstatus(self, value):
		self.status = value
