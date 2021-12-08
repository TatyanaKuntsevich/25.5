import pytest
from selenium import webdriver  # подключение библиотеки
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()  # получение объекта веб-драйвера для нужного браузера

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:\QA\Test\chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()

def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('namenamenamenamename@name.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('name')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # неявное ожидание
    pytest.driver.implicitly_wait(5)
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    pytest.driver.get('http://petfriends1.herokuapp.com/my_pets')

    images = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    type = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]//tbody/tr/td[3]')
    stat = 5

    log_file = open('log.txt','w')
    kf=len(images)
    kn=len(names)
    kt=len(type)
    ka = len(age)
    stat1 = "Статистика: " + str(stat) + ". "
    k1 = "Фото: "+str(kf)+". "
    k2 = "Имя: " + str(kn)+". "
    k3 = "Порода: " + str(kt) + ". "
    k4 = "Возраст: " + str(ka)+". "
    log_file.write(stat1)
    log_file.write(k1)
    log_file.write(k2)
    log_file.write(k3)
    log_file.write(k4)
    list_name=[]
    all_pets = []
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert type[i].text != ''
        assert age[i].text != ''
        # список с именами питомцев
        list_name.append(names[i].text)
        # список питомцев
        all_pets.append(names[i].text + " "+type[i].text+" "+age[i].text)

    all_pets_str = str(all_pets)
    log_file.write("Массив питомцев: " +all_pets_str)


    #Присутствуют все питомцы
    assert kn==stat
    #Хотя бы у половины питомцев есть фото
    assert kf>=stat/2
    #У всех питомцев есть возраст
    assert ka==stat
    #У всех питомцев есть порода
    assert kt==stat

    # У всех питомцев разные имена: преобразуем список в множество уникальных имен
    # Кол-во элементов множества должно быть равно количеству элементов массива имен
    b_name = set(list_name)
    list_b_name_str = str(b_name)
    log_file.write("Массив уникальных имен: " + list_b_name_str)
    assert len(b_name) == kn

    # В списке нет повторяющихся питомцев
    b_pets = set(all_pets)
    b_pets_str = str(b_pets)
    log_file.write("Массив уникальных питомцев: " + b_pets_str)
    assert len(b_pets) == kn

    log_file.close()