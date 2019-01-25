from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://192.168.255.1/#/software/update")
username = driver.find_element_by_name("userName")
username.send_keys("Nemuadmin")
password = driver.find_element_by_name("password")
password.send_keys("nemuuser")
# time.sleep(30)
submitbutton = driver.find_element_by_xpath("/html/body/main-view/div/div[1]/div[1]/ng-view/div/form/div[4]/div[1]/div/ui-button[1]/button")
submitbutton.click()

time.sleep(30)
confirm = driver.find_element_by_xpath("/html/body/div[1]/div/div/ui-modal-renderer/login-banner-modal/ui-modal/div/div/div[3]/div/ui-footer/div/ui-button[1]/button")
confirm.click()


driver.get("https://192.168.255.1/#/software/update")


filebutton = driver.find_element_by_xpath("/html/body/main-view/div/div[1]/div[2]/ng-view/wf-panel/wf-panel-section/div/div/software-management/wf-tabs/div/wf-pane[2]/div/div/div/div[1]/software-update/div/div[2]/div[1]/open-software-local/div/div/ui-file-input/ui-button/button")
filebutton.click()



