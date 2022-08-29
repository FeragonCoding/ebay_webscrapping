from re import search
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
search = "playstation 4 pro"
search_kw = search.replace(" ","-")
url = home_link+search_kw+"#D[A:"+search+"]"
driver.get(url)

next_page = url


#Handling "Accept Cookies" popup with Selenium in Python
#https://stackoverflow.com/questions/64032271/handling-accept-cookies-popup-with-selenium-in-python
#https://selenium-python.readthedocs.io/waits.html

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cookie-consent-banner-opt-out__actions']/button[contains(@data-testid,'action:understood-button')]"))).click()


article_title = []
article_link = []
article_detail = []
article_status = []
article_score = []
article_reviews_amt = []
article_price = []
article_location = []
article_sold = []
article_province = []
article_vendor = []
vendor_perfil = []
vendor_ventas_totales = []

def retrieve_sold_from_text(text):
    soup = BeautifulSoup(text,'html.parser')
    text_soup = soup.prettify()
    split_text = text_soup.split(' ')
    for num in range(0,len(split_text)):
        if ( 'vendidos' in split_text[num]):
            return int(split_text[num - 1])

def retrieve_ubication_from_text(text,var):
    soup = BeautifulSoup(text,'html.parser')
    text_soup = soup.prettify()
    split_text = text_soup.split(',')
    for num in range(0,len(split_text)):
        if var == 'province':
             return split_text[len(split_text)-1].strip()
        if var == 'location':
             return split_text[len(split_text)-2].strip()





pg_amount = 2

page = BeautifulSoup(driver.page_source,'html.parser')
 
for i in range(0, pg_amount):
    print('Página',i)
    count =0
    for articles in page.findAll('li', attrs={'class':'ui-search-layout__item'}):
        count=count+1
        print('Página',i,'Articulo:',count)
        title = articles.find('h2', attrs={'class':'ui-search-item__title'})
        if title:
            print('Articulo',title.text.strip())
            article_title.append(title.text.strip())
        else: 
            article_title.append('')
            print('No title')
        
        link = articles.find('a', attrs={'class':'ui-search-item__group__element ui-search-link'})
        if link:
            print(link['href'])
            article_link.append(link['href'])
            #Articulo
            driver.get(link['href'])
            article = BeautifulSoup(driver.page_source,'html.parser')
            #Ventas
            sold = article.find('span',attrs={'class':'ui-pdp-subtitle'})
            if sold:
                print(sold.text)
                sold = retrieve_sold_from_text(sold.text)
                print('Vendidos:',sold)
                article_sold.append(sold)
            else: 
                print('No sold')
                article_sold.append('')
            
            ubication = article.find('p', attrs={'class':'ui-seller-info__status-info__subtitle'})
            if ubication:
                    print('Ubicación',ubication.text)
                    province = retrieve_ubication_from_text(ubication.text, "province") #Provincia                       
                    location = retrieve_ubication_from_text(ubication.text, "location") #Localidad
                    #print('Provincia',province)
                    #print('Localidad',location)
                    article_location.append(location)
                    article_province.append(province)
            
            else:
                print('No ubication')
                article_location.append('')
                article_province.append('')
            
            vendor = article.find('span', attrs={'class':'ui-pdp-color--BLUE ui-pdp-family--REGULAR'})    
            if vendor:
                print('Vendedor:',vendor.text)
                article_vendor.append(vendor.text)
                        
            else:
                print('No vendor')
                article_vendor.append('')

            
            perfil = article.find('a',attrs={'class':'ui-pdp-media__action ui-box-component__action'})
            
            if perfil:
                print('URL Perfil',perfil['href'])
                parsed = urlparse(perfil['href'])
                perfil_name = re.sub("\/","",parsed.path)
                print('Perfil:', perfil_name)
                vendor_perfil.append(perfil['href'])
                
                driver.get(perfil['href'])
                vendedor = BeautifulSoup(driver.page_source,'html.parser')
                
                PaginaNoExiste=vendedor.find('h4',attrs={'ui-empty-state__title'})
                if PaginaNoExiste:
                    print('pagina no existe')
                    vendor_ventas_totales.append('')    
                #ventas_totales = vendedor.find('div',attrs={'class':'seller-info'}) 
                else:
                    ventas_totales = vendedor.find('p',attrs={'class':'message__subtitle'})
                    if ventas_totales:
                        print('insuficiente')
                        vendor_ventas_totales.append('ventas insuficientes')  
                        vendor_ventas_totales.append('')  
                    else:
                    
                        ventas_totales = vendedor.find('p',attrs={'class':'seller-info__subtitle-sales'}).get_text()
                    
                    if ventas_totales:
                            print('Ventas totales:',ventas_totales)
                            vendor_ventas_totales.append(ventas_totales)        
                    else: 
                            print('No ventas totales')
                            vendor_ventas_totales.append('')       
            
            else: print('No perfil')
        
        else: 
            print('No link')
            article_link.append('')
        
        
        reviews_amt = articles.find('span',attrs={'class':'ui-search-reviews__amount'})
        if reviews_amt:
            #article_reviews_amt.append(reviews_amt.span.text[0:reviews_amt.span.text.find('valor')-1])
            print(reviews_amt.text)
            article_reviews_amt.append(reviews_amt.text)
        else: 
            print('No review')
            article_reviews_amt.append('')
        
        
        status = articles.find('span', attrs={'class':'ui-search-item__group__element ui-search-item__details'})
        if status:
            print(status.text) # Reacondicionado or Usado
            article_status.append(status.text)
        else: 
            print('Nuevo')
            article_status.append('Nuevo')
        
        price = articles.find('span', attrs={'class':'price-tag-fraction'})
        if price:
            print(price.text)
            article_price.append(price.text)
        else: 
            print('No price')
            article_price.append('')
    
    #next_btn = driver.find_element(By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a")
    #next_btn.click()
    #time.sleep(2)
    print(next_page)
    driver.get(next_page)
    driver.implicitly_wait(10)
    next_btn = driver.find_element(By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a")
    next_href = next_btn.get_attribute('href')
    print(next_href)
    #next_page = next_href
    print("Proxima: ",next_href)
    driver.get(next_href)
    
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ui-search-pagination']/ul/li[contains(@class, '--next')]/a"))).click()
    
    #next_btn = driver.find_element(By.XPATH("//button[text()='Siguiente']"))
    #next_btn.click()
    #time.sleep(2)

article_list = pd.DataFrame({
                            'TITLE':article_title,
                            'STATUS':article_status,
                            'SOLD':article_sold,
                            'VENDOR':article_vendor,
                            'PERFIL':vendor_perfil,
                            #'VENTAS_TOTALES':vendor_ventas_totales,
                            'PROVINCE':article_province,
                            'LOCATION':article_location,
                            #'SCORE':article_score,
                            'REVIEWS_AMT':article_reviews_amt,
                            'PRICE':article_price,
                            #'LOCATION':article_location,
                            'LINK': article_link
                         })



#article_list = article_list.sort_values(by=['PRICE','SCORE','REVIEWS_AMT'], ascending=[True,False,False])
article_list = article_list.sort_values(by=['PRICE'], ascending=[True])

article_list.to_csv(r'./article_list.csv', index=None, header=True, encoding='utf-8-sig')

print(article_list)




