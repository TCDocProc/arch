from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.errorhandler import ElementNotVisibleException, \
                                       NoSuchElementException, \
                                       NoAlertPresentException, \
                                       UnexpectedAlertPresentException

from selenium import webdriver

TEST_PASSED = "TEST_PASSED"

class IntegrateTestCase(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        self.selenium.maximize_window()
        super(IntegrateTestCase, self).setUp()

    def tearDown(self):
        # Call tearDown to close the web browser
        self.selenium.quit()
        super(StaticLiveServerTestCase, self).tearDown()
    
    def run_integrate_test(self, testname):
        url = '%s%s' % (self.live_server_url,  "/integrate/")
        test_timeout = 180

        self.selenium.get("%s?test=%s" % (url, testname))
        element = WebDriverWait(self.selenium, test_timeout).until(EC.presence_of_element_located((By.ID, "integrate-test-result")))
        if element.get_attribute("class") != "integrate-test-passed":
            rval = self.selenium.find_element_by_id("integrate-current-step").text
            print "F",
        else:
            rval = TEST_PASSED
            print ".",
        return rval