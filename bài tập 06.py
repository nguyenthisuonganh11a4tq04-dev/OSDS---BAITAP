from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

# =========================
# Cấu hình
# =========================
MAX_COUNT = 5  # Số họa sĩ muốn lấy
URL = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22F%22"

# =========================
# Khởi tạo DataFrame
# =========================
painters_df = pd.DataFrame(columns=['name', 'birth', 'death', 'nationality'])

# =========================
# Khởi tạo trình duyệt
# =========================
driver = webdriver.Chrome()
driver.get(URL)
time.sleep(2)

# =========================
# Tìm danh sách họa sĩ
# =========================
ul_tags = driver.find_elements(By.TAG_NAME, "ul")
ul_painters = None
for ul in ul_tags:
    if "Fragonard" in ul.text:
        ul_painters = ul
        break

if ul_painters is None:
    print("Could not find the painters list.")
    driver.quit()
    exit()

li_tags = ul_painters.find_elements(By.TAG_NAME, "li")

# Lấy link tới trang họa sĩ
all_links = []
for li in li_tags:
    try:
        link = li.find_element(By.TAG_NAME, "a").get_attribute("href")
        all_links.append(link)
    except:
        continue

# =========================
# Lấy thông tin từng họa sĩ
# =========================
for count, link in enumerate(all_links):
    if count >= MAX_COUNT:
        break

    driver.get(link)
    time.sleep(2)

    # Tên
    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        name = ""

    # Năm sinh
    try:
        birth_text = driver.find_element(By.XPATH, "//th[text()='Born']/following-sibling::td").text
        birth_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', birth_text)
        birth = birth_match[0] if birth_match else ""
    except:
        birth = ""

    # Năm mất
    try:
        death_text = driver.find_element(By.XPATH, "//th[text()='Died']/following-sibling::td").text
        death_match = re.findall(r'\d{1,2}\s[A-Za-z]+\s\d{4}|\d{4}', death_text)
        death = death_match[0] if death_match else ""
    except:
        death = ""

    # Quốc tịch
    try:
        try:
            nationality = driver.find_element(By.XPATH, "//th[text()='Nationality']/following-sibling::td").text
        except:
            nationality = driver.find_element(By.XPATH, "//th[text()='Citizenship']/following-sibling::td").text
    except:
        nationality = ""

    painters_df.loc[len(painters_df)] = [name, birth, death, nationality]

driver.quit()

# =========================
# Xuất ra Excel
# =========================
file_name = 'Painter.xlsx'
painters_df.to_excel(file_name, index=False)
print('DataFrame đã được ghi ra Excel thành công.')
