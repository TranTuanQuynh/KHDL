from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import csv
import os

# Đường dẫn thư mục lưu file
save_dir = r"C:\code ptit\KHDL\Bai_tap_chuong_2"
os.makedirs(save_dir, exist_ok=True)  

# Thiết lập Chrome headless
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

all_links = []
data_rows = []

# 1: Thu thập links 
for page in range(2, 150):
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

print(f"   Thu thập được {len(all_links)} links.")

# 1.2: Crawl dữ liệu chi tiết từng link
print("Bắt đầu crawl dữ liệu chi tiết...")
for idx, full_link in enumerate(all_links, 1):  
    print(f"   → Đang xử lý link {idx}/{len(all_links)}: {full_link}")
    try:
        driver.get(full_link)
        time.sleep(5) 
        
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Giá xe: class="p26z2wb"
        gia_elem = soup.find("b", class_="p26z2wb")
        gia_xe = gia_elem.text.strip() if gia_elem else ""
        
        # Năm SX: itemprop="mfdate"
        nam_sx_elem = soup.find("span", {"itemprop": "mfdate"})
        nam_sx = nam_sx_elem.text.strip() if nam_sx_elem else ""
        
        # Xuất xứ: itemprop="carorigin"
        xuat_xu_elem = soup.find("span", {"itemprop": "carorigin"})
        xuat_xu = xuat_xu_elem.text.strip() if xuat_xu_elem else ""
        
        # Kiểu dáng: itemprop="cartype"
        kieu_dang_elem = soup.find("span", {"itemprop": "cartype"})
        kieu_dang = kieu_dang_elem.text.strip() if kieu_dang_elem else ""
        
        # Số km: itemprop="mileage_v2"
        so_km_elem = soup.find("span", {"itemprop": "mileage_v2"})
        so_km = so_km_elem.text.strip() if so_km_elem else ""
        
        # Hộp số: itemprop="gearbox"
        hop_so_elem = soup.find("span", {"itemprop": "gearbox"})
        hop_so = hop_so_elem.text.strip() if hop_so_elem else ""
        
        # Tình trạng: itemprop="condition_ad"
        tinh_trang_elem = soup.find("span", {"itemprop": "condition_ad"})
        tinh_trang = tinh_trang_elem.text.strip() if tinh_trang_elem else ""
        
        # Nhiên liệu: itemprop="fuel"
        nhien_lieu_elem = soup.find("span", {"itemprop": "fuel"})
        nhien_lieu = nhien_lieu_elem.text.strip() if nhien_lieu_elem else ""
        
        # ĐỊA ĐIỂM: class="bwq0cbs flex-1" 
        dia_diem_elem = soup.find("span", class_="bwq0cbs flex-1")
        dia_diem = dia_diem_elem.text.strip() if dia_diem_elem else ""
        
        # NGÀY ĐĂNG: Fallback loop 
        ngay_dang = ""
        all_bwq_spans = soup.find_all("span", class_="bwq0cbs")
        for span in all_bwq_spans:
            span_text = span.get_text(strip=True)  # Strip whitespace để an toàn
            if "Đăng" in span_text and any(word in span_text for word in ["giờ", "ngày", "tháng", "tuần", "phút"]):
                ngay_dang = span_text
                break
        
        # Thêm row
        data_rows.append([
            full_link, gia_xe, ngay_dang, nam_sx, xuat_xu, dia_diem,
            kieu_dang, so_km, hop_so, tinh_trang, nhien_lieu
        ])
        
        # Debug 
        print(f"      ✓ Giá: '{gia_xe}' | Ngày đăng: '{ngay_dang}' | Địa điểm: '{dia_diem}' | Năm SX: '{nam_sx}' | Xuất xứ: '{xuat_xu}' | Kiểu dáng: '{kieu_dang}' | Số km: '{so_km}' | Hộp số: '{hop_so}' | Tình trạng: '{tinh_trang}' | Nhiên liệu: '{nhien_lieu}'")
        
    except Exception as e:
        print(f"       Lỗi: {e}")
        data_rows.append([full_link, "", "", "", "", "", "", "", "", "", ""])

driver.quit()

# 2: lưu CSV 
csv_path = os.path.join(save_dir, "du_lieu_xe_chotot_fixed.csv")
header = ["link", "gia_xe", "ngay_dang", "nam_sx", "xuat_xu", "dia_diem", "kieu_dang", "so_km", "hop_so", "tinh_trang", "nhien_lieu"]
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data_rows)

print(f"Tổng rows: {len(data_rows)} - Lưu CSV vào: {csv_path}")