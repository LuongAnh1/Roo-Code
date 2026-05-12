import os
import subprocess
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_git(args):
    return subprocess.run(["git"] + args, cwd=PROJECT_ROOT, capture_output=True, text=True)


def sync():
    status = run_git(["status", "--porcelain"])
    if not status.stdout.strip():
        print(f"[{datetime.now()}] Không có tài nguyên ảnh/video nào mới.")
        return

    print("Đang phát hiện tài nguyên mới trong kho ...")

    run_git(["add", "."])

    msg = f"Auto-sync Resource: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_git(["commit", "-m", msg])

    # Lệnh HEAD giúp tự động nhận diện và đẩy lên nhánh hiện tại (nhánh Thành)
    result = run_git(["push", "origin", "HEAD"])

    if result.returncode == 0:
        print(f"[{datetime.now()}] Đã đẩy tài nguyên lên GitHub thành công!")
    else:
        print(f"Lỗi khi Push: {result.stderr}")


if __name__ == "__main__":
    sync()