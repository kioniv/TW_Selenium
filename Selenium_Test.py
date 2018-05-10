from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import getpass

driver = webdriver.Chrome()
world = 100
username = raw_input("Enter your username: ")
passwd = getpass.getpass("Enter your password: ")

def login(driver, username, passwd, world):
    driver.get("https://tribalwars.net")
    loginBtn = driver.find_element_by_class_name("btn-login")
    userNameField = driver.find_element_by_name("username")
    passwordField = driver.find_element_by_name("password")
    userNameField.send_keys(username)
    passwordField.send_keys(passwd)
    loginBtn.click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "world_button_active")))
    worldBtn = driver.find_elements_by_class_name("world_button_active")
    try:
        for worldEntry in worldBtn:
            if str(world) in worldEntry.text:
                worldEntry.click()
    except:
        assert driver.find_element_by_id("serverTime")

login(driver, username, passwd, world)