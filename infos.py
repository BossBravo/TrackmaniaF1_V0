from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

class Formula1Infos:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.NbLapsTotal = 0
		self.BestLapLogin = ''
		self.BestLapTime = 0
		self.RefereeLogins = ['boss-bravo', 'eti1705', 'x-ryuuzakii', 'sums41', 'Bae_The_Egirl', 'lu0cky', 'xyromad', 'pingendam', 'quaker299', 'donoddo', 'luffysama93']
		self.StreamerLogins = ['sums41', 'donoddo', 'boss-bravo']
		self.SpectatorLogins = []
		self.PlayersPenalties = []
		self.RaceInfosType = 1 # 0 = Only Spectator | 1 = Spectator + Referee  | 2 = Only Referee and not streamer | 3 = All

	async def on_start(self):
		self.app.context.signals.listen(mp_signals.map.map_begin, self.map_begin)
		self.app.context.signals.listen(tm_signals.finish, self.player_waypoint_finish)
		await self.update_total_laps()

	async def map_begin(self, *args, **kwargs):
		self.NbLapsTotal = 0
		self.BestLapLogin = ''
		self.BestLapTime = 0
		await self.update_total_laps()

	async def player_waypoint_finish(self, raw, *args, **kwargs):
		if raw['isendlap'] == True:
			if raw['laptime'] < self.BestLapTime or self.BestLapTime == 0:
				self.BestLapTime = raw['laptime']
				self.BestLapLogin = raw['login']

	async def update_total_laps(self):
		mode_info = await self.instance.mode_manager.get_current_script_info()
		for line in mode_info['ParamDescs']:
			if line['Name'] == 'S_ForceLapsNb':
				self.NbLapsTotal = line['Default']
				break