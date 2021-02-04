from pyplanet.views.generics import ManualListView

class MeteoAdminView(ManualListView):
	title = 'Météo Management on Track'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Vehicles'

	def __init__(self, app, player):
		super().__init__()
		self.manager = app.context.ui
		self.app = app
		self.player = player
		self.unused = 0
		self.fields = [
			{
				'name': 'ID',
				'index': 'id',
				'sorting': False,
				'searching': False,
				'width': 5,
				'type': 'label'
			},
			{
				'name': 'Checkpoint',
				'index': 'checkpoint',
				'sorting': False,
				'searching': False,
				'width': 60,
				'type': 'label'
			},
			{
				'name': 'Actual',
				'index': 'actual_meteo',
				'sorting': False,
				'searching': False,
				'width': 20,
				'type': 'label',
				'safe': True
			},
		]

	async def get_data(self):
		return [
			{"id": 99, 
			"checkpoint": "Full Track", 
			"actual_meteo": ""
			}, 
			{"id": 0, 
			"checkpoint": "Start > Checkpoint 1", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[0]]
			}, 
			{"id": 1, 
			"checkpoint": "Checkpoint 1 > Checkpoint 2", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[1]]
			}, 
			{"id": 2, 
			"checkpoint": "Checkpoint 2 > Checkpoint 3", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[2]]
			}, 
			{"id": 3, 
			"checkpoint": "Checkpoint 3 > Checkpoint 4", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[3]]
			}, 
			{"id": 4, 
			"checkpoint": "Checkpoint 4 > Checkpoint 5", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[4]]
			}, 
			{"id": 5, 
			"checkpoint": "Checkpoint 5 > Checkpoint 6", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[5]]
			}, 
			{"id": 6, 
			"checkpoint": "Checkpoint 6 > Checkpoint 7", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[6]]
			}, 
			{"id": 7, 
			"checkpoint": "Checkpoint 7 > Checkpoint 8", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[7]]
			}, 
			{"id": 8, 
			"checkpoint": "Checkpoint 8 > Checkpoint 9", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[8]]
			}, 
			{"id": 9, 
			"checkpoint": "Checkpoint 9 > Checkpoint 10", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[9]]
			}, 
			{"id": 10, 
			"checkpoint": "Checkpoint 10 > Checkpoint 11", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[10]]
			}, 
			{"id": 11, 
			"checkpoint": "Checkpoint 11 > Checkpoint 12", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[11]]
			}, 
			{"id": 12, 
			"checkpoint": "Checkpoint 12 > Checkpoint 13", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[12]]
			}, 
			{"id": 13, 
			"checkpoint": "Checkpoint 13 > Finish line", 
			"actual_meteo": self.app.Meteo.MeteoText[self.app.Meteo.MeteoCheckpointData[13]]
			}
		]

	async def display(self, **kwargs):
		kwargs['player'] = self.player
		return await super().display(**kwargs)

	async def get_actions(self):
		return [
			{
				'name': 'Sun',
				'text': 'Sun',
				'sorting': False,
				'searching': False,
				'width': 5,
				'type': 'quad',
				'attrs': 'image=\"http://ftp.boss-bravo.fr/trackmania/images/formula1/sun.png\" autoscale=\"0\"',
				'action': self.set_meteo_sun,
				'safe': True,
			},
			{
				'name': 'Blank',
				'text': '',
				'sorting': False,
				'searching': False,
				'width': 3,
				'type': 'quad',
				'action': self.set_blank,
				'safe': True,
			},
			{
				'name': 'Clouds',
				'text': 'Clouds',
				'sorting': False,
				'searching': False,
				'width': 7,
				'type': 'quad',
				'attrs': 'image=\"http://ftp.boss-bravo.fr/trackmania/images/formula1/clouds.png\" autoscale=\"0\"',
				'action': self.set_meteo_clouds,
				'safe': True,
			},
			{
				'name': 'Blank',
				'text': '',
				'sorting': False,
				'searching': False,
				'width': 3,
				'type': 'quad',
				'action': self.set_blank,
				'safe': True,
			},
			{
				'name': 'Fog',
				'text': 'Fog',
				'sorting': False,
				'searching': False,
				'width': 5,
				'type': 'quad',
				'attrs': 'image=\"http://ftp.boss-bravo.fr/trackmania/images/formula1/fog.png\" autoscale=\"0\"',
				'action': self.set_meteo_fog,
				'safe': True,
			},
			{
				'name': 'Blank',
				'text': '',
				'sorting': False,
				'searching': False,
				'width': 3,
				'type': 'quad',
				'action': self.set_blank,
				'safe': True,
			},
			{
				'name': 'Rain',
				'text': 'Rain',
				'sorting': False,
				'searching': False,
				'width': 5,
				'type': 'quad',
				'attrs': 'image=\"http://ftp.boss-bravo.fr/trackmania/images/formula1/rain.png\" autoscale=\"0\"',
				'action': self.set_meteo_rain,
				'safe': True,
			},
			{
				'name': 'Blank',
				'text': '',
				'sorting': False,
				'searching': False,
				'width': 3,
				'type': 'quad',
				'action': self.set_blank,
				'safe': True,
			},
			{
				'name': 'Snow',
				'text': 'Snow',
				'sorting': False,
				'searching': False,
				'width': 5,
				'type': 'quad',
				'attrs': 'image=\"http://ftp.boss-bravo.fr/trackmania/images/formula1/snowflake.png\" autoscale=\"0\"',
				'action': self.set_meteo_snow,
				'safe': True,
			},
			{
				'name': 'Blank',
				'text': '',
				'sorting': False,
				'searching': False,
				'width': 3,
				'type': 'quad',
				'action': self.set_blank,
				'safe': True,
			},
		]

	async def set_blank(self, user, values, player, *args, **kwargs):
		self.unused = 0

	async def set_meteo_sun(self, user, values, player, *args, **kwargs):
		if player['id'] < 99:
			self.app.Meteo.MeteoCheckpointData[player['id']] = 0
		else:
			for i in range(0,self.app.Meteo.CheckpointNumberWithoutStart + 1):
				self.app.Meteo.MeteoCheckpointData[i] = 0
		await self.refresh(self.player)

	async def set_meteo_clouds(self, user, values, player, *args, **kwargs):
		if player['id'] < 99:
			self.app.Meteo.MeteoCheckpointData[player['id']] = 1
		else:
			for i in range(0,self.app.Meteo.CheckpointNumberWithoutStart + 1):
				self.app.Meteo.MeteoCheckpointData[i] = 1
		await self.refresh(self.player)

	async def set_meteo_fog(self, user, values, player, *args, **kwargs):
		if player['id'] < 99:
			self.app.Meteo.MeteoCheckpointData[player['id']] = 2
		else:
			for i in range(0,self.app.Meteo.CheckpointNumberWithoutStart + 1):
				self.app.Meteo.MeteoCheckpointData[i] = 2
		await self.refresh(self.player)

	async def set_meteo_rain(self, user, values, player, *args, **kwargs):
		if player['id'] < 99:
			self.app.Meteo.MeteoCheckpointData[player['id']] = 3
		else:
			for i in range(0,self.app.Meteo.CheckpointNumberWithoutStart + 1):
				self.app.Meteo.MeteoCheckpointData[i] = 3
		await self.refresh(self.player)

	async def set_meteo_snow(self, user, values, player, *args, **kwargs):
		if player['id'] < 99:
			self.app.Meteo.MeteoCheckpointData[player['id']] = 4
		else:
			for i in range(0,self.app.Meteo.CheckpointNumberWithoutStart + 1):
				self.app.Meteo.MeteoCheckpointData[i] = 4
		await self.refresh(self.player)
