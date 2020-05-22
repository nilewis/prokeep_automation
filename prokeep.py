from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
import logging
import json
import unittest

pgmname = os.path.basename(__file__).split('.')[0]
logname = pgmname + '.log'
logger = logging.getLogger('root')
FORMAT = "%(asctime)12s:Line %(lineno)5s:%(funcName)20s():%(message)s"
logging.basicConfig(filename=logname, filemode='w', format=FORMAT)
logger.setLevel(logging.DEBUG)
logger.debug("Running Prokeep test program")

logger.debug("Setting Chrome Driver options")
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')   
driver = webdriver.Chrome(options=options)
print('')
print("Running Prokeep test program")

class LocalStorage:

    def __init__(self, driver) :
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, items = {}; " \
            "for (var i = 0, k; i < ls.length; ++i) " \
            "  items[k = ls.key(i)] = ls.getItem(k); " \
            "return items; ")

    def keys(self) :
        return self.driver.execute_script( \
            "var ls = window.localStorage, keys = []; " \
            "for (var i = 0; i < ls.length; ++i) " \
            "  keys[i] = ls.key(i); " \
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key) :
        value = self.get(key)
        if value is None :
          raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()

class prokeep(): 
    def __init__(self):
        logger.debug("Running class Login")
        driver.get('https://prokeepelectrical.int.prokeep.com')
        time.sleep(1)

    def login(self,username,password):
        logger.debug("Running login function")
        try:
            url = driver.current_url
            logger.debug("Connected to{}".format(url))
            driver.find_element_by_id("username").clear()
            driver.find_element_by_id("username").send_keys(username)
            driver.find_element_by_id("password").clear()
            driver.find_element_by_id("password").send_keys(password)
            time.sleep(1)
            driver.find_element_by_xpath("/html/body/div/div/div/section[2]/div/div/div[4]/div[1]/button").click()
            time.sleep(1)
            url = driver.current_url
            assert url == 'https://prokeepelectrical.int.prokeep.com/threads/mine',"Assertion error - url redirect after login is not correct\: {}".format(url)
            print("Assertion: Pass - url redirect after login" )
            return(0)
        except Exception as e:
            print("FAILURE: {}".format(e))
            logger.debug("Login Unsuccessful")
            logger.debug("FAILURE: {}".format(e))
            return(100)

    def checkstorage(self):
        try:
            logger.debug("Running check storage function")
            storage = LocalStorage(driver)
            try:
                assert storage["distributor_session"],"Assertion error - distributor_session not found in local storage"
            except:
                raise Exception("Assertion error - distributor_session not found in local storage")
            print("Assertion: Pass - distributor_session present in local storage" )
            j = json.loads(storage["distributor_session"])
            userid=j["currentUser"]['userId']
            idlist = userid.split("-")
            idformat = ""
            for x in idlist:
                idformat += str(len(x))
            assert idformat == '844412',"Assertion error - UUID not in 8-4-4-12 format: {}".format(userid)
            print("Assertion: Pass - UUID 8-4-4-12 format verified" )
            driver.save_screenshot("screenshot.png")
            return(0)
        except Exception as e:
            print("FAILURE: {}".format(e))
            logger.debug("FAILURE: {}".format(e))
            return(100)

    
    def checksettings(self):
        try:
            logger.debug("Running check settings function")  
            driver.find_element_by_xpath('//a[contains(@data-testid,"settings-icon")]').click()
            url = driver.current_url
            assert url == 'https://prokeepelectrical.int.prokeep.com/settings/my-account',"Assertion error - Settings redirect url is not correct\: {}".format(url)
            print("Assertion: Pass - url redirect after clicking settings" )  
            return(0)
        except Exception as e:
            print("FAILURE: {}".format(e))
            logger.debug("FAILURE: {}".format(e))
            return(100)
    
    def logout(self):
        try:
            logger.debug("Running Logout function")  
            driver.find_element_by_xpath('//button[text()="Logout"]').click()
            driver.find_element_by_xpath('//button[text()="Yes"]').click()
            time.sleep(1)
            return(0)
        except Exception as e:
            print("FAILURE: {}".format(e))
            logger.debug("FAILURE: {}".format(e))
            return(100)


    def checkstorage2(self):
        try:
            logger.debug("Running check storage2 function")
            storage = LocalStorage(driver)
            j = json.loads(storage["distributor_session"])
            cuser=j["currentUser"]
            assert cuser == None,"Assertion error - currentUser is not set to null after logout: {}".format(cuser) 
            print("Assertion: Pass - currentUser set to null after logout" )   
            return(0)
        except Exception as e:
            print("FAILURE: {}".format(e))
            logger.debug("FAILURE: {}".format(e))
            return(100)

S = prokeep()
username="jtester@fake.com"
password="2^cnRATJ7W1@"
S.login(username,password)
S.checkstorage()
S.checksettings()
S.logout()
S.checkstorage2()
driver.close()