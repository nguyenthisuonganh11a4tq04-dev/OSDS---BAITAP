from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook

# =============================
#   FIREFOX + GECKODRIVER
# =============================
gecko_path = r"C:/Users/user/OneDrive/Desktop/ma nguon mo/firefox/geckodriver.exe"
ser = Service(gecko_path)

options = webdriver.firefox.options.Options()
options.binary_location = "C:/Users/user/AppData/Local/Mozilla Firefox/firefox.exe"
options.headless = False
driver = webdriver.Firefox(options=options, service=ser)

wait = WebDriverWait(driver, 10)

# =============================
#       LOGIN WEBSITE
# =============================
driver.get("https://quotes.toscrape.com/login")

wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("myuser")
driver.find_element(By.ID, "password").send_keys("mypassword")
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

print("⏳ Đang đăng nhập...")
time.sleep(2)

if "Logout" in driver.page_source or "logout" in driver.page_source:
    print("✅ ĐĂNG NHẬP THÀNH CÔNG!")
else:
    print("❌ ĐĂNG NHẬP THẤT BẠI!")
    driver.quit()
    exit()

# =============================
#        CÀO QUOTES
# =============================
quotes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "quote")))

data = []  # để lưu tạm vào list

for q in quotes:
    quote_text = q.find_element(By.CLASS_NAME, "text").text
    author = q.find_element(By.CLASS_NAME, "author").text

    tags = q.find_elements(By.CSS_SELECTOR, ".tags a.tag")
    tag_list = ", ".join([t.text for t in tags])

    data.append([quote_text, author, tag_list])

driver.quit()

# =============================
#        LƯU EXCEL
# =============================
wb = Workbook()
ws = wb.active
ws.title = "Quotes"

# Header
ws.append(["Quote", "Author", "Tags"])

# Data rows
for row in data:
    ws.append(row)

# Lưu file
output_path = "quotes_data.xlsx"
wb.save(output_path)

print(f"📁 File Excel đã được lưu thành công: {output_path}")
