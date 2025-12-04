from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

options = Options()
options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"

service = Service(r"C:/Users/user/Desktop/ma nguon mo/firefox/geckodriver.exe")  # đảm bảo là phiên bản Windows tương thích

driver = webdriver.Firefox(options=options, service=service)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()
