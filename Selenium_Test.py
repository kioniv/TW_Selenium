from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import getpass
import random
import copy
import time
import requests

driver = webdriver.Chrome()
driver.implicitly_wait(5)
world = 101
units = {'spear':0, 'sword':0, 'axe':0, 'archer':0, 'spy':0, 'light':0, 'marcher':0, 'heavy':0, 'ram':0, 'catapult':0, 'knight':0, 'snob':0}
setArrivalTimeScript = requests.get("https://raw.githubusercontent.com/kioniv/TW_Tamper_Monkey/master/Set_Arrival_Time").text
username = input("Enter your username: ")
passwd = getpass.getpass("Enter your password: ")

def SafeSendKeys(target, keys):
    for char in keys:
        time.sleep(random.uniform(.05, .34))
        target.send_keys(char)

def Login(username, passwd, world):
    driver.get("https://tribalwars.net")
    loginBtn = driver.find_element_by_class_name("btn-login")
    userNameField = driver.find_element_by_name("username")
    passwordField = driver.find_element_by_name("password")
    SafeSendKeys(userNameField, username)
    SafeSendKeys(passwordField, passwd)
    loginBtn.click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "world_button_active")))
    worldBtn = driver.find_elements_by_class_name("world_button_active")
    try:
        for worldEntry in worldBtn:
            if str(world) in worldEntry.text:
                worldEntry.click()
        try:
            driver.find_element_by_class_name("btn-default").click()
        except:
            pass
    except:
        assert driver.find_element_by_id("serverTime")

def SendAttack(sendingVillage, targetVillage, arrivalTime, sendUnits):
    # navigate to correct village
    if str(sendingVillage).lower() != "current":
        NavCombinedOverview()
        RandWait()
        villageList = driver.find_elements_by_class_name("quickedit-label")
        for village in villageList:
            if str(targetVillage) == village.text:
                village.click()

    RandWait()
    driver.get("https://en" + str(world) + ".tribalwars.net/game.php?&screen=place")

    RandWait()
    # enter coordinates
    targetField = driver.find_element_by_class_name("target-input-field")
    SafeSendKeys(targetField, targetVillage)

    RandWait()
    # enter units
    EnterUnits(sendUnits)

    RandWait()
    # press attack
    driver.find_element_by_id("target_attack").click()

    RandWait()
    #
    if arrivalTime != "":
        driver.execute_script(str(setArrivalTimeScript))
        time.sleep(.5)
        milliseconds = arrivalTime[-3:]
        arrivalTime =arrivalTime[:-4]
        driver.find_element_by_id("delayInput").clear()
        driver.find_element_by_id("delayInput").send_keys("0")
        driver.find_element_by_id("delayButton").click()
        driver.find_element_by_id("reloadInput").clear()
        driver.find_element_by_id("reloadInput").send_keys("0")
        driver.find_element_by_id("reloadButton").click()
        driver.find_element_by_id("arrTime").click()

        WebDriverWait(driver, 3).until(expected_conditions.alert_is_present(),
                                        'Timed out waiting for PA creation ' +
                                        'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.send_keys(arrivalTime)
        alert.accept()


        WebDriverWait(driver, 3).until(expected_conditions.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.send_keys(milliseconds)
        alert.accept()

        WebDriverWait(driver, 999999999999).until(expected_conditions.url_changes)
        print ("Sent " + str(sendUnits) + " from " + str(sendingVillage) + " to " + str(targetVillage)
               + "\nArrival set for " + str(arrivalTime) + ":" + str(milliseconds))

    else:
        driver.find_element_by_id("troop_confirm_go").click()



def EnterUnits(sendUnitsDict):
    for key in sendUnitsDict.keys():
        if sendUnitsDict[key] > 0:
            RandWait()
            try:
                unitField = driver.find_element_by_name(str(key).strip())
                SafeSendKeys(unitField, str(sendUnitsDict[key]))
            except:
                pass


def NavCombinedOverview():
    driver.get("https://en" + str(world) + ".tribalwars.net/game.php?&screen=overview_villages")

def RandWait():
    time.sleep(random.uniform(.2, .7))

Login(username, passwd, world)

myAttack = copy.deepcopy(units)
myAttack['spear'] = 1

SendAttack("current", "560|454", "02:43:00:000", myAttack)
