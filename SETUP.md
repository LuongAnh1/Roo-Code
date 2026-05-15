# SETUP - Hướng dẫn Cài đặt Môi trường

## Mục lục
1. [Tổng quan](#tổng-quan)
2. [Python & Git](#python--git)
3. [Cách 1: Virtual Environment (venv)](#cách-1-virtual-environment-venv-đơn-giản-nhất)
4. [Cách 2: Conda (Tùy chọn)](#cách-2-conda-tùy-chọn)
5. [Cài đặt Dependencies](#cài-đặt-dependencies)
6. [Kiểm tra Cài đặt](#kiểm-tra-cài-đặt)

---

## Tổng quan

**Vấn đề:**
- Cài trực tiếp (`pip install` chung) sẽ ảnh hưởng toàn bộ hệ thống Python
- Dự án này dùng nhiều package lớn (manim, pytorch, ...) có thể xung đột với dự án khác

**Giải pháp:**
- Tạo **môi trường ảo (Virtual Environment)** riêng cho dự án này
- Cài dependencies vào đó → **an toàn, độc lập, dễ quản lý**

---

## Python & Git

### [OK] Kiểm tra đã cài chưa:
```bash
python --version      # Phải >= 3.9
git --version         # Bất kỳ phiên bản gần đây
```

### [ERROR] Nếu chưa cài:
- **Python:** https://www.python.org/downloads/ (chọn "Add Python to PATH")
- **Git:** https://git-scm.com/download/win

---

## Cách 1: Virtual Environment (venv) - ĐƠN GIẢN NHẤT

### Bước 1: Clone hoặc mở dự án
```bash
cd d:\Roo Code    # Hoặc đường dẫn của bạn
```

### Bước 2: Tạo môi trường ảo
```bash
# Windows:
python -m venv venv

# macOS / Linux:
python3 -m venv venv
```

**Kết quả:** Thư mục `venv/` sẽ được tạo (chứa Python, pip, và dependencies)

### Bước 3: Activate môi trường ảo

#### Windows:
```bash
venv\Scripts\activate
```
[OK] Lúc này command prompt sẽ có `(venv)` ở đầu:
```
(venv) D:\Roo Code>
```

#### macOS / Linux:
```bash
source venv/bin/activate
```

### Bước 4: Cài đặt tất cả dependencies
```bash
pip install -r requirements.txt
```

Đợi cho đến khi kết thúc (có thể mất vài phút, dependencies khá nặng)

### Bước 5: Kiểm tra cài đặt
```bash
python -c "import manim; print('OK Manim')"
python -c "import numpy; print('OK NumPy')"
python -c "from gtts import gTTS; print('OK gTTS')"
```

### Khi muốn tắt môi trường ảo:
```bash
deactivate
```

---

## Cách 2: Conda (Tùy chọn)

Nếu bạn đã cài [Anaconda](https://www.anaconda.com/products/individual) hoặc [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

### Bước 1: Tạo môi trường Conda
```bash
conda create --name roo_code python=3.11
```

### Bước 2: Activate
```bash
conda activate roo_code
```

### Bước 3: Cài dependencies
```bash
pip install -r requirements.txt
```

### Khi muốn tắt:
```bash
conda deactivate
```

---

## Cài đặt Dependencies

### [OK] Cài tất cả cùng lúc (RECOMMENDED):
```bash
pip install -r requirements.txt
```

### [CONFIG] Hoặc cài từng package (nếu muốn chi tiết):
```bash
pip install manim==0.18.0
pip install manim-voiceover>=0.3.4
pip install gTTS>=2.2.4
pip install googletrans>=4.0.0
# ... v.v
```

### [PACKAGE] Xem những gì đã cài:
```bash
pip list
```

---

## Kiểm tra Cài đặt

### 1. Kiểm tra từng package:
```bash
# Manim
python -c "from manim import *; print('OK Manim')"

# Manim Voiceover
python -c "from manim_voiceover import VoiceoverScene; print('OK Manim Voiceover')"

# gTTS (quan trong!)
python -c "from gtts import gTTS; print('OK gTTS')"

# NumPy
python -c "import numpy; print('OK NumPy')"

# Pillow
python -c "from PIL import Image; print('OK Pillow')"
```

### 2. Chạy một Script test:
```bash
# Từ thư mục dự án (với venv activated):
python scripts/Scene2.py -pql
```

**Lệnh này sẽ:**
- `-p`: Preview (mở preview video)
- `-q`: Quiet (ít log)
- `-l`: Low quality (nhanh, chất lượng thấp, dùng để test)

---

## Troubleshooting

### [ERROR] "ModuleNotFoundError: No module named 'manim'"
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

### [ERROR] "ImportError: cannot import name 'GTTSService'"
**Nguyên nhân:** Thiếu gTTS

**Cách sửa:**
```bash
pip install gTTS>=2.2.4
```

### [ERROR] "Module 'googletrans' not found"
**Nguyên nhân:** Thiếu googletrans

**Cách sửa:**
```bash
pip install googletrans>=4.0.0
```

### [ERROR] venv chậm hoặc bị lỗi
**Cách sửa:** Xóa venv cũ và tạo lại
```bash
rmdir /s venv                    # Windows
rm -rf venv                      # macOS/Linux

python -m venv venv
venv\Scripts\activate            # Windows hoặc source venv/bin/activate
pip install -r requirements.txt
```

---

## Mẹo

### 1. Lưu danh sách dependencies (sau khi cài mới):
```bash
pip freeze > requirements.txt
```

### 2. Xóa packages không dùng:
```bash
pip uninstall package_name
```

### 3. Upgrade pip (tùy chọn):
```bash
python -m pip install --upgrade pip
```

### 4. Cài dependencies khi collaborate:
Mỗi người clone repo mới đều chạy:
```bash
pip install -r requirements.txt
```
**Tất cả sẽ có đúng cùng phiên bản dependencies!**