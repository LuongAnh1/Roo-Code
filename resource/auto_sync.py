import os
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_git(args):
    return subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)


def sync():
    # Bước 1: CHỈ kiểm tra sự thay đổi bên trong thư mục 'resource'
    status = run_git(["status", "resource/", "--porcelain"])
    if not status.stdout.strip():
        print(f"[{datetime.now()}] Không có tài nguyên nào mới trong thư mục 'resource'.")
        return

    print("Đang đóng gói tài nguyên mới trong mục 'resource'...")

    # Bước 2: CHỈ gom (add) các file nằm trong thư mục 'resource'
    run_git(["add", "resource/"])

    msg = f"Auto-sync Resource: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_git(["commit", "-m", msg])

    result = run_git(["push", "origin", "HEAD"])

    if result.returncode == 0:
        print(f"[{datetime.now()}] Đã đẩy kho ảnh lên GitHub thành công!")
    else:
        print(f"Lỗi khi Push: {result.stderr}")


if __name__ == "__main__":
    sync()