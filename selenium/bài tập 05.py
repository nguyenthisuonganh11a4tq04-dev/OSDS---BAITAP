from selenium import webdriver
from selenium.webdriver.common.by import By
from pygments.formatters.html import webify
import pandas as pd
import time
import re

# Khởi tạo DataFrame rỗng
d = pd.DataFrame({'name': [], 'birth': [], 'death': [], 'nationality': []})

#Khởi tạo webdriver 
driver = webdriver.Chrome()

#Mở trang
url = "https://en.wikipedia.org/wiki/Edvard_Munch"
driver.get(url)

#Đợi 2 giây
time.sleep(2)



try:
    # Mở trang
    url = "https://en.wikipedia.org/wiki/Edvard_Munch"
    driver.get(url)

    # Chờ infobox của Wikipedia xuất hiện
    wait = WebDriverWait(driver, 10)
    infobox = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table.infobox"))
    )

    # Lấy tên từ tiêu đề infobox (nếu có)
    try:
        name_el = infobox.find_element(By.CSS_SELECTOR, "caption, .infobox-title")
        name = name_el.text.strip()
    except:
        # Fallback: lấy từ tiêu đề trang
        name = driver.find_element(By.ID, "firstHeading").text.strip()

    # Duyệt các hàng trong infobox để tìm birth, death, nationality
    birth = ""
    death = ""
    nationality = ""

    rows = infobox.find_elements(By.CSS_SELECTOR, "tr")
    for row in rows:
        try:
            th = row.find_element(By.CSS_SELECTOR, "th")
            label = th.text.strip().lower()
        except:
            label = ""

        try:
            td = row.find_element(By.CSS_SELECTOR, "td")
            value = td.text.strip()
        except:
            value = ""

        if not label or not value:
            continue

        # Chuẩn hóa nhãn để bắt các biến thể
        if "born" in label or "birth" in label:
            birth = value
        elif "died" in label or "death" in label:
            death = value
        elif "nationality" in label or "citizenship" in label:
            nationality = value

    # Thêm vào DataFrame
    d.loc[len(d)] = {
        "name": name,
        "birth": birth,
        "death": death,
        "nationality": nationality,
    }

    # In kết quả
    print(d)

finally:
    driver.quit()