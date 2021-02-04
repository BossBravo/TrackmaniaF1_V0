from pyplanet.views.generics import ManualListView

class ChecklistView(ManualListView):
	title = 'Race management'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Race'

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
				'name': 'Actual Mode',
				'index': 'actual_mode',
				'sorting': False,
				'searching': False,
				'width': 60,
				'type': 'label'
			},
			{
				'name': 'Actual Race',
				'index': 'actual_race',
				'sorting': False,
				'searching': False,
				'width': 60,
				'type': 'label'
			},
			{
				'name': 'Mode',
				'index': 'mode',
				'sorting': False,
				'searching': False,
				'width': 60,
				'type': 'label'
			}
		]

	async def get_data(self):
		return [
			{"id": 0, 
			"actual_mode": self.app.RaceManagement.ActualMode, 
			"actual_race": self.app.RaceManagement.ActualRace, 
			"mode": "Essais publics", 
			"select_mode": ""
			},
			{"id": 1, 
			"actual_mode": self.app.RaceManagement.ActualMode, 
			"actual_race": self.app.RaceManagement.ActualRace, 
			"mode": "Essais libres", 
			"select_mode": ""
			},
			{"id": 2, 
			"actual_mode": self.app.RaceManagement.ActualMode, 
			"actual_race": self.app.RaceManagement.ActualRace, 
			"mode": "Q1 + Q2", 
			"select_mode": ""
			},
			{"id": 3, 
			"actual_mode": self.app.RaceManagement.ActualMode, 
			"actual_race": self.app.RaceManagement.ActualRace, 
			"mode": "Q3", 
			"select_mode": ""
			},
			{"id": 4, 
			"actual_mode": self.app.RaceManagement.ActualMode, 
			"actual_race": self.app.RaceManagement.ActualRace, 
			"mode": "Course", 
			"select_mode": ""
			}
		]

	async def display(self, **kwargs):
		kwargs['player'] = self.player
		return await super().display(**kwargs)

	async def get_actions(self):
		return [
			{
				'name': 'Select Mode',
				'type': 'label',
				'text': 'Select Mode',
				'width': 20,
				'action': self.set_mode,
				'safe': True
			}
		]

	async def set_blank(self, user, values, player, *args, **kwargs):
		self.unused = 0

	async def set_mode(self, user, values, player, *args, **kwargs):
		await self.app.RaceManagement.set_mode(player['id'], player['mode'],user)
		await super().hide()
