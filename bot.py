#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from db import db

import time
import os
import sys
import csv
import json
import sqlite3

database = db()
actionChains = None
browser = None
Contact = None
message = None
messages = None
invalidFlag = True
conn = None
Link = "https://web.whatsapp.com/"
wait = None
choice = None
docChoice = None
doc_filename = None
unsaved_Contacts = None
media = None

def whatsappLogin():
    global wait,browser,Link, actionChains
    browser = webdriver.Chrome()
    # browser = webdriver.Firefox()
    actionChains = ActionChains(browser)
    wait = WebDriverWait(browser, 600)
    browser.get(Link)
    browser.maximize_window()
    print("QR scanned")

def selectContactViaName(username):
    global wait, browser, actionChains, invalidFlag

    name = username.strip()
    
    target = './/span[@title="'+name+'"]'

    try:
        wait.until(EC.presence_of_element_located(By.XPATH, target))
    except:
        search_box = browser.find_element_by_xpath('//input[@title="Search or start new chat"]')
        search_box.click()
        search_box.clear()
        
        browser.execute_script('arguments[0].value += "' + str(name[:-1]) + '";', search_box)
        search_box.send_keys(name[-1])

        # search_box.send_keys(Keys.SPACE)
        # search_box.send_keys(Keys.BACKSPACE)

        # for ch in str(name):
        #     search_box.send_keys(ch)

        time.sleep(2)

    invalidFlag = True

    try:
        options = browser.find_elements_by_xpath('//div[@id="pane-side"]/div/div/div/*')

        for option in reversed(options):
            try:
                userTypeSpan = option.find_element_by_xpath('.//div/div/div[1]/div/span')            
                userType = userTypeSpan.get_attribute('data-icon')

                if userType == 'default-user':
                    span = option.find_element_by_xpath(target)
                    span.click()
                    invalidFlag = False
                    time.sleep(1)
            except:
                pass

    except NoSuchElementException as e:
        print(e)
        pass

    try:
        mainEl = browser.find_element_by_xpath('//div[@id="main"]')
        mainEl.find_element_by_xpath(target)
    except NoSuchElementException as ex:
        invalidFlag = True
        print(ex)
        pass

def selectContactViaNumber(number):
    global wait, browser, actionChains, invalidFlag
    # x_arg = '//span[contains(@title,' + contact + ')]'
    search_box = browser.find_element_by_xpath('//input[@title="Search or start new chat"]')
    search_box.click()
    search_box.clear()
    
    browser.execute_script('arguments[0].innerText += "' + str(message[1:]) + '";', search_box)

    time.sleep(2)
    
    options = browser.find_elements_by_xpath('//div[@id="pane-side"]/div/div/div/*')

    invalidFlag = True
    for option in reversed(options):
        try:
            userTypeSpan = option.find_element_by_xpath('.//div/div/div[1]/div/span')            
            userType = userTypeSpan.get_attribute('data-icon')
            try:
                img = option.find_element_by_tag_name('img')
                url = img.get_attribute('src')
                if number in url and userType == 'default-user':
                    invalidFlag = False
                    option.click()
                    time.sleep(2)
                    break
            except NoSuchElementException as ex:
                pass
                
            if userType == 'default-user':
                invalidFlag = False
                option.click()
                time.sleep(2)
                break
        except NoSuchElementException as e1:
            # try:
            #     userTypeSpan = option.find_element_by_xpath('.//div/div/div[1]/div/span')            
            #     userType = userTypeSpan.get_attribute('data-icon')
                
            # except NoSuchElementException as e2:
            invalidFlag = True
            continue

    # if invalidFlag and not database.isEntryMade(number):
    #     options[-1].click()
    #     time.sleep(2)
    #     invalidFlag = False
    
def sendMessage(name, number, message, campaign_id):
    global wait, browser, database, invalidFlag
    try:
        input_box = browser.find_element_by_xpath('//div[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        
        input_box.send_keys(message[0])
        browser.execute_script('arguments[0].innerText += "' + str(message[1:]) + '";', input_box)
        input_box.send_keys(Keys.SPACE)
        input_box.send_keys(Keys.BACKSPACE)

        btnSend = browser.find_element_by_xpath('//div[@id="main"]/footer/div[1]/div[3]/button')
        btnSend.click()
        
        database.makeMessageEntry(message, 'text', name, number, campaign_id)
        print("Message sent")
        # time.sleep(5)
    except NoSuchElementException as err:
        print("No such element exception" + str(err))
        return

def sendMedia(name, number, img): # img - name of image along with ext
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    mediaButtonInput = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input')
    
    image_path = os.getcwd() + '/Media/' + img

    mediaButtonInput.send_keys(image_path)

    time.sleep(3)
    whatsapp_send_button_path = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div'
    wait.until(EC.presence_of_element_located((By.XPATH, whatsapp_send_button_path)))
    whatsapp_send_button = browser.find_element_by_xpath(whatsapp_send_button_path)
    whatsapp_send_button.click()
    database.makeMessageEntry(img, 'image', name, number, 0)
    # Controlling windows dialog

    print('media sent')
    
def sendFile(name, number, filename): # img - name of image along with ext
    # Attachment Drop Down Menu
    clipButton = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/div/span')
    clipButton.click()
    time.sleep(1)

    # To send Videos and Images.
    fileButtonInput = browser.find_element_by_xpath(
        '//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[3]/button/input')
    
    file_path = os.getcwd() + '/Media/' + filename

    fileButtonInput.send_keys(file_path)

    time.sleep(3)
    whatsapp_send_button_path = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span[2]/div/div'
    wait.until(EC.presence_of_element_located((By.XPATH, whatsapp_send_button_path)))
    whatsapp_send_button = browser.find_element_by_xpath(whatsapp_send_button_path)
    whatsapp_send_button.click()
    database.makeMessageEntry(filename, 'file', name, number, 0)

    print('file sent')

def main():
    
    global browser, database, invalidFlag

    users = None
    messages = None
    campaign_id = None

    with open('message.csv', 'r') as f:
        data = f.read()

        messages = csv.reader(data.splitlines())

        campaign_id = list(messages)[0][1]

        with open('contacts.csv', 'r') as csvfile:
            users = csv.reader(csvfile, delimiter=',')
            
            if users and messages:
    
                whatsappLogin() # initiate login
                
                wait.until(EC.presence_of_element_located((By.XPATH, '//input[@title="Search or start new chat"]'))) # check if the page is loaded

                for row in users:
                    if not database.isEntryMade(row[0], row[1], campaign_id): # check by the number if entry is made
                        try:
                            selectContactViaName(row[0])
                            time.sleep(2)
                            if not invalidFlag:
                                for msg in messages[1:]:
                                    if msg[0] in ('text', 'word'):
                                        sendMessage(row[0], row[1], msg[1])
                                        time.sleep(2)
                                    elif msg[0] in ('image', 'video', 'media'):
                                        sendMedia(row[0], row[1], msg[1])
                                        time.sleep(3)
                                    elif msg[0] in ('file'):
                                        sendFile(row[0], row[1], msg[1])
                        except Exception as e:
                            print(e)
                            pass

if __name__ == '__main__':
    main()