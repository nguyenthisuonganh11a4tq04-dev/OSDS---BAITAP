from selenium import webdriver
from selenium.webdriver.common.by import By
import time
# Khởi tạo Webdriver
driver = webdriver.Chrome ()
#Mỏ trang
url="https://en.wikipedia.org/wiki/List of painters by name beginning with %22P%22"
driver.get(url)
# Đợi một chút để trang tải
time.sleep (2)
#Lay ra tat cac ca the ul
ul_tags = driver.find_elements(By.TAG_NAME, "ul") 
print(len(ul_tags))
# Chon the ul thu 21
ul_painters = ul_tags [20] # list start with index=(0)
# Lay ra tat ca the <li> thuoc ul painters
li_tags = ul_painters.find_elements (By.TAG_NAME, "li")

# Chon the ul thu 21
ul_painters = ul_tags [20] # list start with index=0
#Lay ra tat ca the <li> thuoc ul_painters
li_tags = ul_painters.find_elements (By.TAG_NAME, "li")
#Tao danh sach cac url
links = [tag.find_element(By.TAG_NAME, "a").get_attribute("href") for tag in li_tags]
#Tao danh sach cac url
titles = [tag.find_element(By.TAG_NAME, "a").get_attribute("title") for tag in li_tags]
# In ra url
for link in links:
    print(link)
# In ra title
for title in titles:
    print (title)
# Dong webdrive 
driver.quit()