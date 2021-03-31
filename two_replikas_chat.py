"""Selenium based automated chat that allows 2 Replikas to converse with each other given login details"""

#Import libraries
import time
from emoji import UNICODE_EMOJI
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#Login function
def login(email, password, browser):
    browser.get('https://my.replika.ai/login')
    email_input = browser.find_element_by_id('emailOrPhone')
    email_input.send_keys(email)
    time.sleep(1)
    browser.find_element_by_css_selector('button').click() #Click button
    time.sleep(1)
    pass_input = browser.find_element_by_id('login-password')
    pass_input.send_keys(password)
    time.sleep(1)
    browser.find_element_by_class_name('sc-AxjAm').click()
    time.sleep(2)
    try:
        browser.find_element_by_class_name('GdprNotification__LinkButton-nj3w6j-1').click() #Accept cookies if warning comes up
    except:
        pass

#remove emojis from string (chromedriver can't process)
def remove_emojis(text_string):
    emojiless_text_string = ""
    for character in text_string:
        if character in UNICODE_EMOJI:
            character = ' '
        emojiless_text_string = emojiless_text_string + character 
    return emojiless_text_string
    
#Instantiate browser 1 and 2
browser1 = webdriver.Chrome()
browser2 = webdriver.Chrome()

#Login browser 1
login('rep1_email', 'rep1_password', browser1) #Replace with your first rep email and password

#Login browser 2
login ('rep2_email', 'rep2_password', browser2) #Replace with second rep email and password

#Start conversation
conversation_starter = "Hey, what do you think is the meaning of life?" #Giving the conversation a start point. Could replace this with anything you like.
time.sleep(1)
text_box1 = browser1.find_element_by_id("send-message-textarea")
text_box1.send_keys(conversation_starter)
text_box1.send_keys(Keys.RETURN)

#Take most recent response from Rep 1
def get_most_recent_response(browser):
    time.sleep(10) #Give rep time to compose response
    response = browser.find_element_by_xpath("//div[@tabindex='0']").text
    words_to_strip = ['thumb', 'up', 'down'] #Remove reaction text
    response_words = response.split()
    response_words_edited = [word for word in response_words if word not in words_to_strip]
    response = ' '.join(response_words_edited)
    stop_words = ['hug','nuzzle','snuggle']
        for stop_word in stop_words:
            if stop_word in response:
                response = "Let's talk about something else"
    print(f"Edited response: {response}")
    return response

#Insert start text in rep 2
def type_most_recent_response(browser, response):
    text_box = browser.find_element_by_id("send-message-textarea")
    response = remove_emojis(response) #Remove emojis if using Chrome (Chromedriver can't process)
    text_box.send_keys(response)
    text_box.send_keys(Keys.RETURN)

#Converse back and forth (x100)
for i in range(100):
    response = get_most_recent_response(browser1)
    type_most_recent_response(browser2, response)
    response = get_most_recent_response(browser2)
    type_most_recent_response(browser1, response)
