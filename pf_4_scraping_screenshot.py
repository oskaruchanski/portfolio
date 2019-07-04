from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import random as rd

data = pd.read_excel('path_to_your_file.xlsx', header=1)
# data.head(5)
data['M6'] = data['M4'] + ' ' + data['M3']
list_of_interest = data['M6'].iloc[70:]

filename = 'screen'

browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
time.sleep(1)
browser.maximize_window()
browser.get('https://www.google.com')
time.sleep(1)
priv_pol = browser.find_element_by_id('cnsd')
priv_pol.click()

for i, item in enumerate(list_of_interest):
    input_field = browser.find_element_by_name('q')
    input_field.click()
    input_field.clear()
    input_field.send_keys('"' + item + '"' + ' -site:youtube.com')
    input_field.send_keys(Keys.RETURN)
    time.sleep(rd.randint(2, 5))
    # eksport prtscr
    original_size = browser.get_window_size()
    required_width = browser.execute_script(
        'return document.body.parentNode.scrollWidth')
    required_height = browser.execute_script(
        'return document.body.parentNode.scrollHeight')
    browser.set_window_size(required_width, required_height)
    browser.save_screenshot(filename + str(i+71) + '.png')
    browser.set_window_size(original_size['width'], original_size['height'])
    time.sleep(rd.randint(2, 5))
    if i % 10 == 0:
        browser.close()
        browser = webdriver.Safari(executable_path='/usr/bin/safaridriver')
        time.sleep(1)
        browser.maximize_window()
        browser.get('https://www.google.com')
        time.sleep(1)
        priv_pol = browser.find_element_by_id('cnsd')
        priv_pol.click()

browser.close()
