# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, json, httplib, base64, sys


credentials = {"username": "sarora16",
          "access-key": "4bc59e18-9f09-4eb0-b46c-60bdffd6f310"}

base64string = base64.encodestring('%s:%s' % (credentials['username'], credentials['access-key']))[:-1]

class Alationlogin(unittest.TestCase):
    browserName = ""
    platform = ""
    version = ""
    baseUrl = ""
    
    def setUp(self):
        #self.driver = webdriver.Firefox()
        if browserName and platform and version and baseUrl:
            desired_cap = { "baseUrl": baseUrl, "browserName": browserName,"version" : version, "platform": platform }
        else:
            desired_cap = self.getConfig()
        self.driver = webdriver.Remote(command_executor='http://'+ credentials['username']+':'+credentials['access-key']+ '@ondemand.saucelabs.com:80/wd/hub',
                        desired_capabilities=desired_cap)
        self.driver.implicitly_wait(30)
        #self.base_url = "https://shashank.trialalation.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def getConfig(self):
        with open('config.json') as config_file:    
            config_cap = json.load(config_file)

        return config_cap if config_cap else {"browserName": "firefox","platform": "OS X 10.9","version": "45.0", "baseUrl": "https://shashank.trialalation.com/"}


    def test_alationlogin(self):
        driver = self.driver
        driver.get(driver.baseUrl + "login/")
        driver.find_element_by_id("email").clear()
        title = "Alation" 
        assert title == driver.title
        # driver.find_element_by_id("email").send_keys("devops@alation.com")
        # driver.find_element_by_id("password").clear()
        # driver.find_element_by_id("password").send_keys("hHe3k7Lla7zuvKqhbemG")
        # driver.find_element_by_xpath("//button").click()
        # driver.implicitly_wait("5000")
        # title = "Home | Alation"
        # assert title == driver.title
        set_test_status(driver.session_id, passed=(title == driver.title))
    
    # def test_login_failure(self):
    #     driver = self.driver
    #     driver.get(self.base_url + "/login/")
    #     driver.find_element_by_id("email").clear()
    #     title = "Alation" 
    #     assert title == driver.title
    #     driver.find_element_by_id("email").send_keys("devops@test.com")
    #     driver.find_element_by_id("password").clear()
    #     driver.find_element_by_id("password").send_keys("Test@123")
    #     driver.find_element_by_xpath("//button").click()
    #     driver.implicitly_wait("5000")
    #     #title = "Home | Alation"
    #     assert title == driver.title
    #     set_test_status(driver.session_id, passed=(title == driver.title))

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def set_test_status(jobid, passed=True):
    body_content = json.dumps({"passed": passed})
    connection =  httplib.HTTPConnection("saucelabs.com")
    connection.request('PUT', '/rest/v1/%s/jobs/%s' % (credentials['username'], jobid),
                       body_content,
                       headers={"Authorization": "Basic %s" % base64string})
    result = connection.getresponse()
    return result.status == 200


if __name__ == "__main__":
    if len(sys.argv) > 1 and len(sys.argv) == 4:
        unittest.main(baseUrl= sys.argv[1],platform= sys.argv[2],browserName,version= sys.argv[2].split(" "))
    else:
        print(len(sys.argv))
        #unittest.main()
