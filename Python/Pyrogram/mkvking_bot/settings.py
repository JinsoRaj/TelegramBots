from selenium.webdriver.chrome.options import Options
from selenium import webdriver


chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--remote-debugging-port=9232")


class Tools(object):
	driver =webdriver.Chrome(executable_path='chromedriver',options=chrome_options)