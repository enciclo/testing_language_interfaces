#Импортируем pytest для использования маркеров и параметризированных запросов
import pytest
#Импортируем модуль time для просмотра результатов работы веб-драйвера
import time

#Импортируем класс для обращения к элементам сайта
from selenium.webdriver.common.by import By 
#Импортируем модули для использования явных "ожиданий"
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Импортируем модуль конкретного исключения для отлова события превышения времени поиска
from selenium.common.exceptions import TimeoutException


@pytest.mark.add_button
def test_add_to_basket_button_presence(browser):
	link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"
	browser.get(link)
	try:
		#Указываем значения для явного поиска кнопки
		#Вместо time.sleep(30) можно просто увеличить search_time
		search_time = 5
		#Иницилизируем начальное значение
		add_button = None
		add_button = WebDriverWait(browser,search_time).until(
				#Ожидание проверки наличия элемента в DOM страницы
				EC.presence_of_element_located((By.CSS_SELECTOR,'.btn-add-to-basket'))
			)
	except TimeoutException:
		print("Превышено время поиска элемента add_button: ({search_time} сек.)")

	assert add_button is not None,\
	"Cтраница товара на сайте не содержит кнопку добавления в корзину"
	





