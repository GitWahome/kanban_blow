from selenium import webdriver
import concurrent.futures

import random
import string
import logging
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S", filename="success")
import os

# To Verify above code


class SeleniumTests:
    def __init__(self, daemon = True):
        self.browser = webdriver.Chrome()
        if daemon:
            options = webdriver.ChromeOptions();
            options.add_argument('headless');

        self.counts=0
        self.success=0

    def site_register(self, uname,em, pass1, confirm_pass):
        self.counts += 1
        self.browser.get("http://127.0.0.1:5000/register")

        username_field = self.browser.find_element_by_id("username")
        username_field.send_keys(uname)

        email_field = self.browser.find_element_by_id("email")
        email_field.send_keys(em)

        password_field = self.browser.find_element_by_id("password")
        password_field.send_keys(pass1)

        confirm_password = self.browser.find_element_by_id("confirm_password")
        confirm_password.send_keys(confirm_pass)

        submit = self.browser.find_element_by_id("submit")
        submit.click()

        confirm = self.browser.current_url == "http://127.0.0.1:5000/login"
        if confirm:
            self.success+=1
            success_message = f"Successfuly Created User: {uname},Password: {pass1}, email {em}"
            logging.info(success_message)
        else:
            fail_message = f"Failed to create user: {uname},Password: {pass1}, email {em}"
            logging.warning(fail_message)
        self.browser.close()


    def run_test(self,workers=50, users=1000):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for i in range(100):

                chars = "".join([random.choice(string.ascii_letters) for i in range(10)])
                un =chars

                digits = "".join([random.choice(string.digits) for i in range(5)])
                chars = "".join([random.choice(string.ascii_letters) for i in range(5)])
                w = digits + chars
                emt =w

                digits = "".join([random.choice(string.digits) for i in range(5)])
                chars = "".join([random.choice(string.ascii_letters) for i in range(8)])
                w = digits + chars
                p1 = w
                p2 = p1
                executor.submit(self.site_register, un, f"{emt}@email.com", p1,p2)

    def __str__(self):
        mess = f"Total number of tests:{self.counts}, " \
               f"Successes: {self.success}, Failures: " \
               f"{self.counts-self.success}, " \
               f"Failure rate:{(self.counts-self.success)/self.counts}%"
        return mess


new_test = SeleniumTests(daemon = True)
new_test.run_test(workers=50, users=1000)
print(new_test)