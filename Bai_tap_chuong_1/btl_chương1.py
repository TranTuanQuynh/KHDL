import pandas as pd
import numpy as np
from scipy.stats import t

# Đọc dữ liệu từ file Excel
df = pd.read_excel(r'C:\code ptit\KHDL\Bai_tap_chuong_1\data.xlsx', sheet_name='Sheet1')

# Lọc dữ liệu cho năm 2021 và giới tính
bang_trung_binh_cac_nuoc_2021 = df[
    (df['Period'] == 2021) &
    (df['Dim1'] == 'Both sexes') &
    (df['IndicatorCode'] == 'WHOSIS_000001')
].copy()

# Chuyển cột về số
bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] = pd.to_numeric(
    bang_trung_binh_cac_nuoc_2021['FactValueNumeric'], errors='coerce'
)

# 1. Chuẩn hóa dữ liệu (dùng hàm có sẵn)
trung_binh_toan_cuc = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].mean()
do_lech_chuan_mau = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].std(ddof=1)  # mẫu
do_lech_chuan = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].std(ddof=0)      # tổng thể
phuong_sai_mau = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].var(ddof=1)
phuong_sai = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].var(ddof=0)
so_luong_quoc_gia = bang_trung_binh_cac_nuoc_2021['FactValueNumeric'].count()

# Tính sai lệch và giá trị chuẩn hóa
bang_trung_binh_cac_nuoc_2021['trung_binh_sai_lech'] = (
    bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] - trung_binh_toan_cuc
)
bang_trung_binh_cac_nuoc_2021['gia_tri_chuan_hoa'] = (
    bang_trung_binh_cac_nuoc_2021['FactValueNumeric'] - trung_binh_toan_cuc
) / do_lech_chuan

print(f"Trung bình: {trung_binh_toan_cuc:.2f}")
print(f"Phương sai tổng thể: {phuong_sai:.2f}")
print(f"Phương sai mẫu: {phuong_sai_mau:.2f}")
print(f"Độ lệch chuẩn tổng thể: {do_lech_chuan:.2f}")
print(f"Độ lệch chuẩn mẫu: {do_lech_chuan_mau:.2f}")

# 2. Ước lượng kỳ vọng bằng khoảng tin cậy (dùng hàm)
confidence = 0.95
alpha = 1 - confidence
dfree = so_luong_quoc_gia - 1
sai_so_chuan = do_lech_chuan_mau / np.sqrt(so_luong_quoc_gia)

t_critical = t.ppf(1 - alpha/2, dfree)
margin = t_critical * sai_so_chuan
khoang_tin_cay = (trung_binh_toan_cuc - margin, trung_binh_toan_cuc + margin)

print(f"t critical (95% CI, df={dfree}): {t_critical:.3f}")
print(f"Sai số chuẩn: {sai_so_chuan:.3f}")
print("Khoảng tin cậy 95%:", khoang_tin_cay)

# 3. Kiểm định giả thuyết thống kê cho kỳ vọng (dùng t-test 1 mẫu)
μ0 = 72.0
t_stat = (trung_binh_toan_cuc - μ0) / sai_so_chuan
p_value = 2 * (1 - t.cdf(abs(t_stat), df=so_luong_quoc_gia-1))

print("Giá trị t:", t_stat)
print("p-value:", p_value)
if p_value < alpha:
    print("Bác bỏ H0: μ = 72.0")
else:
    print("Không bác bỏ H0: μ = 72.0")

# Xuất dữ liệu
columns_to_export = ['Location', 'FactValueNumeric', 'trung_binh_sai_lech', 'gia_tri_chuan_hoa']
bang_trung_binh_cac_nuoc_2021[columns_to_export].to_excel(
    r'C:\code ptit\KHDL\Bai_tap_chuong_1\tuoi_tho_trung_binh_cac_nuoc_2021_ketqua.xlsx',
    index=False,
    engine='openpyxl'
)
