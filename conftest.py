#Импортируем pytest для использования фикстур, а также опций
import pytest 

#Импортируем веб-драйвер для связи с драйверами браузеров
from selenium import webdriver 
#Импортируем класс опций в соответсвии с новыми стандартами Selenium 4.*
from selenium.webdriver.chrome.options import Options 


class Browser():
	"""Родительский класс Браузера"""	
	def __init__(self):
		#Инициализируем переменную объекта webdriver
		self.webdriver_object = None
		#Инициализируем переменную значения полного наименования браузера
		self.browser_fullname = "none"
		#Инициализируем переменную значения языка интерфейса
		self.language = "none"


	def info(self,msg_type="open"):
		"""Функция вывода информации о запуске/закрытии браузера"""
		if msg_type == "open":
			return f"\n**** Тестирование выполняется в браузере \'{self.browser_fullname}\' ****\n\
				   язык интерфейса: \"{self.language}\""
		elif msg_type == "close":
			return f"\n**** Браузер \'{self.browser_fullname}\' был закрыт ****"
	

	def SetLanguage(user_language):
		return False

class Chrome(Browser):	
	"""Класс браузера для инициализации браузера Google Chrome"""
	def __init__(self,user_language):		
		self.browser_fullname = "Google Chrome"
		self.language = user_language
		options = Options()
		options.add_experimental_option('prefs', {'intl.accept_languages': user_language})
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--ignore-ssl-errors')
		self.webdriver_object = webdriver.Chrome(options=options)
		

class Firefox(Browser):
	"""Класс браузера для инициализации браузера Firefox"""
	def __init__(self,user_language):
		self.browser_fullname = "Firefox"
		self.language = user_language
		profile = webdriver.FirefoxProfile()
		profile.accept_untrusted_certs = True
		profile.set_preference("intl.accept_languages", user_language)
		self.webdriver_object = webdriver.Firefox(firefox_profile=profile)


class AllowedParametrs():
	"""Класс допустимых браузеров и доступных языков интерфейса"""

	#Словарь со значениями доступных для тестирования браузеров
	Allowed_Browsers = {
		"chrome": Chrome,
		"firefox": Firefox
		}
	#Список доступных языков интерфейса
	Allowed_Language = ["ru","uk", "en", "fr", "es", "de"]


def GetBrowser(browser_name,user_language):
	"""Функция инициализации браузера исходя из входных значений"""

	#Определяем корректность значения введённого браузера
	try:
		true_browser = AllowedParametrs.Allowed_Browsers[browser_name]
	except KeyError:			
		raise pytest.UsageError("\n--browser_name может принимать следующие значения: \'chrome\', \'firefox\'.")
	

	#Определяем корректность значения введённого языка интерфейса
	if user_language not in AllowedParametrs.Allowed_Language:
		raise pytest.UsageError("\n--language  может принимать следующие значения: \'ru\', \'uk\', \'en\', \'es\', \'fr\', \'de\'.")
	
	#Инициализируем объект выбранного браузера с указанным языком интерфейса
	return AllowedParametrs.Allowed_Browsers[browser_name](user_language)


def pytest_addoption(parser):
	"""Функция определения входных параметров тестирования"""
	#Опция отвечает за выбор браузера для тестов
	parser.addoption('--browser_name',action ='store',default = "chrome",
					 help ="Выберите браузер: chrome или firefox")

	#Опция отвечает за выбор языка интерфейса
	parser.addoption('--language',action ='store',default ="ru",
					 help = "Доступные языки интерфейса браузера: \'ru\', \'en\'.")


@pytest.fixture(scope = "function")
def browser(request):
	"""Функция отвечает за инициализацию объекта браузера:
	выбор браузера, передача необходимых опций, в число 
	которых входит и предпочитаемый язык интерфейса"""

	#Получаем значение опции выбранного браузера
	browser_name = request.config.getoption("browser_name")
	#Получаем значение опции выбранного языка интерфейса
	user_language = request.config.getoption("language")

	#Инициализируем браузер по входным данным	
	browser = GetBrowser(browser_name,user_language)

	#Выводим информацию о начале теста
	print(browser.info(msg_type="open"))
	yield browser.webdriver_object
	#Выводим информацию о завершении теста
	print(browser.info(msg_type="close"))

	#Закрываем браузер
	browser.webdriver_object.quit()







