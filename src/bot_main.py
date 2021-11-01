from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from fuzzywuzzy import fuzz
import time
from datetime import datetime
import os
import pathlib

waitForDrop = True

links = {
    "t-shirt": "https://www.supremenewyork.com/shop/all/t-shirts",
    "jacket": "https://www.supremenewyork.com/shop/all/jackets",
    "shirt": "https://www.supremenewyork.com/shop/all/shirts",
    "sweater": "https://www.supremenewyork.com/shop/all/tops_sweaters",
    "pant": "https://www.supremenewyork.com/shop/all/pants",
    "bag": "https://www.supremenewyork.com/shop/all/bags",
    "accessory": "https://www.supremenewyork.com/shop/all/accessories",
    "shoe": "https://www.supremenewyork.com/shop/all/shoes"
}


def cart_item(current_item, current_user, sDriver):
    pauseTime = .25
    interactable = False
    itemFound = False

    if waitForDrop:
        hour = int(datetime.now().time().hour)
        minute = int(datetime.now().time().minute)
        second = int(datetime.now().time().second)
        if hour >= 11 and minute > 0:
            seconds = 60 - second
            minute += 1
            minutes = 60 - minute
            hour += 1
            hours = 35 - hour
            waitTime = seconds + (minute * 60) + (hours * 3600)
            print("Hours : " + str(hours) + "\nMinutes : " + str(minutes) + "\nSeconds : " + str(seconds) + "\nWaiting " + str(waitTime) + " econds")
            time.sleep(waitTime)
        else:
            seconds = 60 - second
            minute += 1
            minutes = 60 - minute
            hour += 1
            hours = 11 - hour
            waitTime = seconds + (minute * 60) + (hours * 3600)
            print("Hours : " + str(hours) + "\nMinutes : " + str(minutes) + "\nSeconds : " + str(seconds) + "\nWaiting " + str(waitTime) + " econds")
            time.sleep(waitTime)
    try:
        if sDriver == "Safari":
            driver = webdriver.Safari()
        if sDriver == "Chrome":
            driver = webdriver.Chrome()
        if sDriver == "Firefox":
            driver = webdriver.Firefox()
        if sDriver == "Internet Explorer":
            driver = webdriver.Ie()
    except:
        print("Oops something went wrong while setting the webserver!\nCheck to make sure the option is valid!")

    # once we've located the item using beautiful soup and requests we then begin to interact
    # with the items webpage using selenium
    while itemFound == False:
        try:
            foundLink = _fuzzy_find(current_item)
            driver.get(foundLink)
            itemFound = True
        except:
            print("Oops something went wrong while navigating to the given item link!\nRetrying!")

    while interactable == False:
        try:
            size = "//select[@id='size']/option[text()='" + str(current_item["size"]) + "']"
            driver.find_element_by_xpath(size).click()
            time.sleep(pauseTime)

            # the bot then adds item to the cart
            (driver.find_elements_by_xpath("//input[@name='commit' and @value='add to cart']")[0]).click()
            time.sleep(pauseTime)

            # clicks the checkout button that redirects the bot to the checkout page
            (driver.find_elements_by_xpath(
                "//a[@class='button checkout' and @href='https://www.supremenewyork.com/checkout']")[0]).click()
            interactable = True
        except:
            print("Page wasn't loaded when interaction began, adding to wait time.")
            pauseTime += .1

    _sendCustomerInfo(current_user, driver)


def _fuzzy_find(current_item):
    page_items = []

    current_item_index = 0
    max_sim = 0
    url = links[current_item["type"]]

    # gets given webpage
    origin = requests.get(url)

    # grabs html of the page
    soup = BeautifulSoup(origin.content, "html.parser")

    # finds the container that has all of the item links
    items = soup.find(id="container")

    # locates the actual items within the container
    info = items.find_all("div", class_="inner-article")

    for bits in info:
        labels = bits.find_all("a", class_="name-link")
        obtained_link = False

        for specifics in labels:
            current_item_color = specifics.text

            # if we don't have the items link we grab it
            if not obtained_link:
                current_item_name = specifics.text
                link_url = specifics["href"]
                link_url = "https://www.supremenewyork.com" + link_url
                obtained_link = True

        name_similarity = fuzz.ratio(current_item["name"].lower(), current_item_name.lower())
        color_similarity = fuzz.ratio(current_item["color_way"].lower(), current_item_color.lower())

        # Calculates one similarity value based off of the similarities of an items color and name
        general_similarity = (name_similarity + color_similarity) / 2
        if general_similarity > max_sim:
            max_index = current_item_index
            max_sim = general_similarity

        page_items.append([current_item_color, current_item_name, link_url, general_similarity])

        current_item_index = current_item_index + 1
    foundLink = page_items[max_index][2]
    return foundLink


def _sendCustomerInfo(customerInfo, driver):
    pauseTime = .25
    success = False

    while success == False:
        try:
            time.sleep(pauseTime)

            driver.find_element_by_id('order_billing_name').send_keys(customerInfo["name"])

            driver.find_element_by_id('order_email').send_keys(customerInfo["email"])

            driver.find_element_by_id('order_tel').send_keys(customerInfo["phone"])

            driver.find_element_by_id('order_billing_address').send_keys(customerInfo["address"])

            driver.find_element_by_id('order_billing_zip').send_keys(customerInfo["zipCode"])

            driver.find_element_by_id('order_billing_city').send_keys(customerInfo["city"])

            driver.find_element_by_id('credit_card_number').send_keys(customerInfo["cardNumber"])

            driver.find_element_by_id('credit_card_verification_value').send_keys(customerInfo["cvv"])

            creditMonth = "//select[@id='credit_card_month']/option[text()='" + str(customerInfo["month"]) + "']"
            driver.find_element_by_xpath(creditMonth).click()

            creditYear = "//select[@id='credit_card_year']/option[text()='" + str(customerInfo["year"]) + "']"
            driver.find_element_by_xpath(creditYear).click()

            time.sleep(5)
            # driver.find_element_by_id('order_terms').click()

            success = True
        except:
            print("Oops something went wrong while trying to send the users credentials!\nRetrying with increased wait time!")
            pauseTime += .1

    print("Finished carting item!\nManual Checkout Required!")
