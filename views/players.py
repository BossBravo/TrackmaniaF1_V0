from pyplanet.views.generics import ManualListView

from pyplanet.apps.contrib.formula1.view import FlagView


class PlayerListView(ManualListView):
	title = 'Players'
	icon_style = 'Icons128x128_1'
	icon_substyle = 'Buddies'

	def __init__(self, app, player):
		super().__init__()
		self.manager = app.context.ui
		self.app = app
		self.player = player
		self.fields = [
			{
				'name': 'Nickname',
				'index': 'nickname',
				'sorting': True,
				'searching': True,
				'width': 60,
				'type': 'label'
			},
			{
				'name': 'Login',
				'index': 'login',
				'sorting': False,
				'searching': True,
				'width': 50,
				'type': 'label',
			},
			{
				'name': 'Spec',
				'index': 'is_spectator',
				'sorting': True,
				'searching': False,
				'width': 15,
				'type': 'label',
				'safe': True
			},
			{
				'name': 'Statut Pénalité',
				'index': 'is_penalty',
				'sorting': True,
				'searching': False,
				'width': 20,
				'type': 'label',
				'safe': True
			},
		]
		
		self.flag_view = FlagView(self, manager=app.context.ui)

	async def get_data(self):
		players = self.app.instance.player_manager.online
		return [dict(
			nickname=p.nickname,
			login=p.login,
			is_spectator='$f00&#xf03d;' if p.flow.is_spectator else '$73f&#xf007;',
			is_penalty="Active" if p.login in self.app.RaceInfos.PlayersPenalties else "Inactive",
		) for p in players]

	async def display(self, **kwargs):
		kwargs['player'] = self.player
		return await super().display(**kwargs)

	async def get_actions(self):
		return [
			{
				'name': 'Penalité',
				'type': 'label',
				'text': 'Penalité',
				'width': 12,
				'action': self.action_penalite,
				'safe': True,
			},
		]

	async def action_penalite(self, user, values, player, *args, **kwargs):
		if not player['login'] in self.app.RaceInfos.PlayersPenalties:
			self.flag_view.flag_sound_active = 1
			self.flag_view.flag_sound = "Penalty"
			self.flag_view.flag_name = "black_flag"
			self.flag_view.text_1 = "$s$00cPENALTY !"
			self.flag_view.text_2 = ""
			await self.flag_view.display(player_logins=[player['login']])
			await self.flag_view.setstatus(1)
			await self.app.instance.chat('$s$00cPenalty for %s'%(player['nickname'],))
			self.app.RaceInfos.PlayersPenalties.append(player['login'])
		else:
			await self.flag_view.hide(player_logins=[player['login']])
			await self.flag_view.setstatus(0)
			self.app.RaceInfos.PlayersPenalties.remove(player['login'])
		await self.refresh(self.player)
