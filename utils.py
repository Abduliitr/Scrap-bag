import time
import logging as log

def get_potd(browser):
    browser.get("https://practice.geeksforgeeks.org/problem-of-the-day/")
    time.sleep(3)
    res = browser.find_element( 'xpath', '//*[@id="potd_solve_prob"]').get_attribute('href')
    log.info("// Todays problem of the day is : %s", res)
    return res