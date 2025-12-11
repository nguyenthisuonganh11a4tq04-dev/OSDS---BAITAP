from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import sqlite3

# Tạo dataframe trống
painters_df = pd.DataFrame(columns=['name', 'birth', 'death', 'nationality'])

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
url = "https://en.wikipedia.org/wiki/List_of_painters_by_name_beginning_with_%22F%22"
driver.get(url)
time.sleep(3)

# Tìm danh sách UL chứa họa sĩ (dựa vào tên Fragonard)
ul_tags = driver.find_elements(By.TAG_NAME, "ul")
ul_painters = None
for ul in ul_tags:
    if "Fragonard" in ul.text:
        ul_painters = ul
        break

if ul_painters is None:
    print("Không tìm thấy danh sách họa sĩ.")
    driver.quit()
    exit()

# Lấy tất cả link họa sĩ
li_tags = ul_painters.find_elements(By.TAG_NAME, "li")
all_links = []
for li in li_tags:
    try:
        link = li.find_element(By.TAG_NAME, "a").get_attribute("href")
        all_links.append(link)
    except:
        pass

# Crawl từng họa sĩ
for count, link in enumerate(all_links):
    if count >= 10:
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
        birth_text = driver.find_element(By.XPATH, 
            "//th[contains(text(),'Born')]/following-sibling::td"
        ).text
        birth_match = re.findall(r'\d{4}|c\.\s*\d{4}', birth_text)
        birth = birth_match[0] if birth_match else ""
    except:
        birth = ""
        birth_text = ""

    # Năm mất
    try:
        death_text = driver.find_element(By.XPATH, 
            "//th[contains(text(),'Died')]/following-sibling::td"
        ).text
        death_match = re.findall(r'\d{4}|c\.\s*\d{4}', death_text)
        death = death_match[0] if death_match else ""
    except:
        death = ""

    # NATIONALITY / CITIZENSHIP
    try:
        citizen = driver.find_element(By.XPATH,
            "//th[contains(text(),'Nationality') or contains(text(),'Citizenship')]/following-sibling::td"
        ).text
    except:
        citizen = ""

    # Nếu không có mục Nationality → lấy từ dòng Born (quốc gia cuối cùng)
    if citizen == "" and isinstance(birth_text, str) and "," in birth_text:
        possible_country = birth_text.split(",")[-1].strip()
        if len(possible_country) >= 3:
            citizen = possible_country

    painters_df.loc[len(painters_df)] = [name, birth, death, citizen]

driver.quit()

# Lưu vào SQLite
conn = sqlite3.connect("painters.db")
cursor = conn.cursor()

#Tạo bảng
cursor.execute("""
CREATE TABLE IF NOT EXISTS painters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    birth TEXT,
    death TEXT,
    nationality TEXT
)
""")

#Thêm dữ liệu vào bảng
sql_insert = """
INSERT INTO painters (name, birth, death, nationality)
VALUES (?, ?, ?, ?)
"""

for row in painters_df.itertuples(index=False):
    cursor.execute(sql_insert, row)

conn.commit()

print("Đã lưu đầy đủ dữ liệu 15 họa sĩ vào SQLite!")

# =========================
# 4. Truy vấn SQL & thống kê
# =========================

TABLE_NAME = "painters" #table_name chỉ là tên biến để tái sử dụng

# 1. Tổng số họa sĩ
cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
total = cursor.fetchone()[0]
print(f"\n1. Tổng số họa sĩ: {total}")

# 2. 5 dòng đầu tiên
cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 5")
print("\n2. 5 dòng đầu tiên:")
for r in cursor.fetchall():
    print(r)

# 3. Quốc tịch duy nhất
cursor.execute(f"SELECT DISTINCT nationality FROM {TABLE_NAME}")
print("\n3. Quốc tịch duy nhất:")
for n in cursor.fetchall():
    print(n[0])

# 4. Họa sĩ tên bắt đầu F
cursor.execute(f"SELECT name FROM {TABLE_NAME} WHERE name LIKE 'F%'")
print("\n4. Họa sĩ tên bắt đầu F:")
for n in cursor.fetchall():
    print(n[0])

# 5. Họa sĩ quốc tịch chứa 'French'
cursor.execute(f"SELECT name, nationality FROM {TABLE_NAME} WHERE nationality LIKE '%French%'")
print("\n5. Họa sĩ quốc tịch chứa 'French':")
for n in cursor.fetchall():
    print(n)

# 6. Họa sĩ không có quốc tịch
cursor.execute(f"SELECT name FROM {TABLE_NAME} WHERE nationality IS NULL OR nationality = ''")
print("\n6. Họa sĩ không có quốc tịch:")
for n in cursor.fetchall():
    print(n[0])

# 7. Họa sĩ có ngày sinh và ngày mất
cursor.execute(f"SELECT name FROM {TABLE_NAME} WHERE birth != '' AND death != ''")
print("\n7. Họa sĩ có ngày sinh và ngày mất:")
for n in cursor.fetchall():
    print(n[0])

# 8. Họa sĩ tên chứa 'Fales'
cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE name LIKE '%Fales%'")
print("\n8. Họa sĩ tên chứa 'Fales':")
for n in cursor.fetchall():
    print(n)

# 9. Sắp xếp A-Z
cursor.execute(f"SELECT name FROM {TABLE_NAME} ORDER BY name ASC")
print("\n9. Họa sĩ A-Z:")
for n in cursor.fetchall():
    print(n[0])

# 10. Nhóm theo quốc tịch
cursor.execute(f"SELECT nationality, COUNT(*) FROM {TABLE_NAME} GROUP BY nationality")
print("\n10. Số lượng họa sĩ theo quốc tịch:")
for n in cursor.fetchall():
    print(n)

# Đóng kết nối
conn.close() 
print("\nĐã đóng kết nối cơ sở dữ liệu.")


    


