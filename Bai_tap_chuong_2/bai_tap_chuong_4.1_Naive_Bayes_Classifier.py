# ===============================================
#  NAIVE BAYES CLASSIFIER - DỰ ĐOÁN KIỂU DÁNG XE
# ===============================================

# 1. Import thư viện
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 2. Đọc dữ liệu
df = pd.read_csv(r"C:\code ptit\KHDL\Bai_tap_chuong_2\du_lieu_clean.csv")

# 3. Chọn và tiền xử lý cột
features = ['nam_sx', 'so_km', 'xuat_xu', 'hop_so', 'nhien_lieu', 'tinh_trang']
target = 'kieu_dang'

df = df.dropna(subset=features + [target])

le_dict = {}
for col in ['xuat_xu', 'hop_so', 'nhien_lieu', 'tinh_trang', 'kieu_dang']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le  

# 4. Chia dữ liệu train/test
X = df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 5. Huấn luyện mô hình
model = GaussianNB()
model.fit(X_train, y_train)

# 6. Đánh giá mô hình
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Độ chính xác mô hình: {acc:.2%}")

print("\n=== Báo cáo phân loại ===")
print(classification_report(y_test, y_pred))

# Ma trận nhầm lẫn
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=le_dict['kieu_dang'].classes_,
            yticklabels=le_dict['kieu_dang'].classes_)
plt.xlabel("Dự đoán")
plt.ylabel("Thực tế")
plt.title("Ma trận nhầm lẫn Naive Bayes - Dự đoán kiểu dáng xe")
plt.tight_layout()
plt.show()

# 7. Dự đoán xe mới
new_data = pd.DataFrame([{
    'nam_sx': 2023,
    'so_km': 25000,
    'xuat_xu': le_dict['xuat_xu'].transform(['Việt Nam'])[0],
    'hop_so': le_dict['hop_so'].transform(['Tự động'])[0],
    'nhien_lieu': le_dict['nhien_lieu'].transform(['Xăng'])[0],
    'tinh_trang': le_dict['tinh_trang'].transform(['Đã sử dụng'])[0]
}])

pred = model.predict(new_data)[0]
pred_label = le_dict['kieu_dang'].inverse_transform([pred])[0]
print(f"\n🚗 Dự đoán kiểu dáng xe: {pred_label}")