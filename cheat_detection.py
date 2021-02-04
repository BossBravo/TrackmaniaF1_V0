import keyboard
import threading, time

from pyplanet.apps.core.maniaplanet import callbacks as mp_signals
from pyplanet.apps.core.trackmania import callbacks as tm_signals

from pyplanet.apps.core.pyplanet.views.controller import ControllerView


class CheatDetection:
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']
	# mode_dependencies = ['TimeAttack']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance
		self.controller_view = ControllerView(manager=self.app.context.ui)

	async def on_start(self):
		print("Cheat Detection Active")
		# threading.Thread(target = self.KeyDetection).start()
		keyboard.hook(self.KeyDetectionAll)
	
	def KeyDetectionAll(self, data):
		print("Key pressed : %s" % data)
	
	def KeyDetection(self):
		print("Cheat Detection Cycle ON")
		while True:
			time.sleep(0.05)
			try:
				if keyboard.is_pressed('*'):
					print('You Pressed The Fucking Key!')
				else:
					pass
			except:
				break