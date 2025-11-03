from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import os
import pandas as pd  

save_dir = r"C:\code ptit\KHDL\Bai_tap_chuong_2"
os.makedirs(save_dir, exist_ok=True)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

start_page = 106  
end_page = 150

csv_path = os.path.join(save_dir, "du_lieu_xe_chotot_fixed.csv")
existing_links = set()
if os.path.exists(csv_path):
    df_old = pd.read_csv(csv_path)
    existing_links = set(df_old['link'].tolist())  
    print(f"Đã đọc {len(existing_links)} links cũ từ CSV.")
else:
    print("Không tìm thấy CSV cũ, crawl từ đầu.")

all_links = []
new_links = []  

for page in range(start_page, end_page + 1):
    url = f"https://xe.chotot.com/mua-ban-oto-ha-noi?page={page}"
    print(f"Đang tải trang {url}")
    driver.get(url)
    time.sleep(4)  
    soup = BeautifulSoup(driver.page_source, "html.parser")
    divs = soup.find_all("div", class_="crd7gu7")
    print(f"   → Tìm thấy {len(divs)} div chứa tin đăng.")
    for div in divs:
        a = div.find("a", href=True)
        if a:
            full_link = "https://xe.chotot.com" + a["href"]
            all_links.append(full_link)
            if full_link not in existing_links:  
                new_links.append(full_link)

print(f"Thu thập {len(all_links)} links tổng, {len(new_links)} links mới.")

print("Bắt đầu crawl dữ liệu chi tiết cho links mới...")
data_rows_new = [] 
for idx, full_link in enumerate(new_links, 1):  
    print(f"    Đang xử lý link mới {idx}/{len(new_links)}: {full_link}")
    try:
        driver.get(full_link)
        time.sleep(5) 
        
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        nam_sx_elem = soup.find("span", {"itemprop": "mfdate"})
        nam_sx = nam_sx_elem.text.strip() if nam_sx_elem else ""
        
        xuat_xu_elem = soup.find("span", {"itemprop": "carorigin"})
        xuat_xu = xuat_xu_elem.text.strip() if xuat_xu_elem else ""
        
        kieu_dang_elem = soup.find("span", {"itemprop": "cartype"})
        kieu_dang = kieu_dang_elem.text.strip() if kieu_dang_elem else ""
        
        so_km_elem = soup.find("span", {"itemprop": "mileage_v2"})
        so_km = so_km_elem.text.strip() if so_km_elem else ""
        
        hop_so_elem = soup.find("span", {"itemprop": "gearbox"})
        hop_so = hop_so_elem.text.strip() if hop_so_elem else ""
        
        tinh_trang_elem = soup.find("span", {"itemprop": "condition_ad"})
        tinh_trang = tinh_trang_elem.text.strip() if tinh_trang_elem else ""
        
        nhien_lieu_elem = soup.find("span", {"itemprop": "fuel"})
        nhien_lieu = nhien_lieu_elem.text.strip() if nhien_lieu_elem else ""
        
        dia_diem_elem = soup.find("span", class_="bwq0cbs flex-1")
        dia_diem = dia_diem_elem.text.strip() if dia_diem_elem else ""
        
        ngay_dang = ""
        all_bwq_spans = soup.find_all("span", class_="bwq0cbs")
        for span in all_bwq_spans:
            span_text = span.get_text(strip=True)
            if "Đăng" in span_text and any(word in span_text for word in ["giờ", "ngày", "tháng", "tuần", "phút"]):
                ngay_dang = span_text
                break
        
        # Thêm row mới
        data_rows_new.append([
            full_link, ngay_dang, nam_sx, xuat_xu, dia_diem,
            kieu_dang, so_km, hop_so, tinh_trang, nhien_lieu
        ])
        
        print(f"      ✓ Ngày đăng: '{ngay_dang}' | Địa điểm: '{dia_diem}' | Năm SX: '{nam_sx}' | ...")  # Debug ngắn
        
    except Exception as e:
        print(f"      ❌ Lỗi: {e}")
        data_rows_new.append([full_link, "", "", "", "", "", "", "", "", ""])

driver.quit()

# 2: Append data mới vào CSV 
if data_rows_new:
    with open(csv_path, "a", newline="", encoding="utf-8") as f:  # "a" = append
        writer = csv.writer(f)
        writer.writerows(data_rows_new) 
    print(f"Đã thêm {len(data_rows_new)} rows mới vào CSV: {csv_path}")
    print(f"Tổng rows hiện tại: {len(pd.read_csv(csv_path))}")
else:
    print("Không có links mới, CSV giữ nguyên.")