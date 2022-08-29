from re import search
from attr import attrs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import time

word = 'Nuevo | 7 vendidos'
loc = 'Ramos Mejia , Buenos Aires'
def retrieve_sold_from_text(text):
    soup = BeautifulSoup(text,'html.parser')
    print(soup)
    text_soup = soup.prettify()
    print(text_soup)
    split_text = text_soup.split(' ')
    print(split_text)
    print(len(split_text))
   
    for num in range(0,len(split_text)):
        print(split_text[num])
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
    
    



sold = retrieve_sold_from_text(word)
print(sold)

loca = retrieve_ubication_from_text(loc, "location")
print(loca)