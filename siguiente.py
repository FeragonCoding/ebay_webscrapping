from re import search
from telnetlib import EC
from attr import attrs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import pandas as pd
from datetime import date
import time
import re

path = "./chromedriver" #Ruta del driver
driver = webdriver.Chrome(path)

home_link = "https://listado.mercadolibre.com.ar/"
search = "iphone x"
search_kw = search.replace(" ","-")

driver.get(home_link+"/"+search_kw+"#D[A:"+search+"]")
driver.implicitly_wait(10)
#page = BeautifulSoup(driver.page_source,'html.parser')

#next = driver.find_element(By.XPATH("//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a")[0].get('href'))
cookie_btn = driver.find_element(By.XPATH, "//div[@class='cookie-consent-banner-opt-out__actions']/button[contains(@data-testid,'action:understood-button')]")
print(cookie_btn)
#next_btn   = driver.find_element(By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a")

#//div[@class='cookie-consent-banner-opt-out__actions']/button[contains(@data-testid,"action:understood-button")]

#WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='taLnk ulBlueLinks']"))).click()
#//div[@class='cookie-consent-banner-opt-out__actions']/button[contains(@data-testid,"action:understood-button
#WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'cookie-consent-banner-opt-out__action cookie-consent-banner-opt-out__action--primary cookie-consent-banner-opt-out__action--key-accept')))

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cookie-consent-banner-opt-out__actions']/button[contains(@data-testid,'action:understood-button')]"))).click()
next_btn = driver.find_element(By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a")
next_href = next_btn.get_attribute('href')
print(next_href)

#WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a"))).click()

#time.sleep(2)
#print(next_btn)
#next_btn.click()
#time.sleep(2)
