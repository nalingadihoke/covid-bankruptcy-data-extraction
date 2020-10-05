# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import os
import shutil
import requests
import sys
from lxml import html
import time
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException



INPUT_FILE_PATH = ""
DOWNLOAD_DIR_PATH = ""
CHROME_DRIVER_PATH = ""



def _fill_text(el, search_key, search_params):
    if search_key in search_params:
        el.send_keys(search_params[search_key])
    
def _select_from_options(el, search_key, search_params):
    if search_key not in search_params:
        return
    search_value = search_params[search_key]
    for option in el.find_elements_by_tag_name('option'):
        if option.text.strip() == search_value:
            option.click()
            return

def _select_checkbox(el, search_key, search_params):
    if search_key in search_params and search_params[search_key] == "Select":
        el.click()
        
    
        
def search(browser, search_params, i):
    browser.get("https://www.bloomberglaw.com/product/blaw/search/results/503b7fe442093008906e19ebeb2c9c0b")

    # Logging into the website

    username = browser.find_element_by_xpath("//*[@id='indg-username']")
    password = browser.find_element_by_xpath("//*[@id='indg-password']")
        

    _fill_text(username, "Username", search_params)
    _fill_text(password, "Password", search_params)
    
    browser.find_element_by_xpath("//*[@id='indg-submit']").click()

    
    timeout = 100
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[1]/span")))
    except TimeoutException:
        print("Timed out waiting for search results page to load")
        
    # Setting the date
    
    temp = browser.find_elements_by_class_name('selected')
    
    temp[0].click()
    
    browser.find_element_by_xpath('/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[2]').click()
    
    date = browser.find_element_by_xpath('/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div/span/input')
    
    _fill_text(date, 'Date', search_params)
    
    browser.find_element_by_xpath("//body").click()
    
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="search-results-list-container"]/div/div[1]/span[2]/div[1]/label')))
    
    import time 
    time.sleep(2)
    
    url = browser.current_url
    browser.get(url)
    browser.refresh()
    
    # Setting the chapter
    
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[2]/div/div[2]')))
    
    
    
    try:
        browser.find_element_by_xpath(i).click()
    except:
        print("No data for this chapter on this date.")
    
    time.sleep(2)
    
    # Getting the count of records
    
    try:
        c = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[6]/div/div[2]/div/div[1]/label/span/span").text
    except:
        c = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/label/span/span").text
        
    count = ''
    for char in c:
        if char not in "(+)":
            count += char
    count = int(count)
    
    try:
        chap = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[6]/div/div[2]/div/div[1]/label/span").text
    except:
        chap = browser.find_element_by_xpath("/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/label/span").text

    chap = chap.split(' ')

    if count<1000:
        download(browser)
        
        time.sleep(3)
        filename = max([DOWNLOAD_DIR_PATH + "/" + f for f in os.listdir(DOWNLOAD_DIR_PATH)],key=os.path.getctime)
        newname = search_params["Date"].replace("/","_",2) +"_Ch_" + chap[1] +"_"+ chap[2].replace("(","").replace(")","") +".csv"
        shutil.move(filename,os.path.join(DOWNLOAD_DIR_PATH,newname))
    else:
        download(browser)
        
        time.sleep(3)
        filename = max([DOWNLOAD_DIR_PATH + "/" + f for f in os.listdir(DOWNLOAD_DIR_PATH)],key=os.path.getctime)
        newname = search_params["Date"].replace("/","_",2) +"_Ch_" + chap[1] +"_"+ chap[2].replace("(","").replace(")","") +".csv"
        shutil.move(filename,os.path.join(DOWNLOAD_DIR_PATH,newname))
        
    
    
def download(browser):
    action = ActionChains(browser)
    download_menu = browser.find_element_by_class_name("DownloadDocumentsButton")
    download_button = browser.find_element_by_xpath('//*[@id="search-results-list-container"]/div/div[2]/div/div[2]/span[1]/span/span[2]/span[2]/ul/li[2]')
    action.move_to_element(download_menu).perform()
    download_button.click()
    
    
    
def main():
    with open(INPUT_FILE_PATH, "r") as f:
        
        queries = json.load(f)
        #for query in queries:
        chapter_list = ["/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[2]/div/div[1]",
                  "/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[2]/div/div[2]",
                  "/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[2]/div/div[3]",
                  "/html/body/div/div[1]/div[4]/div/div[2]/div[1]/div/div[8]/div/div[2]/div/div[4]"
            ]
        for i in chapter_list:
            
            option = webdriver.ChromeOptions()
            prefs = {'download.default_directory' : DOWNLOAD_DIR_PATH}
            option.add_argument(" - incognito")
            option.add_experimental_option("detach", True)
            option.add_experimental_option('prefs', prefs)
            browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=option)
            
            
            search(browser, queries[0],i)
            browser.quit()

      
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scrape_scrape.py <search query input file path> <chrome drivr path>")
        exit(1)
    # See expected input file format in README

    INPUT_FILE_PATH = sys.argv[1]
    DOWNLOAD_DIR_PATH = sys.argv[2]
    CHROME_DRIVER_PATH = sys.argv[3]
    main()