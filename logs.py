import logging, os, requests
 
from logging.handlers import RotatingFileHandler

class F1Logs:

	def __init__(self, app):
		self.app = app
		
		self.logger = logging.getLogger("F1")
		self.logger.setLevel(logging.DEBUG)
		 
		formatter = logging.Formatter('%(asctime)s | %(levelname)-10s | %(message)s')
		file_handler = RotatingFileHandler('/home/tm2/F1_Logs/all.log', 'a', 10000000, 10)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(formatter)
		self.logger.addHandler(file_handler)
		
		self.logger_data = logging.getLogger("F1_Data")
		self.logger_data.setLevel(logging.DEBUG)
		 
		formatter_data = logging.Formatter('%(message)s')
		file_handler_data = RotatingFileHandler('/home/tm2/F1_Logs/datas.log', 'a', 100000000, 1)
		file_handler_data.setLevel(logging.DEBUG)
		file_handler_data.setFormatter(formatter_data)
		self.logger_data.addHandler(file_handler_data)

	def log(self, level, message, login='NO_LOGIN', lap=-1, file='NO_FUNCTION_FILE', function='NO_FUNCTION'):
		FinalMessage = '%-25s | %-18s | %-2s | %-16s | %-45s | %s' % (login, self.app.RaceManagement.ActualMode, lap, file, function, message)
		if(level == 'CRITICAL'):
			self.log_critical(FinalMessage)
		elif(level == 'ERROR'):
			self.log_error(FinalMessage)
		elif(level == 'WARNING'):
			self.log_warning(FinalMessage)
		elif(level == 'INFO'):
			self.log_info(FinalMessage)
		else:
			self.log_debug(FinalMessage)
	
	def log_critical(self, FinalMessage):
		self.logger.critical(FinalMessage)
	
	def log_error(self, FinalMessage):
		self.logger.error(FinalMessage)
	
	def log_warning(self, FinalMessage):
		self.logger.warning(FinalMessage)
	
	def log_info(self, FinalMessage):
		self.logger.info(FinalMessage)
	
	def log_debug(self, FinalMessage):
		self.logger.debug(FinalMessage)
	
	def reset_data(self):
		x = requests.post('http://crodaf1.boss-bravo.fr/race_datas/get_server_datas.php?CrodaServerKey=qksjghnqsdqolO238GNuinbcityOZI7JCA7IF6QSNGDQZq57qs1d&CrodaServerType=ResetDatas&CrodaServerSaisonNb=0&CrodaServerRaceNb=0&CrodaServerDatas=0')
		# print(x)
	
	def log_data(self, LineData):
		self.logger_data.debug(LineData)
		x = requests.post('http://crodaf1.boss-bravo.fr/race_datas/get_server_datas.php?CrodaServerKey=qksjghnqsdqolO238GNuinbcityOZI7JCA7IF6QSNGDQZq57qs1d&CrodaServerType=AddDatas&CrodaServerSaisonNb=%s&CrodaServerRaceNb=%s&CrodaServerDatas=%s' % (self.app.RaceManagement.SaisonNb,self.app.RaceManagement.RaceNb,LineData))
		# print(x)