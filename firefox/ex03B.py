from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# ======== CẤU HÌNH FIREFOX + GECKODRIVER ========
gecko_path = r"C:/Users/user/OneDrive/Desktop/ma nguon mo/firefox/geckodriver.exe"
ser = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = "C:/Users/user/AppData/Local/Mozilla Firefox/firefox.exe"
options.headless = False

driver = webdriver.Firefox(options=options, service=ser)

#URL LOGIN
url = 'https://quotes.toscrape.com/login'

# MỞ TRANG
driver.get(url)
time.sleep(2)

# TÌM INPUT USERNAME
username_input = driver.find_element(By.XPATH, "//input[@id='username']")
password_input = driver.find_element(By.XPATH, "//input[@id='password']")

# GỬI DỮ LIỆU 
username_input.send_keys("admin")
time.sleep(1)
password_input.send_keys("admin")

time.sleep(2)

#  CLICK LOGIN 
btn_login = driver.find_element(By.XPATH, "//input[@type='submit']")
btn_login.click()

time.sleep(3)

#  KIỂM TRA KẾT QUẢ 
if "Logout" in driver.page_source:
    print(">>> ĐĂNG NHẬP THÀNH CÔNG !!!")
else:
    print(">>> ĐĂNG NHẬP THẤT BẠI !!!")

time.sleep(3)
driver.quit()
