@echo off
chcp 65001 > nul
title Hệ Thống Tư Vấn Chẩn Đoán Sự Cố Máy Tính - Naive Bayes

echo ===================================================================
echo     HỆ THỐNG TƯ VẤN CHẨN ĐOÁN SỰ CỐ MÁY TÍNH (NAIVE BAYES)
echo     Sinh viên: Nguyễn Tuấn Kiệt - Huỳnh Tuấn Kiệt
echo     GVHD: ThS. Nguyễn Ngọc Tân
echo ===================================================================
echo.
echo [*] Đang kiểm tra môi trường và khởi động ứng dụng...

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" start_app.py
) else (
    echo [!] Không tìm thấy .venv. Đang sử dụng Python mặc định...
    python start_app.py
)

pause
