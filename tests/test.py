import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class Test():
    def setup_method(self, method):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test(self):
        self.login()
        self.check_titles()
        self.add_entrypoint()
        self.select_entrypoint()
        self.clear_entrypoint()
        self.delete_entrypoint()

    def login(self):
        # Open the browser
        self.driver.get('http://localhost:8000')
        self.driver.implicitly_wait(10)

        # Login with dummy credentials
        username = self.driver.find_element_by_id('username_input')
        password = self.driver.find_element_by_id('password_input')

        username.send_keys('admin')
        password.send_keys('admin')

        login_button = self.driver.find_element_by_id('login_submit')
        login_button.click()

        # Open the services tab, then the entrypoint view
        services_button = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Services')]")[0]
        services_button.click()

        entrypoint_button = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'entrypoint')]")[0]
        entrypoint_button.click()

    def check_titles(self):
        # Make sure the page renders with the correct titles
        title = self.driver.find_element_by_id('title')
        assert title.text == 'JupyterHub Entrypoint Service'

        elem = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Manage Conda Entrypoints')]")
        assert len(elem) == 1

        elem = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Selected custom entrypoint for Cori')]")
        assert len(elem) == 1

    def add_entrypoint(self):
        elem = self.driver.find_element_by_id('add-conda-button')
        elem.click()

        path_input = self.driver.find_element_by_id('add-conda-path')
        path_input.send_keys('/envs/my-env')

        name_input = self.driver.find_element_by_id('add-conda-name')
        name_input.send_keys('My Env')

        elem = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'Add entrypoint')]")
        elem.click()

        # put in API calls to check it was added correctly

    def select_entrypoint(self):
        elem = self.driver.find_element_by_id('conda')
        elem.click()

        elem = self.driver.find_element_by_xpath(
            "//option[contains(text(), 'My Env')]")
        elem.click()

        elem = self.driver.find_element_by_id('select-conda-button')
        elem.click()

        # make an API call to test it was set correctly
        elem = self.driver.find_element_by_id('current-entrypoint')
        assert 'Conda: My Env' in elem.text

    def clear_entrypoint(self):
        elem = self.driver.find_element_by_id('clear-selection-button')
        elem.click()

        # check that the entrypoint was cleared
        elem = self.driver.find_element_by_id('current-entrypoint')
        assert elem.text == 'None'

    def delete_entrypoint(self):
        elem = self.driver.find_element_by_id('conda')
        elem.click()

        elem = self.driver.find_element_by_xpath(
            "//option[contains(text(), 'My Env')]")
        elem.click()

        elem = self.driver.find_element_by_xpath(
            "//button[contains(text(), 'delete')]")
        elem.click()

        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()

        # make an API call to test it was deleted correctly
