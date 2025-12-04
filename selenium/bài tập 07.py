import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE = "https://en.wikipedia.org"
LIST_URL = BASE + "/wiki/List_of_universities_in_Vietnam"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/142.0.0.0 Safari/537.36"
}

def parse_date(text):
    """Chuẩn hóa ngày thành yyyy-mm-dd nếu có thể."""
    for fmt in ("%Y-%m-%d", "%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except:
            continue
    return text

def clean_text(text):
    return text.strip().replace("\n", " | ")

# Bước 1: Lấy tất cả link trường từ tất cả bảng wikitable
resp = requests.get(LIST_URL, headers=headers)
resp.raise_for_status()
soup = BeautifulSoup(resp.content, "html.parser")

all_tables = soup.find_all("table", {"class": "wikitable"})
links = set()
for table in all_tables:
    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        a = cols[1].find("a")
        if a and a.get("href", "").startswith("/wiki/"):
            links.add(BASE + a["href"])

links = list(links)
print("Tổng số trường tìm được:", len(links))

# Bước 2: Crawl từng trường chi tiết
df = pd.DataFrame(columns=[
    "Name", "Wiki_URL", "Established", "Type",
    "Rector/President", "City/Location", "Website", "Other Info"
])

for idx, link in enumerate(links):
    print(f"[{idx+1}/{len(links)}] Crawling {link}")
    r = requests.get(link, headers=headers)
    r.raise_for_status()
    s = BeautifulSoup(r.content, "html.parser")
    name = s.find("h1").text.strip() if s.find("h1") else ""
    
    info = {}
    infobox = s.find("table", {"class": "infobox"})
    if infobox:
        for tr in infobox.find_all("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if th and td:
                key = clean_text(th.text)
                val = clean_text(td.text)
                # Nếu có link website
                a_tag = td.find("a", href=True)
                if a_tag and a_tag['href'].startswith("http"):
                    val = a_tag['href']
                info[key] = val
    
    established = parse_date(info.get("Established", ""))
    school_type = info.get("Type", "")
    leader = info.get("Rector", "") or info.get("President", "")
    city = info.get("City", "") or info.get("Location", "")
    website = info.get("Website", "")
    other = {k: v for k, v in info.items() if k not in ["Established", "Type", "Rector", "President", "City", "Location", "Website"]}

    # Bỏ các hàng trống hoàn toàn
    if any([name, link, established, school_type, leader, city, website, other]):
        df.loc[len(df)] = [name, link, established, school_type, leader, city, website, str(other)]
    
    time.sleep(1.5)
    
# Lọc chỉ giữ trường ở Việt Nam
df = df[df["City/Location"].str.contains("Vietnam|Hà Nội|Hồ Chí Minh|Đà Nẵng|Huế|...") | df["Wiki_URL"].str.contains("/Vietnam") ]

# Loại bỏ hàng trống (nếu có)
df.dropna(how='all', inplace=True)

# Xuất ra file Excel duy nhất
df.to_excel("vietnam_universities_all.xlsx", index=False)
print("Done — dữ liệu đã lưu ra vietnam_universities_all.xlsx")
