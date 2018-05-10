from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import getpass
import random
import copy
import time
try:
    import requests
except ImportError:
    import pip
    pip.main(['install', 'requests'])
    import requests

driver = webdriver.Chrome()
driver.implicitly_wait(5)
world = 101
units = {'spear':0, 'sword':0, 'axe':0, 'archer':0, 'spy':0, 'light':0, 'marcher':0, 'heavy':0, 'ram':0, 'catapult':0, 'knight':0, 'snob':0}
setArrivalTimeScript = requests.get("https://raw.githubusercontent.com/kioniv/TW_Tamper_Monkey/master/Set_Arrival_Time").text
username = raw_input("Enter your username: ")
passwd = getpass.getpass("Enter your password: ")

def Login(username, passwd, world):
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

def SendAttack(sendingVillage, targetVillage, arrivalTime, sendUnits):
    # navigate to correct village
    if str(sendingVillage).lower() == "current":
        driver.find_element_by_class_name("village").click()
    else:
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
        driver.execute_async_script(str(setArrivalTimeScript))

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

def SafeSendKeys(target, keys):
    for char in keys:
        RandWait()
        target.send_keys(char)


def NavCombinedOverview():
    driver.get("https://en" + str(world) + ".tribalwars.net/game.php?&screen=overview_villages")

def RandWait():
    time.sleep(random.uniform(.2, .8))

Login(username, passwd, world)

myattack = copy.deepcopy(units)
myattack['spear'] = 1

SendAttack("current", "560|454", "", myattack)
