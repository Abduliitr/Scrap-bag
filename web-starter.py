import logging as log
import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.window import WindowTypes
from selenium.common.exceptions import NoSuchElementException

from utils import *

default_pw = '***********'
creds_mail  = ['gfgtest101@gmail.com', 'thisismygmail@gmail.com']
creds_pw    = [default_pw, default_pw]
potd = "NA"

gfg_login_button_xref = "/html/body/div[1]/div/div/div[4]/div/div/div[3]/div/a"
fb_oauth_button_xref = "/html/body/div[3]/div/div/div[2]/div/div[2]/div/div/div[2]/button[2]"
fb_email_xref = "//*[@id=\"email\"]"
fb_pw_xref = "//*[@id=\"pass\"]"
fb_login_button_xref = "//*[@id=\"loginbutton\"]"
# gfg_profile_icon_xref = "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div[3]"
gfg_profile_icon_xref = "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div[2]/img" 
gfg_profile_logout_xref = "/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div[3]/div/a[6]"
remind_me_later = "//*[@id=\"lower_section_text\"]"
cursor_location_on_editor = "//*[@class=\"ace_cursor\"]"
code_here_xref = "//span[text() = '// code here']"

log.basicConfig(format='%(asctime)s.%(msecs)03d :: %(name)s :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=log.INFO)
log.info(" ***** Starting automated POTD tool *****")
log.info('We are using selenium version: %s', selenium.__version__)

# creating an instance of web driver
browser = webdriver.Firefox()
potd = get_potd(browser)  
  
def timed(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = datetime.datetime.now()
        result = func(*args, **kwargs)
        t2 = datetime.datetime.now()
        log.info(f'Function {func.__name__} executed in {(t2-t1).total_seconds():.4f}s')
        # print(func.__name__ , t2, t1, (t2-t1).total_seconds())
        return result
    return wrap_func

def lets_click_and_sleep(reference, t):
    reference.click()
    time.sleep(t)

def get_gfg_login_button():
    login_button = browser.find_element('xpath', gfg_login_button_xref)
    if(login_button.text == "Login"):
        log.info('GFG login button found...')
        return login_button
    # Use exception handling on all this.

def get_facebook_button():
    fb_button = browser.find_element('xpath', fb_oauth_button_xref)
    if(fb_button.text == "Facebook"):
        log.info('Fb login button found...')
        return fb_button

@timed
def check_if_need_to_skip():
    time.sleep(1)
    try:
        skip_button = browser.find_element('xpath', remind_me_later)
        lets_click_and_sleep(skip_button, 1)
    except NoSuchElementException:
        log.warning("No need to Skip - Remind me later page not found.")


@timed
def login_to_fb(email, pw):
    email_input = browser.find_element('xpath', fb_email_xref)
    pw_input = browser.find_element('xpath', fb_pw_xref)
    email_input.send_keys(email)
    pw_input.send_keys(pw)
    fb_login = browser.find_element('xpath', fb_login_button_xref)
    lets_click_and_sleep(fb_login, 3)       # final oauth step needs more time.

@timed   
def fb_login_handler():
    # time.sleep(10)
    fb_button = get_facebook_button()
    lets_click_and_sleep(fb_button, 1)
    login_to_fb(creds_mail[i], creds_pw[i])

@timed
def gfg_login_handler():
    gfg_login_button = get_gfg_login_button()
    lets_click_and_sleep(gfg_login_button, 1)
    fb_login_handler()
    check_if_need_to_skip()

@timed
def program_submission_handler():
    time.sleep(3)
    code = browser.find_element('xpath', code_here_xref)
    print(code)
    browser.execute_script('arguments[0].innerHTML = "//Write your code here - may be use chatGPT to get the code";', code)
    time.sleep(5)

@timed
def logout_handler():
    try:
        gfg_profile_icon = browser.find_element('xpath', gfg_profile_icon_xref)
        gfg_profile_icon.click()
        
        gfg_logout_button = browser.find_element('xpath', gfg_profile_logout_xref)
        gfg_logout_button.click()
        log.info("lOGOUT Successful...")
    except NoSuchElementException:
        log.error("Not able to logout - will be closing the browser anyway")


for i in range(len(creds_mail)):
    # browser.switch_to.new_window(WindowTypes.WINDOW)
    if(i != 0):
        browser = webdriver.Firefox()
    browser.get(potd)
    time.sleep(3)
    gfg_login_handler()

    program_submission_handler()

    logout_handler()
    browser.close()
    




# for i in range(len(creds_mail)):

# # Open a new tab in the same window
# browser.switch_to.new_window(WindowTypes.TAB)