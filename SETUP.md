# SETUP - Huong dan Cai dat Moi truong

## Muc luc
1. [Tong quan](#tong-quan)
2. [Python & Git](#python--git)
3. [Cach 1: Virtual Environment (venv)](#cach-1-virtual-environment-venv-don-gian-nhat)
4. [Cach 2: Conda (Tuy chon)](#cach-2-conda-tuy-chon)
5. [Cai dat Dependencies](#cai-dat-dependencies)
6. [Kiem tra Cai dat](#kiem-tra-cai-dat)

---

## Tong quan

**Van de:**
- Cai truc tiep (`pip install` chung) se anh huong toan bo he thong Python
- Du an nay dung nhieu package lon (manim, pytorch, ...) co the xung dot voi du an khac

**Giai phap:**
- Tao **moi truong ao (Virtual Environment)** rieng cho du an nay
- Cai dependencies vao do → **an toan, doc lap, de quan ly**

---

## Python & Git

### [OK] Kiem tra da cai chua:
```bash
python --version      # Phai >= 3.9
git --version         # Bat ky phien ban gan day
```

### [ERROR] Neu chua cai:
- **Python:** https://www.python.org/downloads/ (chon "Add Python to PATH")
- **Git:** https://git-scm.com/download/win

---

## Cach 1: Virtual Environment (venv) - DON GIAN NHAT

### Buoc 1: Clone hoac mo du an
```bash
cd d:\Roo Code    # Hoac duong dan cua ban
```

### Buoc 2: Tao moi truong ao
```bash
# Windows:
python -m venv venv

# macOS / Linux:
python3 -m venv venv
```

**Ket qua:** Thu muc `venv/` se duoc tao (chua Python, pip, va dependencies)

### Buoc 3: Activate moi truong ao

#### Windows:
```bash
venv\Scripts\activate
```
[OK] Luc nay command prompt se co `(venv)` o dau:
```
(venv) D:\Roo Code>
```

#### macOS / Linux:
```bash
source venv/bin/activate
```

### Buoc 4: Cai dat tat ca dependencies
```bash
pip install -r requirements.txt
```

Doi cho den khi ket thuc (co the mat vai phut, dependencies kha nang)

### Buoc 5: Kiem tra cai dat
```bash
python -c "import manim; print('OK Manim')"
python -c "import numpy; print('OK NumPy')"
python -c "from gtts import gTTS; print('OK gTTS')"
```

### Khi muon tat moi truong ao:
```bash
deactivate
```

---

## Cach 2: Conda (Tuy chon)

Neu ban da cai [Anaconda](https://www.anaconda.com/products/individual) hoac [Miniconda](https://docs.conda.io/en/latest/miniconda.html):

### Buoc 1: Tao moi truong Conda
```bash
conda create --name roo_code python=3.11
```

### Buoc 2: Activate
```bash
conda activate roo_code
```

### Buoc 3: Cai dependencies
```bash
pip install -r requirements.txt
```

### Khi muon tat:
```bash
conda deactivate
```

---

## Cai dat Dependencies

### [OK] Cai tat ca cung luc (RECOMMENDED):
```bash
pip install -r requirements.txt
```

### [CONFIG] Hoac cai tung package (neu muon chi tiet):
```bash
pip install manim==0.18.0
pip install manim-voiceover>=0.3.4
pip install gTTS>=2.2.4
pip install googletrans>=4.0.0
# ... v.v
```

### [PACKAGE] Xem nhung gi da cai:
```bash
pip list
```

---

## Kiem tra Cai dat

### 1. Kiem tra tung package:
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

### 2. Chay mot Script test:
```bash
# Tu thu muc du an (voi venv activated):
python scripts/Scene2.py -pql
```

**Lenh nay se:**
- `-p`: Preview (mo preview video)
- `-q`: Quiet (it log)
- `-l`: Low quality (nhanh, chat luong thap, dung de test)

---

## Troubleshooting

### [ERROR] "ModuleNotFoundError: No module named 'manim'"
**Nguyen nhan:** Chua activate venv hoac dependencies chua cai

**Cach sua:**
```bash
# Kiem tra venv co activate khong (co (venv) o dau khong?)
# Neu khong, chay:
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux

# Roi cai lai:
pip install -r requirements.txt
```

### [ERROR] "ImportError: cannot import name 'GTTSService'"
**Nguyen nhan:** Thieu gTTS

**Cach sua:**
```bash
pip install gTTS>=2.2.4
```

### [ERROR] "Module 'googletrans' not found"
**Nguyen nhan:** Thieu googletrans

**Cach sua:**
```bash
pip install googletrans>=4.0.0
```

### [ERROR] venv cham hoac bi loi
**Cach sua:** Xoa venv cu va tao lai
```bash
rmdir /s venv                    # Windows
rm -rf venv                      # macOS/Linux

python -m venv venv
venv\Scripts\activate            # Windows hoac source venv/bin/activate
pip install -r requirements.txt
```

---

## Meo

### 1. Luu danh sach dependencies (sau khi cai moi):
```bash
pip freeze > requirements.txt
```

### 2. Xoa packages khong dung:
```bash
pip uninstall package_name
```

### 3. Upgrade pip (tuy chon):
```bash
python -m pip install --upgrade pip
```

### 4. Cai dependencies khi collaborate:
Moi nguoi clone repo moi deu chay:
```bash
pip install -r requirements.txt
```
**Tat ca se co dung cung phien ban dependencies!**

---

## Ket luan

| Phuong phap | Uu diem | Nhược diem |
|-----------|---------|-----------|
| **venv** | Don gian, built-in Python | Chi cho 1 du an |
| **Conda** | De quan ly nhieu phien ban Python | Can cai Anaconda |
| **Cai truc tiep** | Nhanh | RUI RO xung dot |

**KHUYEN CAO:** Dung **venv** cho du an nay - don gian va du!

---

Ban co cau hoi? Hoi toi!
