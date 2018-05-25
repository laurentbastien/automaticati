from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
import requests
import re
from bs4 import BeautifulSoup
from time import sleep
path_to_chromedriver = 'foo/chromedriver' 
browser = webdriver.Chrome(executable_path = path_to_chromedriver)
url = 'https://open.canada.ca/en/search/ati'
browser.get(url)


pageurl = "https://open.canada.ca/en/search/ati?ati%5B0%5D=ss_ati_organization_en%3ANational%20Defence&ajax_page_state%5Btheme%5D=od_bootstrap&ajax_page_state%5Blibraries%5D=bootstrap/wet-boew&ajax_page_state%5Btheme_token%5D=&search_api_fulltext=&page="

for i in range(2899):
    browser.get(pageurl+str(i))
    for i in range(10):
        sleep(0.5)
        browser.find_elements_by_partial_link_text("Make an informal request")[i].click()
        try: 
            myurl = browser.current_url
            html = requests.get(myurl)
            page = html.text
            soup = BeautifulSoup(page, 'html.parser')
            pagen = soup.findAll("", {"class": "field-content"})
            pagen[6]
            pagen = str(pagen[6]).replace('<span class="field-content">',"")
            pagen = pagen.replace("</span>","")
            pagen = int(pagen)
            sleep(0.5)
            if pagen > 0:
                select = Select(browser.find_element_by_xpath("//*[@id='edit-requestor-category']"))
                select.select_by_visible_text('Media')
                select = Select(browser.find_element_by_xpath("//*[@id='edit-delivery-method']"))
                select.select_by_visible_text('Electronic Copy') 
                inputElement = browser.find_element_by_xpath("//*[@id='edit-given-name']")
                inputElement.send_keys('firstname')
                inputElement = browser.find_element_by_xpath("//*[@id='edit-family-name']")
                inputElement.send_keys('lastname')
                inputElement = browser.find_element_by_xpath("//*[@id='edit-your-e-mail-address']")
                inputElement.send_keys('youremail')
                inputElement = browser.find_element_by_xpath("//*[@id='edit-your-telephone-number']")
                inputElement.send_keys('phone number')
                inputElement = browser.find_element_by_xpath("//*[@id='edit-address-fieldset-address']")
                inputElement.send_keys('youraddress')               
                inputElement = browser.find_element_by_xpath("//*[@id='edit-address-fieldset-city']")
                inputElement.send_keys('yourcity')
                select = Select(browser.find_element_by_xpath("//*[@id='edit-address-fieldset-state-province-select']"))
                select.select_by_visible_text('yourprovince') 
                inputElement = browser.find_element_by_xpath("//*[@id='edit-address-fieldset-postal-code']")
                inputElement.send_keys('postalcode')
                select = Select(browser.find_element_by_xpath("//*[@id='edit-address-fieldset-country']"))
                select.select_by_visible_text('Canada') 
                select = Select(browser.find_element_by_xpath("//*[@id='edit-consent']"))
                select.select_by_visible_text('Yes') 
                browser.find_element_by_xpath("//*[@id='edit-actions-submit']").click()        
                browser.execute_script("window.history.go(-2)")
            else:
                browser.execute_script("window.history.go(-1)")
        
        except IndexError:
            browser.execute_script("window.history.go(-1)")