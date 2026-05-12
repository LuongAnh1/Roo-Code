import os
import subprocess
from datetime import datetime

# Lấy đường dẫn gốc của dự án Roo-Code
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_git(args):
    return subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)


def sync():
    # Kiểm tra xem có file ảnh/video mới không
    status = run_git(["status", "--porcelain"])
    if not status.stdout.strip():
        print(f"[{datetime.now()}] Không có tài nguyên mới.")
        return

    print("Đang phát hiện tài nguyên mới trong B.F.E Alliance Resource...")
    run_git(["add", "."])

    msg = f"Auto-sync Resource: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_git(["commit", "-m", msg])

    result = run_git(["push", "origin", "main"])
    if result.returncode == 0:
        print(f"[{datetime.now()}] Đã đẩy ảnh/video lên GitHub thành công!")
    else:
        print(f"Lỗi: {result.stderr}")


if __name__ == "__main__":
    sync()