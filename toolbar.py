import logging

from pyplanet.apps.contrib.formula1.views.toolbar import ToolbarView
from pyplanet.contrib.setting import Setting

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals

logger = logging.getLogger(__name__)


class ToolbarRaceControl:
	def __init__(self, app):
		self.app = app
		self.instance = app.instance

		self.view = ToolbarView(self.app)

		self.setting_enable_toolbar = Setting(
			'enable_toolbar', 'Enable the race control toolbar', Setting.CAT_DESIGN, type=bool,
			description='Enable and show the race control toolbar for admins (all players with level above player level).',
			default=True
		)

	async def on_start(self):
		await self.app.context.setting.register(self.setting_enable_toolbar)

		# Listen to connect event.
		self.app.context.signals.listen(mp_signals.player.player_connect, self.player_connect)

		# Display to all current online admins.
		if await self.setting_enable_toolbar.get_value():
			for player in self.app.instance.player_manager.online:
				if player.login in self.app.RaceInfos.RefereeLogins:
					await self.view.display(player_logins=[player.login])

	async def player_connect(self, player, is_spectator, source, **kwargs):
		if player.login in self.app.RaceInfos.RefereeLogins and await self.setting_enable_toolbar.get_value():
			await self.view.display(player_logins=[player.login])
