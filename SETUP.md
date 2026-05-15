# 🚀 SETUP - Hướng dẫn Cài đặt Môi trường

## 📋 Mục lục
1. [Tổng quan](#tổng-quan)
2. [Python & Git](#python--git)
3. [Cách 1: Virtual Environment (venv)](#cách-1-virtual-environment-venv-đơn-giản-nhất)
4. [Cách 2: Conda (Tùy chọn)](#cách-2-conda-tùy-chọn)
5. [Cài đặt Dependencies](#cài-đặt-dependencies)
6. [Kiểm tra Cài đặt](#kiểm-tra-cài-đặt)

---

## 🎯 Tổng quan

**Vấn đề:** 
- Cài trực tiếp (`pip install` chung) sẽ ảnh hưởng toàn bộ hệ thống Python
- Dự án này dùng nhiều package lớn (manim, pytorch, ...) có thể xung đột với dự án khác

**Giải pháp:** 
- Tạo **môi trường ảo (Virtual Environment)** riêng cho dự án này
- Cài dependencies vào đó → **an toàn, độc lập, dễ quản lý**

---

## 📥 Python & Git

### ✅ Kiểm tra đã cài chưa:
```bash
python --version      # Phải ≥ 3.9
git --version         # Bất kỳ phiên bản gần đây
```

### ❌ Nếu chưa cài:
- **Python:** https://www.python.org/downloads/ (chọn "Add Python to PATH")
- **Git:** https://git-scm.com/download/win

---

## Cách 1: Virtual Environment (venv) - ĐƠN GIẢN NHẤT ✨

### 📍 Bước 1: Clone hoặc mở dự án
```bash
cd d:\Roo Code    # Hoặc đường dẫn của bạn
```

### 📍 Bước 2: Tạo môi trường ảo
```bash
# Windows:
python -m venv venv

# macOS / Linux:
python3 -m venv venv
```

**Kết quả:** Thư mục `venv/` sẽ được tạo (chứa Python, pip, và dependencies)

### 📍 Bước 3: Activate môi trường ảo

#### Windows:
```bash
venv\Scripts\activate
```
✅ Lúc này command prompt sẽ có `(venv)` ở đầu:
```
(venv) D:\Roo Code>
```

#### macOS / Linux:
```bash
source venv/bin/activate
```

### 📍 Bước 4: Cài đặt tất cả dependencies
```bash
pip install -r requirements.txt
```

Đợi cho đến khi kết thúc (có thể mất vài phút, dependencies khá nặng)

### 📍 Bước 5: Kiểm tra cài đặt
```bash
python -c "import manim; print('✓ Manim OK')"
python -c "import numpy; print('✓ NumPy OK')"
python -c "from gtts import gTTS; print('✓ gTTS OK')"
```

### 📍 Khi muốn tắt môi trường ảo:
```bash
deactivate
```

---

## Cách 2: Conda (Tùy chọn)

Nếu bạn đã cài [Anaconda](https://www.anaconda.com/products/individual) hoặc [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

### 📍 Bước 1: Tạo môi trường Conda
```bash
conda create --name roo_code python=3.11
```

### 📍 Bước 2: Activate
```bash
conda activate roo_code
```

### 📍 Bước 3: Cài dependencies
```bash
pip install -r requirements.txt
```

### 📍 Khi muốn tắt:
```bash
conda deactivate
```

---

## 🔧 Cài đặt Dependencies

### ✅ Cài tất cả cùng lúc (RECOMMENDED):
```bash
pip install -r requirements.txt
```

### ⚙️ Hoặc cài từng package (nếu muốn chi tiết):
```bash
pip install manim==0.18.0
pip install manim-voiceover>=0.3.4
pip install gTTS>=2.2.4
pip install googletrans>=4.0.0
# ... v.v
```

### 📦 Xem những gì đã cài:
```bash
pip list
```

---

## ✔️ Kiểm tra Cài đặt

### 1️⃣ Kiểm tra từng package:
```bash
# Manim
python -c "from manim import *; print('✓ Manim')"

# Manim Voiceover
python -c "from manim_voiceover import VoiceoverScene; print('✓ Manim Voiceover')"

# gTTS (quan trọng!)
python -c "from gtts import gTTS; print('✓ gTTS')"

# NumPy
python -c "import numpy; print('✓ NumPy')"

# Pillow
python -c "from PIL import Image; print('✓ Pillow')"
```

### 2️⃣ Chạy một Script test:
```bash
# Từ thư mục dự án (với venv activated):
python scripts/Scene2.py -pql
```

**Lệnh này sẽ:**
- `-p`: Preview (mở preview video)
- `-q`: Quiet (ít log)
- `-l`: Low quality (nhanh, chất lượng thấp, dùng để test)

---

## 🆘 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'manim'"
**Nguyên nhân:** Chưa activate venv hoặc dependencies chưa cài

**Cách sửa:**
```bash
# Kiểm tra venv có activate không (có (venv) ở đầu không?)
# Nếu không, chạy:
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux

# Rồi cài lại:
pip install -r requirements.txt
```

### ❌ "ImportError: cannot import name 'GTTSService'"
**Nguyên nhân:** Thiếu gTTS

**Cách sửa:**
```bash
pip install gTTS>=2.2.4
```

### ❌ "Module 'googletrans' not found"
**Nguyên nhân:** Thiếu googletrans

**Cách sửa:**
```bash
pip install googletrans>=4.0.0
```

### ❌ venv chậm hoặc bị lỗi
**Cách sửa:** Xóa venv cũ và tạo lại
```bash
rmdir /s venv                    # Windows
rm -rf venv                      # macOS/Linux

python -m venv venv
venv\Scripts\activate            # Windows hoặc source venv/bin/activate
pip install -r requirements.txt
```

---

## 💡 Mẹo

### 1️⃣ Lưu danh sách dependencies (sau khi cài mới):
```bash
pip freeze > requirements.txt
```

### 2️⃣ Xóa packages không dùng:
```bash
pip uninstall package_name
```

### 3️⃣ Upgrade pip (tùy chọn):
```bash
python -m pip install --upgrade pip
```

### 4️⃣ Cài dependencies khi collaborate:
Mỗi người clone repo mới đều chạy:
```bash
pip install -r requirements.txt
```
**Tất cả sẽ có đúng cùng phiên bản dependencies!**

---

## ✨ Kết luận

| Phương pháp | Ưu điểm | Nhược điểm |
|-----------|---------|-----------|
| **venv** | Đơn giản, built-in Python | Chỉ cho 1 dự án |
| **Conda** | Dễ quản lý nhiều phiên bản Python | Cần cài Anaconda |
| **Cài trực tiếp** | Nhanh | ⚠️ Rủi ro xung đột |

**👉 Khuyến cáo:** Dùng **venv** cho dự án này - đơn giản và đủ!

---

**Bạn có câu hỏi? Hỏi tôi! 😊**
