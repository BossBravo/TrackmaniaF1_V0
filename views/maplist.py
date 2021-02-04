from pyplanet.views.generics import ManualListView

class MaplistView(ManualListView):
	title = 'Map List'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Browse'

	def __init__(self, app, player):
		super().__init__()
		self.manager = app.context.ui
		self.app = app
		self.instance = app.instance
		self.player = player
		self.unused = 0
		self.fields = [
			{
				'name': 'UID',
				'index': 'uid',
				'sorting': False,
				'searching': False,
				'width': 100,
				'type': 'label'
			},
			{
				'name': 'Name',
				'index': 'name',
				'sorting': False,
				'searching': False,
				'width': 200,
				'type': 'label'
			}
		]

	async def get_data(self):
		Datas = []
		for map in self.instance.map_manager.maps:
			Datas.append({"uid": map.uid,"name": map.name})
		return Datas

	async def display(self, **kwargs):
		kwargs['player'] = self.player
		return await super().display(**kwargs)

	async def get_actions(self):
		return []

	async def set_blank(self, user, values, player, *args, **kwargs):
		self.unused = 0
