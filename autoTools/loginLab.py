import os
from selenium import webdriver

def login(username, password):
    driver = webdriver.Chrome()
    driver.get("https://10.68.148.38/dana-na/auth/url_default/welcome.cgi")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("btnSubmit_6").click()












if __name__ =="__main__":
    username = "shuyu@nsn-intra"
    password = "82851689Ysq"
    login(username, password)






