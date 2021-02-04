from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.apps.core.pyplanet.views.controller import ControllerView


class FiaAutoDetection:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.controller_view = ControllerView(manager=self.app.context.ui)

	async def on_start(self):
		self.app.context.signals.listen(tm_signals.stunt, self.stunt)
	
	def stunt(self, player, race_time, lap_time, stunt_score, figure, angle, points, combo, is_straight, is_reverse, is_master_jump, factor):
		print("Stunt datas : player = %s | stunt_score = %s | figure = %s | angle = %s | points = %s | combo = %s | is_straight = %s | is_reverse = %s | is_master_jump = %s | factor" % (player, stunt_score, figure, angle, points, combo, is_straight, is_reverse, is_master_jump, factor))