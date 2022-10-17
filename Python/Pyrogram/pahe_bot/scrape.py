import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from identifiers import *
from settings import Tools


def get_link(e,url):
	driver=Tools.driver
	driver.get(url)
	texts= [y for x in [driver.find_elements('xpath',type) for type in LINK_TYPE] for y in x]
	texts[e].click()

	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, AGREE_BUTTON))).click()		
	except TimeoutException:
		print('No browser verification')

	driver.execute_script("document.getElementById('landing').submit();")
	WebDriverWait(driver, 45).until(EC.element_to_be_clickable((By.CSS_SELECTOR, GENERATE))).click()
	WebDriverWait(driver, 45).until(EC.element_to_be_clickable((By.ID, SHOW_LINK))).click()

	window_after = driver.window_handles[1]
	driver.switch_to.window(window_after)
	driver.execute_script("window.scrollTo(0,535.3499755859375)")
	try:
		WebDriverWait(driver, 45).until(EC.element_to_be_clickable((By.LINK_TEXT, CONTINUE)))
		last=driver.find_element("link text",CONTINUE)
		driver.execute_script("arguments[0].click();", last)
	except TimeoutException:
		print('Failed in the last step')

	link=driver.current_url
	print(link)
	return link

def get_datas(url):
	driver=Tools.driver
	driver.get(url)
	texts= [y for x in [driver.find_elements('xpath',type) for type in LINK_TYPE] for y in x]
	print(f"{len(texts)} links detected")
	out=[x for x in range(len(texts))]
	return out