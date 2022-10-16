import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from settings import Tools

driver =Tools.driver

def get_trib(url: str,type: str):
    r = requests.get(url).text
    bs = BeautifulSoup(r,'lxml')
    possible_links = bs.find_all('a',class_ = 'button button-shadow')
    trib_links = [x['href'] for x in possible_links if x.has_attr('href') and type in x.text]
    return trib_links

def get_link(url: str)-> str:
    driver.get(url)
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "center > img"))).click()
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#generater > img"))).click()
    window_before = driver.window_handles[0]
    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="showlink"]'))).click()
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    link=driver.current_url
    driver.switch_to.window(window_before)
    driver.close()
    driver.switch_to.window(window_after)
    return link