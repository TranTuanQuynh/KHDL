import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Đường dẫn thư mục
save_dir = r"C:\code ptit\KHDL\Bai_tap_chuong_2"
os.makedirs(save_dir, exist_ok=True) 

# Đọc dữ liệu từ CSV trong thư mục
csv_path = os.path.join(save_dir, "du_lieu_xe_chotot_fixed.csv")
df = pd.read_csv(csv_path)

# Chuyển đổi cột số
df['nam_sx'] = pd.to_numeric(df['nam_sx'], errors='coerce')
df['so_km'] = pd.to_numeric(df['so_km'], errors='coerce')

# Loại bỏ rows NaN ở cột số
df = df.dropna(subset=['nam_sx', 'so_km'])

print("Dữ liệu gốc (preview):")
print(df.head())
print(f"\nTổng số rows: {len(df)}")

# 1. Thống kê mô tả cho cột số
print("\n1. Thống kê mô tả cho cột số:")
print(df[['nam_sx', 'so_km']].describe())

# 2. Thống kê cho cột phân loại (fill missing)
print("\n2. Thống kê cho cột phân loại:")
cat_cols = ['xuat_xu', 'kieu_dang', 'hop_so', 'tinh_trang', 'nhien_lieu']
for col in cat_cols:
    df[col] = df[col].fillna('Unknown').str.strip()
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))

# 3. Phát hiện và xử lý outlier bằng IQR
def detect_and_remove_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][[col, 'link']]
    print(f"\n{col}: Số outlier = {len(outliers)} (giới hạn: {lower_bound:.2f} - {upper_bound:.2f})")
    if len(outliers) > 0:
        print("Outliers (với link):")
        print(outliers.head())
    # Remove outliers
    df_clean = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df_clean

print("\n3. Xử lý outlier:")
for col in ['nam_sx', 'so_km']:
    df = detect_and_remove_outliers(df, col)

print(f"\nRows sau xử lý outliers: {len(df)}")

# Lưu 
clean_path = os.path.join(save_dir, 'du_lieu_clean.csv')
df.to_csv(clean_path, index=False)
print(f"Lưu DF clean: {clean_path}")

# 4. Co giãn chuẩn hóa dữ liệu
num_cols = ['nam_sx', 'so_km']
minmax_scaler = MinMaxScaler()
std_scaler = StandardScaler()
df[['nam_sx_minmax', 'so_km_minmax']] = minmax_scaler.fit_transform(df[num_cols])
df[['nam_sx_std', 'so_km_std']] = std_scaler.fit_transform(df[num_cols])

print("\n4. Thống kê sau chuẩn hóa (MinMax):")
print(df[['nam_sx_minmax', 'so_km_minmax']].describe())
print("\nThống kê sau chuẩn hóa (Standard):")
print(df[['nam_sx_std', 'so_km_std']].describe())

# Correlation matrix
print("\nCorrelation matrix (numeric):")
print(df[num_cols].corr())

# 5. Vẽ các biểu đồ trực quan
# Boxplot và Histogram (numeric)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.boxplot(data=df, y='nam_sx')
plt.title('Boxplot: Năm sản xuất (nam_sx)')

plt.subplot(1, 2, 2)
sns.boxplot(data=df, y='so_km')
plt.title('Boxplot: Số km (so_km)')

plt.tight_layout()
boxplot_path = os.path.join(save_dir, 'boxplot_outliers.png')
plt.savefig(boxplot_path)
plt.show()

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
df['nam_sx'].hist(bins=20, edgecolor='black')
plt.title('Histogram: Năm sản xuất')
plt.xlabel('Năm')

plt.subplot(1, 2, 2)
df['so_km'].hist(bins=20, edgecolor='black')
plt.title('Histogram: Số km')
plt.xlabel('Km')

plt.tight_layout()
hist_path = os.path.join(save_dir, 'histogram_distribution.png')
plt.savefig(hist_path)
plt.show()

# biểu đồ categorical
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.countplot(data=df, x='xuat_xu', order=df['xuat_xu'].value_counts().index[:5])  # Top 5
plt.title('Countplot: Xuất xứ')
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
sns.countplot(data=df, x='kieu_dang', order=df['kieu_dang'].value_counts().index[:5])
plt.title('Countplot: Kiểu dáng')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
df['nhien_lieu'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Pie: Nhiên liệu')

plt.tight_layout()
catplot_path = os.path.join(save_dir, 'categorical_plots.png')
plt.savefig(catplot_path)
plt.show()

print(f"\nHoàn thành! Lưu ảnh PNG: {boxplot_path}, {hist_path}, {catplot_path}")

