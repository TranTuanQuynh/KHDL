
import pandas as pd
import numpy as np
import openpyxl
from scipy.stats import t

# Đọc dữ liệu từ file Excel
df = pd.read_excel(r'C:\code ptit\KHDL\data.xlsx', sheet_name='Sheet1')
# Lọc dữ liệu cho năm 2021 và giới tính
bang_trung_binh_cac_nuoc_2021 = df[(df['Period'] == 2021) &(df['Dim1'] == 'Both sexes')&(df['IndicatorCode'] == 'WHOSIS_000001') ].copy()
# Chuyển đổi cột 'FactValueNumeric' sang kiểu số, bỏ qua các giá trị không thể chuyển đổi
bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] = pd.to_numeric(bang_trung_binh_cac_nuoc_2021['FactValueNumeric'], errors='coerce')

# 1.Chuẩn hoa dữ liệu 
# Tính tuổi thọ trung bình của các quốc gia năm 2021 
trung_binh_toan_cuc = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].mean()
# Tính sai lệch so với tuổi thọ trung bình toàn cục
bang_trung_binh_cac_nuoc_2021['trung_binh_sai_lech'] = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] - trung_binh_toan_cuc
# Tính tổng bình phương sai lệch
tong_binh_phuong_sai_lech = np.sum(bang_trung_binh_cac_nuoc_2021['trung_binh_sai_lech'] ** 2)
# Tính số lượng các quốc gia
so_luong_quoc_gia = len(bang_trung_binh_cac_nuoc_2021)
# Tính phương sai tổng thể (n)
phuong_sai = tong_binh_phuong_sai_lech / so_luong_quoc_gia 
# Tính phương sai mẫu (n-1) 
phuong_sai_mau = tong_binh_phuong_sai_lech / (so_luong_quoc_gia - 1)
# Tính độ lệch chuẩn
do_lech_chuan = np.sqrt(phuong_sai)
# Tính độ lệch chuẩn mẫu
do_lech_chuan_mau = np.sqrt(phuong_sai_mau)
# Tính giá trị chuẩn hóa (tuổi thọ - trung bình) / độ lệch chuẩn
bang_trung_binh_cac_nuoc_2021['gia_tri_chuan_hoa'] = (bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] - trung_binh_toan_cuc) / do_lech_chuan

print(f"Trung bình tuổi thọ trung bình của các quốc gia năm 2021: {trung_binh_toan_cuc:.2f}")
print(f"Tổng bình phương sai lệch: {tong_binh_phuong_sai_lech:.2f}")
print(f"Số lượng quốc gia: {so_luong_quoc_gia}")
print(f"Phương sai tổng thể: {phuong_sai:.2f}")
print(f"Độ lệch chuẩn tổng thể: {do_lech_chuan:.2f}")
print(f"Phương sai mẫu: {phuong_sai_mau:.2f}")
print(f"Độ lệch chuẩn mẫu: {do_lech_chuan_mau:.2f}")

# 2.Ước lượng kỳ vọng bằng khoảng tin cậy
# Thông số
confidence = 0.95
alpha = 1 - confidence
df = so_luong_quoc_gia - 1  # n-1

# Tính sai số chuẩn của mẫu
sai_so_chuan = do_lech_chuan_mau / np.sqrt(so_luong_quoc_gia)

# Giá trị t tới hạn hai phía
t_critical = t.ppf(1 - alpha/2, df)
# Tính khoảng tin cậy
khoang = t_critical * sai_so_chuan
khoang_tin_cay = (trung_binh_toan_cuc - khoang, trung_binh_toan_cuc + khoang)

print("t critical (95% CI, df={}):".format(df), t_critical)
print("Sai số chuẩn của mẫu:", sai_so_chuan)
print("Khoảng tin cậy 95% cho tuổi thọ trung bình của các quốc gia năm 2021:", khoang_tin_cay)

# 3.Kiểm định giả thuyết thống kê cho kỳ vọng
# Giả thuyết không H0: μ = 72.0
μ0 = 72.0
t= (trung_binh_toan_cuc - μ0) / sai_so_chuan
print("Giá trị t:", t)
if(abs(t) > t_critical):
    print("Bác bỏ giả thuyết không H0: μ = 72.0")
else:
    print("Không bác bỏ giả thuyết không H0: μ = 72.0")

print(bang_trung_binh_cac_nuoc_2021.head(10))

# Chọn các cột cần xuất
columns_to_export = ['Location', 'FactValueNumeric', 'trung_binh_sai_lech', 'gia_tri_chuan_hoa']
bang_trung_binh_cac_nuoc_2021_export = bang_trung_binh_cac_nuoc_2021[columns_to_export]

# Lưu kết quả vào file Excel
bang_trung_binh_cac_nuoc_2021_export.to_excel(
    r'C:\code ptit\KHDL\tuoi_tho_trung_binh_cac_nuoc_2021.xlsx',
    index=False,
    engine='openpyxl'
)
