from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager as CDM
import time
import pickle
import os

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
# chrome_options.add_argument("--disable-gpu")  # Отключение GPU (для стабильности)
# chrome_options.add_argument("--no-sandbox")  # Для предотвращения ошибок в Linux
# chrome_options.add_argument("--window-size=1920x1080")  # Размер окна
ip_port = ''
chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15')

cookie_path = 'my_cookies.dat'
local_storage_path = 'local_storage.pkl'
session_storage_path = 'session_storage.pkl'
local_storage_path_pr1cechart = 'local_storage_pr1cechart.pkl'
session_storage_path_pr1cechart = 'session_storage_pr1cechart.pkl'

url_Waaanther = 'https://web.telegram.org/a/#748128253'
url_pr1cechart = 'https://web.telegram.org/a/#587365981'
url_lekhsak = 'https://web.telegram.org/a/#737571357'
url_lpacev1ch = 'https://web.telegram.org/a/#878757091'
url_akkkeyjin = 'https://web.telegram.org/a/#5440772908'
url_ifvck1ngh8u = 'https://web.telegram.org/a/#679941570'

def save_cookies(driver, path):
    """Сохранение cookies в файл"""
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    """Загрузка cookies из файла"""
    if os.path.exists(path):
        with open(path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                # Убедимся, что cookie имеет правильный домен и путь
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])  # Преобразуем значение в int
                driver.add_cookie(cookie)

def save_storage(driver, path, storage_type='localStorage'):
    """Сохранение localStorage или sessionStorage в файл"""
    storage = driver.execute_script(f"return window.{storage_type};")
    with open(path, 'wb') as file:
        pickle.dump(storage, file)

def load_storage(driver, path, storage_type='localStorage'):
    """Загрузка localStorage или sessionStorage из файла"""
    if os.path.exists(path):
        with open(path, 'rb') as file:
            storage = pickle.load(file)
            for key, value in storage.items():
                driver.execute_script(f"window.{storage_type}.setItem(arguments[0], arguments[1]);", key, value)


def login_tg():
    try:
        driver = webdriver.Chrome(service= Service(CDM().install()),
                          options=chrome_options,
                          )
    except Exception as err:
        print(f"cant connect, err {err}")
        return
    print(f'connected {driver}')
    driver.implicitly_wait(5)
    url='https://web.telegram.org/'
    driver.get(url)

    if os.path.exists(cookie_path):
        print('Cookies already exist')
        # load_cookies(driver, cookie_path)
        # driver.refresh()  # Перезагрузка страницы после загрузки cookies
        # time.sleep(2)
        
        # Загрузка localStorage и sessionStorage
        load_storage(driver, local_storage_path, 'localStorage')
        load_storage(driver, session_storage_path, 'sessionStorage')
        # driver.refresh()  # Перезагрузка страницы для применения данных
        driver.get('https://web.telegram.org/a/#587365981')
        time.sleep(2)
    else:
        print('cookie is not writed')
        time.sleep(10)
        driver.find_element(by=By.XPATH, value = '//*[@id="auth-pages"]/div/div[2]/div[3]/div/div[2]/button/div').click()
        # driver.find_element(by=By.XPATH, value = '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[1]/div[1]').send_keys('be')
        # driver.find_element(by=By.XPATH, value = '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[1]/div[3]/div/ul/li[20]/span[2]').click()
        driver.find_element(by=By.XPATH, value = '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]').send_keys('447459399858')
        driver.find_element(by=By.XPATH, value = '//*[@id="auth-pages"]/div/div[2]/div[2]/div/div[3]/button[1]/div').click()
        
        input("write to save session")
        
         # Сохранение cookies, localStorage и sessionStorage после успешного входа
        save_cookies(driver, cookie_path)
        save_storage(driver, local_storage_path, 'localStorage')
        save_storage(driver, session_storage_path, 'sessionStorage')
        print('Cookies, localStorage, and sessionStorage saved!')

    # driver.refresh()
    # driver.get('https://web.telegram.org/a/#587365981')
    # driver.refresh()
    # time.sleep(5)
    # driver.find_element(by=By.XPATH, value = '//*[@id="MiddleColumn"]/div[4]/div[1]/div[3]/div/button[2]').click()
    try: 
        driver.find_element(by=By.XPATH, value = '//*[@id="portals"]/div[1]/div/div/div[2]/div[2]/div/button').click()
    except Exception as err:
        print(f"cant find button 'smthg went wrong', err: {err}")

    driver.find_element(by=By.XPATH, value = '//*[@id="message-input-text"]/div[1]/div').click()
    driver.find_element(by=By.XPATH, value = '//*[@id="editable-message-text"]').send_keys('test bota')  
    time.sleep(2)  
    driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/button').click()   
    # driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/button').click()  
    # driver.find_element(by=By.XPATH, value = '//*[@id="MiddleColumn"]/div[4]/div[2]/div/div[2]/div[1]/button').click()    

    print('Звоним Ромчику')    

    input('some to exit')
    driver.quit()

def start(name: str):
    if name == '@pr1cechart':
        call(url_pr1cechart)
    elif name == '@Waaanther':
        call(url_Waaanther)
    elif name == '@lekhsak':
        call(url_lekhsak)
    elif name == '@lpacev1ch':
        call(url_lpacev1ch)
    elif name == '@akkkeyjin':
        call(url_akkkeyjin)
    elif name == '@ifvck1ngh8u':
        call(url_ifvck1ngh8u)

def call(chat_url: str):
    try:
        driver = webdriver.Chrome(service= Service(CDM().install()),
                          options=chrome_options,
                          )
    except Exception as err:
        print(f"cant connect, err {err}")
        return
    print(f'connected {driver}')
    driver.implicitly_wait(5)
    url='https://web.telegram.org/'
    driver.get(url)

    load_storage(driver, local_storage_path_pr1cechart, 'localStorage')
    load_storage(driver, session_storage_path_pr1cechart, 'sessionStorage')
    # driver.refresh()  # Перезагрузка страницы для применения данных
    driver.get(chat_url)
    time.sleep(2)
    
    try: 
        driver.find_element(by=By.XPATH, value = '//*[@id="portals"]/div[1]/div/div/div[2]/div[2]/div/button').click()
    except Exception as err:
        print(f"cant find button 'smthg went wrong', err: {err}")

    time.sleep(3)
    # input('smthng to next step')
    # driver.find_element(by=By.XPATH, value = '//*[@id="message-input-text"]/div[1]/div').click()
    # driver.find_element(by=By.XPATH, value = '//*[@id="editable-message-text"]').send_keys('test bota')  
    # time.sleep(2)  
    # driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/button').click()   
    # driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div[1]/button').click()  
    try:
        driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[4]/div[1]/div[2]/div/button[2]').click()    
    except Exception as err:
        print('first timer for call button is timeout')
        time.sleep(12)
        try:
            driver.find_element(by=By.XPATH, value = '//*[@id="portals"]/div[1]/div/div/div[2]/div[2]/div/button').click()
        except Exception as err1:
            print(f'err = {err1}')
        # return f'не успела догрузиться кнопка звонка, пробуй еще раз (err={err})'
    print('Звоним!')    

    input('some to exit')
    driver.quit()

    