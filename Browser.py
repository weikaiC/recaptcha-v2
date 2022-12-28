from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import platform
import os

current_system = platform.system()
if current_system == 'Linux':
    chrome_path = '/usr/bin/chromedriver'
elif current_system == 'Darwin':
    chrome_path = '/usr/local/bin/chromedriver'
elif current_system == 'Windows':
    chrome_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'chromedriver.exe')


class Browser(object):
    chrome = None

    @staticmethod
    def get_chrome(headless=True, incognito=True, user_agent=False, proxy='', from_script=False):
        chrome_options = Options()

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        # web page content will show difference language in difference area
        chrome_options.add_argument('--lang=zh-TW')

        prefs = {
            # 把瀏覽器正受到自動化控制的info bar關掉
            'profile.password_manager_enabled': False,
            'credentials_enable_service': False,
            # prevent target site auto download files
            'download_restrictions': 3
        }

        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('w3c', True)

        if headless:
            chrome_options.add_argument('--headless')

        # Ubuntu 必須要開啟無頭模式
        # if not headless and Config()['Scraper']['mode'] != 'debug' and not from_script:
        #     chrome_options.add_argument('--headless')

        if incognito:
            chrome_options.add_argument('--incognito')

        if user_agent:
            ua = UserAgent(verify_ssl=False)
            user_agent = ua.random   # ua.ie, ua.google, ua.firefox, ua.safari, ua.random 隨機產生前面幾項瀏覽器的User-Agent 字串
            chrome_options.add_argument(f'user-agent={user_agent}')

        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(
            executable_path=chrome_path, chrome_options=chrome_options)
        driver.delete_all_cookies()
        driver.set_window_position(0, 0)

        return driver
