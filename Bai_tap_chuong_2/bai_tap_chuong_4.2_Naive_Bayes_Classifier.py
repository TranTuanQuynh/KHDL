# ===============================================
#  NAIVE BAYES CLASSIFIER - DỰ ĐOÁN LOẠI HỘP SỐ XE
# ===============================================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import issparse  
import os 

save_dir = r"C:\code ptit\KHDL\Bai_tap_chuong_2"  
os.makedirs(save_dir, exist_ok=True)

# Đọc dữ liệu từ file CSV thực tế
csv_path = os.path.join(save_dir, 'du_lieu_clean.csv')  
df = pd.read_csv(csv_path)  

print("Shape của dữ liệu:", df.shape)
print("\nPhân bố target (hop_so):")
print(df['hop_so'].value_counts())


features = ['nam_sx', 'so_km', 'kieu_dang', 'xuat_xu', 'nhien_lieu']
X = df[features]
y = df['hop_so']

categorical_features = ['kieu_dang', 'xuat_xu', 'nhien_lieu']
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)],
    remainder='passthrough'  
)

class DenseTransformer:
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.toarray() if issparse(X) else X


pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('dense', DenseTransformer()),  
    ('classifier', GaussianNB())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print("\nĐộ chính xác:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)


plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.show()

new_sample = pd.DataFrame({
    'nam_sx': [2020],
    'so_km': [50000],
    'kieu_dang': ['SUV / Cross over'],
    'xuat_xu': ['Việt Nam'],
    'nhien_lieu': ['Xăng']
})
prediction = pipeline.predict(new_sample)
print("\nDự đoán cho mẫu mới:", prediction[0])