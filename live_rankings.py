from pyplanet.apps.config import AppConfig
from pyplanet.apps.contrib.formula1.view import LiveRankingsWidget
from pyplanet.apps.contrib.formula1.view import FlagView

from pyplanet.apps.core.trackmania import callbacks as tm_signals
from pyplanet.apps.core.maniaplanet import callbacks as mp_signals


class LiveRankings(AppConfig):
	game_dependencies = ['trackmania']
	app_dependencies = ['core.maniaplanet', 'core.trackmania']

	def __init__(self, app):
		self.app = app
		self.instance = app.instance

		self.current_rankings = []
		self.widget = None
		
		self.BlackFlagView = FlagView(self, manager=app.context.ui)

	async def on_start(self):
		# Register signals
		self.app.context.signals.listen(mp_signals.map.map_start, self.map_start)
		self.app.context.signals.listen(tm_signals.finish, self.player_finish)
		self.app.context.signals.listen(tm_signals.waypoint, self.player_waypoint)
		self.app.context.signals.listen(mp_signals.player.player_connect, self.player_connect)
		self.app.context.signals.listen(tm_signals.give_up, self.player_giveup)
		self.app.context.signals.listen(mp_signals.player.player_disconnect, self.player_giveup)
		self.app.context.signals.listen(mp_signals.player.player_enter_spectator_slot, self.player_giveup)
		self.app.context.signals.listen(tm_signals.scores, self.scores)

		self.widget = LiveRankingsWidget(self, self.app)
		await self.widget.display()

		scores = None
		try:
			scores = await self.instance.gbx('Trackmania.GetScores')
		except:
			pass

		if scores:
			await self.handle_scores(scores['players'])
			await self.widget.display()

	def is_mode_supported(self, mode):
		mode = mode.lower()
		return mode.startswith('timeattack') or mode.startswith('rounds') or mode.startswith('team') or \
			   mode.startswith('laps') or mode.startswith('cup')

	async def scores(self, section, players, **kwargs):
		await self.handle_scores(players)
		# self.widget.widget_y = 90
		# self.widget.top_entries = 50
		await self.widget.display()

	async def handle_scores(self, players):
		# self.current_rankings = [{'login': 'boss-bravo1', 'nickname': 'Bot 1', 'score': 791117, 'cps': 5, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo2', 'nickname': 'Bot 2', 'score': 791117, 'cps': 6, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo3', 'nickname': 'Bot 3', 'score': 791117, 'cps': 7, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo4', 'nickname': 'Bot 4', 'score': 791117, 'cps': 8, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo5', 'nickname': 'Bot 5', 'score': 791117, 'cps': 9, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085]}, {'login': 'boss-bravo6', 'nickname': 'Bot 6', 'score': 791117, 'cps': 10, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo7', 'nickname': 'Bot 7', 'score': 791117, 'cps': 11, 'best_cps': 10, 'finish': False, 'giveup': False}, {'login': 'boss-bravo8', 'nickname': 'Bot 8', 'score': 791117, 'cps': 12, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo9', 'nickname': 'Bot 9', 'score': 791117, 'cps': 13, 'best_cps': 10, 'finish': False, 'giveup': False}, {'login': 'boss-bravo10', 'nickname': 'Bot 10', 'score': 791117, 'cps': 14, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo11', 'nickname': 'Bot 11', 'score': 791117, 'cps': 15, 'best_cps': 10, 'finish': False, 'giveup': False}, {'login': 'boss-bravo12', 'nickname': 'Bot 12', 'score': 791117, 'cps': 16, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo13', 'nickname': 'Bot 13', 'score': 791117, 'cps': 17, 'best_cps': 10, 'finish': False, 'giveup': False}, {'login': 'boss-bravo14', 'nickname': 'Bot 14', 'score': 791117, 'cps': 18, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo15', 'nickname': 'Bot 15', 'score': 791117, 'cps': 19, 'best_cps': 10, 'finish': False, 'giveup': False}, {'login': 'boss-bravo16', 'nickname': 'Bot 16', 'score': 791117, 'cps': 20, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo17', 'nickname': 'Bot 17', 'score': 791117, 'cps': 21, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo18', 'nickname': 'Bot 18', 'score': 791117, 'cps': 23, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo19', 'nickname': 'Bot 19', 'score': 791117, 'cps': 22, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo20', 'nickname': 'Bot 20', 'score': 791117, 'cps': 24, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo21', 'nickname': 'Bot 21', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo22', 'nickname': 'Bot 22', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo23', 'nickname': 'Bot 23', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo24', 'nickname': 'Bot 24', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo25', 'nickname': 'Bot 25', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo26', 'nickname': 'Bot 26', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo27', 'nickname': 'Bot 27', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo28', 'nickname': 'Bot 28', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo29', 'nickname': 'Bot 29', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}, {'login': 'boss-bravo30', 'nickname': 'Bot 30', 'score': 791117, 'cps': 25, 'best_cps': 10, 'finish': False, 'giveup': False, 'cp_times': [64826, 66108, 71714, 73861, 75085, 86195, 87749, 133407, 136372, 143602, 169847, 183813, 188697, 195369, 203019, 204369, 209785, 211995, 213158, 223345, 224665, 228336, 231354, 239370, 247924, 265032, 289230, 295494, 302525, 303741, 308615, 310645, 311678, 321340, 322548, 326010, 328838, 335255, 343533, 350134, 350268, 353308, 411218, 413459, 430702, 434294, 495004, 508026, 564174, 568705, 572085, 578628, 586982, 592438, 592562, 595410, 789809, 791117]}]
		# self.current_rankings = []

		current_script = (await self.instance.mode_manager.get_current_script()).lower()
		if 'timeattack' in current_script:
			for player in players:
				if 'best_race_time' in player:
					if player['best_race_time'] != -1:
						new_ranking = dict(login=player['player'].login, nickname=player['player'].nickname, score=player['best_race_time'])
						self.current_rankings.append(new_ranking)
				elif 'bestracetime' in player:
					if player['bestracetime'] != -1:
						new_ranking = dict(login=player['login'], nickname=player['name'], score=player['bestracetime'])
						self.current_rankings.append(new_ranking)

			self.current_rankings.sort(key=lambda x: x['score'])
		elif 'rounds' in current_script or 'team' in current_script or 'cup' in current_script:
			for player in players:
				if 'map_points' in player:
					if player['map_points'] != -1:
						new_ranking = dict(login=player['player'].login, nickname=player['player'].nickname, score=player['map_points'])
						self.current_rankings.append(new_ranking)
				elif 'mappoints' in player:
					if player['mappoints'] != -1:
						new_ranking = dict(login=player['login'], nickname=player['name'], score=player['mappoints'])
						self.current_rankings.append(new_ranking)

			self.current_rankings.sort(key=lambda x: x['score'])
			self.current_rankings.reverse()

	async def map_start(self, map, restarted, **kwargs):
		self.current_rankings = []
		# self.widget.widget_y = 20
		# self.widget.top_entries = 16
		await self.widget.display()

	async def player_connect(self, player, is_spectator, source, signal):
		await self.widget.display(player=player)

	async def player_giveup(self, player, *args, **kwargs):
		if 'Laps' not in await self.instance.mode_manager.get_current_script():
			return
		
		# print(self.current_rankings)

		current_rankings = [x for x in self.current_rankings if x['login'] == player.login]
		if len(current_rankings) > 0:
			current_ranking = current_rankings[0]
			current_ranking['giveup'] = True

		await self.widget.display()
		
		# print(self.current_rankings)

	async def player_waypoint(self, player, race_time, flow, raw):
		if 'laps' not in (await self.instance.mode_manager.get_current_script()).lower():
			return
		
		# print(self.current_rankings)
		
		await self.checkYellowFlagAutoPenalty(player.login)
		
		current_rankings = [x for x in self.current_rankings if x['login'] == player.login]
		if len(current_rankings) > 0:
			current_ranking = current_rankings[0]
			current_ranking['score'] = raw['racetime']
			current_ranking['cps'] = (raw['checkpointinrace'] + 1)
			current_ranking['best_cps'] = (self.current_rankings[0]['cps'])
			current_ranking['finish'] = raw['isendrace']
			current_ranking['cp_times'] = raw['curracecheckpoints']
			current_ranking['giveup'] = False
		else:
			best_cps = 0
			if len(self.current_rankings) > 0:
				best_cps = (self.current_rankings[0]['cps'])
			new_ranking = dict(login=player.login, nickname=player.nickname, score=raw['racetime'], cps=(raw['checkpointinrace'] + 1), best_cps=best_cps, cp_times=raw['curracecheckpoints'], finish=raw['isendrace'], giveup=False)
			self.current_rankings.append(new_ranking)
		
		self.current_rankings.sort(key=lambda x: (-x['cps'], x['score']))
		await self.widget.display()

	async def player_finish(self, player, race_time, lap_time, cps, flow, raw, **kwargs):
		current_script = (await self.instance.mode_manager.get_current_script()).lower()
		if 'laps' in current_script:
			await self.player_waypoint(player, race_time, flow, raw)
			return

		if 'timeattack' not in current_script:
			return

		current_rankings = [x for x in self.current_rankings if x['login'] == player.login]
		score = lap_time
		if len(current_rankings) > 0:
			current_ranking = current_rankings[0]

			if score < current_ranking['score']:
				current_ranking['score'] = score
				self.current_rankings.sort(key=lambda x: x['score'])
				await self.widget.display()
		else:
			new_ranking = dict(login=player.login, nickname=player.nickname, score=score)
			self.current_rankings.append(new_ranking)
			self.current_rankings.sort(key=lambda x: x['score'])
			await self.widget.display()
	
	def player_find_ranking(self, player_login):
		data_return = {'rank':0, 'data':0}
		i = 0
		for line_rank in self.current_rankings:
			i += 1
			if line_rank['login'] == player_login:
				data_return = {'rank':i,'data':line_rank}
				break
		return data_return
	
	async def checkYellowFlagAutoPenalty(self, player_login):
		if True == False:
			if self.app.ToolbarAdmin.view.SafetyCarStatus == 1 or self.app.ToolbarAdmin.view.YellowFlagStatus == 1:
				i = 0
				RaceRankingNow = {}
				for rank_player in self.app.RaceRanking.current_rankings:
					i += 1
					RaceRankingNow[i] = rank_player['login']
				
				if self.app.ToolbarAdmin.view.RaceRankingStartYellowFlag != RaceRankingNow:
					login_penalty = ""
					for i in range(1,len(self.app.ToolbarAdmin.view.RaceRankingStartYellowFlag)+1):
						if RaceRankingNow[i] != self.app.ToolbarAdmin.view.RaceRankingStartYellowFlag[i]:
							login_penalty = RaceRankingNow[i]
							break
					if login_penalty not in self.app.RaceInfos.PlayersPenalties:
						self.BlackFlagView.flag_sound_active = 1
						self.BlackFlagView.flag_sound = "Penalty"
						self.BlackFlagView.flag_name = "black_flag"
						self.BlackFlagView.text_1 = "$s$00cPENALTY !"
						self.BlackFlagView.text_2 = ""
						await self.BlackFlagView.display(player_logins=[login_penalty])
						await self.BlackFlagView.setstatus(1)
						await self.app.instance.chat('$s$00cAutomatic Penalty for %s, overtake on Yellow Flag'%(login_penalty,))
						self.app.RaceInfos.PlayersPenalties.append(login_penalty)
