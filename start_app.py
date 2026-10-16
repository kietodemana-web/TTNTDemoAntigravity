import os
import sys
import time
import socket
import webbrowser
import subprocess

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def main():
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = os.path.join(base_dir, ".venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        python_exe = sys.executable

    print("=" * 65)
    print("   HỆ THỐNG CHẨN ĐOÁN SỰ CỐ MÁY TÍNH - NAIVE BAYES CLASSIFIER   ")
    print("=" * 65)
    print(f"[*] Thư mục dự án: {base_dir}")
    print(f"[*] Trình thông dịch: {python_exe}")
    print(f"[*] Địa chỉ máy chủ: {url}")

    if is_port_in_use(port, host):
        print("\n[+] Máy chủ chẩn đoán đang hoạt động sẵn sàng!")
    else:
        print("\n[*] Đang khởi động máy chủ FastAPI/Uvicorn...")
        # Start server as a background subprocess
        server_cmd = [
            python_exe,
            "-m",
            "uvicorn",
            "server:app",
            "--host",
            host,
            "--port",
            str(port)
        ]
        proc = subprocess.Popen(server_cmd, cwd=base_dir)
        
        # Wait up to 10 seconds for the server to be ready
        print("[*] Đang nạp mô hình Naive Bayes và 17,671 mẫu dữ liệu...")
        for _ in range(20):
            if is_port_in_use(port, host):
                print("[+] Khởi động máy chủ thành công!")
                break
            time.sleep(0.5)

    print("\n[+] Đang tự động mở giao diện ứng dụng...")
    time.sleep(0.5)
    
    # Try opening as a standalone App Window (Edge / Chrome) for desktop app look and feel
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    opened = False
    for path in edge_paths + chrome_paths:
        if os.path.exists(path):
            try:
                subprocess.Popen([path, f"--app={url}"])
                opened = True
                break
            except Exception:
                pass
                
    if not opened:
        webbrowser.open(url)
    
    print("\n" + "=" * 65)
    print(f"  Giao diện đã mở tại: {url}")
    print("  Nhấn Enter hoặc đóng cửa sổ này khi bạn hoàn tất sử dụng.")
    print("=" * 65)
    try:
        input("\n[Nhấn Enter để thoát trình điều khiển launcher]...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
