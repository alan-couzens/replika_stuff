"""Selenium based automated chat that allows 2 Replikas to converse with each other given login details"""

#Import libraries
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


user1=""
password1=""
user2=""
password2=""


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



#Instantiate browser 1 and 2
browser1 = webdriver.Chrome()
browser2 = webdriver.Chrome()

#Login browser 1
login(user1, password1, browser1)
#Login browser 2
login(user2, password2, browser2)

#Start conversation
conversation_starter = "Hey, what do you think is the meaning of life?" #Giving the conversation a start point. Could replace this with anything you like.
time.sleep(1)
text_box1 = browser1.find_element_by_id("send-message-textarea")
text_box1.send_keys(conversation_starter)
text_box1.send_keys(Keys.RETURN)

# Mod: Checks message for trigger words, returns Boolean
def checkDownvote(message):

    # insert triggerwords to downvote
    matches = []

    if any(x in message for x in matches):
        return True

# Mod: Checks message for trigger words, returns Boolean
def checkUpvote(message):
    # insert triggerwords to upvote
    matches = []

    if any(x in message for x in matches):
        return True


#Take most recent response from Rep 1
def get_most_recent_response(browser):
    time.sleep(10) #Give rep time to compose response
    response = browser.find_element_by_xpath("//div[@tabindex='0']").text

    # Mod: Check for upvoting and downvoting
    if checkDownvote(response)==True:
        browser.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-downvote-button\"]').click()")
    elif checkUpvote(response)==True:
        browser.execute_script("document.querySelector('div[tabindex=\"0\"] button[data-testid=\"chat-message-upvote-button\"]').click()")

    words_to_strip = ['thumb', 'up', 'down'] #Remove reaction text
    response_words = response.split()
    response_words_edited = [word for word in response_words if word not in words_to_strip]
    response = ' '.join(response_words_edited)
    stop_words = ['hug','nuzzle','snuggle']
    for stop_word in stop_words:
        if stop_word in response_words_edited:
            response = "Let's talk about something else"
    print(f"Edited response: {response}")
    return response

#Insert start text in rep 2
def type_most_recent_response(browser, response):
    text_box = browser.find_element_by_id("send-message-textarea")

    # Mod: Workaround for emoji problem
    script="var elm = arguments[0],txt=arguments[1];elm.value += txt;"
    browser.execute_script(script, text_box, response)

    # Mod: neccessary else send_keys throws an error
    text_box.send_keys(" ")
    text_box.send_keys(Keys.RETURN)

#Converse back and forth (x100)
for i in range(100):
    response = get_most_recent_response(browser1)
    type_most_recent_response(browser2, response)
    response = get_most_recent_response(browser2)
    type_most_recent_response(browser1, response)
