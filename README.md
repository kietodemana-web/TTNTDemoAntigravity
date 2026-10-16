# Hệ Thống Tư Vấn Chẩn Đoán Sự Cố Máy Tính Dựa Trên Triệu Chứng (Naive Bayes Classifier)

> **Đề tài:** Hệ thống tư vấn dựa trên triệu chứng, sử dụng bộ phân lớp Naive Bayes  
> **Sinh viên thực hiện:** Nguyễn Tuấn Kiệt & Huỳnh Tuấn Kiệt  
> **Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Tân  
> **Địa chỉ Web Demo chạy thật:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 1. Tổng Quan & Mục Tiêu Dự Án

Hệ thống được xây dựng nhằm giải quyết bài toán tư vấn sàng lọc ban đầu khi máy tính gặp sự cố phần cứng hoặc phần mềm. Dựa trên mô tả ngôn ngữ tự nhiên và danh mục triệu chứng người dùng cung cấp, mô hình toán học **Naive Bayes** (kết hợp kỹ thuật làm trơn **Laplace Smoothing $\alpha=1$**) tính toán xác suất hậu nghiệm $P(\text{Nhóm sự cố} \mid \text{Triệu chứng})$ để:
1. **Xếp hạng Top-3 nguyên nhân sự cố tiềm ẩn nhất** kèm tỷ lệ xác suất (%) định lượng rõ ràng.
2. **Liệt kê chi tiết các nguyên nhân con (Sub-causes)** và tỷ lệ tương ứng.
3. **Cung cấp checklist kiểm tra an toàn điện** và **hướng dẫn khắc phục từng bước** trước khi quyết định can thiệp sửa chữa.

---

## 2. Nguồn Dữ Liệu Thực Nghiệm (17,671 Mẫu Thật - Không Tự Sinh)

Tuân thủ nghiêm ngặt yêu cầu đề tài **"không tự sinh dữ liệu giả định, số mẫu ít nhất 2,000 mẫu"**, hệ thống thu thập và chuẩn hóa dữ liệu từ **2 nguồn dữ liệu mở quốc tế lớn nhất hiện nay**:

| Nguồn Dữ Liệu | Số lượng mẫu | Mô tả chi tiết |
| :--- | :---: | :--- |
| **Hugging Face IT Troubleshooting**<br>*(UmerSajid/IT-Troubleshooting-Dataset)* | **10,500 mẫu** | Dữ liệu hỗ trợ kỹ thuật CNTT thực tế gồm các triệu chứng (Symptoms), sự cố (Issues), nguyên nhân gốc (Causes) và các bước xử lý (Solution Steps) trên máy tính, hệ thống, mạng, phần cứng. |
| **Open Repair Alliance (ORDS)**<br>*(Open Repair Data Standard)* | **7,171 mẫu** | Dữ liệu sự cố sửa chữa thực tế từ mạng lưới sửa chữa cộng đồng toàn cầu (The Restart Project, Repair Café International, iFixit) đối với Laptop, Desktop PC, Màn hình, phụ kiện. |
| **TỔNG CỘNG DỮ LIỆU THỰC TẾ** | **17,671 mẫu** | **Vượt xa yêu cầu tối thiểu (gấp gần 9 lần mốc 2,000 mẫu)** |

### Phân Bổ Mẫu Theo 7 Nhóm Sự Cố:
1. **Phần mềm (Software / OS / Virus / Driver):** 7,624 mẫu
2. **Màn hình (Display / LCD / GPU / Cable):** 3,521 mẫu
3. **Nguồn (Power / Battery / Charger / PSU):** 2,070 mẫu
4. **Ổ cứng (Storage / HDD / SSD / Bad Sector):** 1,939 mẫu
5. **Mạng (Network / Wi-Fi / Ethernet / DNS):** 1,788 mẫu
6. **RAM (Memory / Beep Codes / Unseated):** 386 mẫu
7. **Quá nhiệt (Overheating / Fan Noise / Thermal):** 343 mẫu

---

## 3. Cơ Sở Toán Học & Kiến Trúc Mô Hình (Naive Bayes)

### Công thức Bayes:
$$P(C_k \mid X) = \frac{P(C_k) \cdot \prod_{i=1}^{n} P(x_i \mid C_k)}{P(X)}$$

- **$C_k$**: Một trong 7 nhóm sự cố máy tính.
- **$X = (x_1, x_2, \dots, x_n)$**: Vector đặc trưng triệu chứng trích xuất qua bộ trích xuất **TF-IDF N-gram (1,2) sublinear** (từ vựng 12,854 chiều).
- **Làm trơn Laplace ($\alpha=1$):** Triệt tiêu xác suất 0 khi gặp từ khóa triệu chứng mới chưa xuất hiện trong tập huấn luyện của lớp đó:
  $$P(x_i \mid C_k) = \frac{N_{ki} + \alpha}{N_k + \alpha \cdot |V|}$$

### Quy trình 5 bước theo Slide 6:
$$\text{Nhập triệu chứng} \longrightarrow \text{Mã hóa Vector (TF-IDF)} \longrightarrow \text{Phân lớp Naive Bayes} \longrightarrow \text{Top-3 nguyên nhân kèm \%} \longrightarrow \text{Gợi ý khắc phục & An toàn}$$

---

## 4. Kết Quả Thực Nghiệm Thật (Thay thế số liệu minh họa Slides 8, 9, 10)

Mô hình được phân chia phân tầng (Stratified Split) theo tỷ lệ chuẩn **80% Huấn luyện (14,136 mẫu)** và **20% Kiểm thử độc lập (3,535 mẫu)**.

### Bảng So Sánh Các Mô Hình Phân Lớp (Slide 10 Thực Nghiệm):
| Mô hình | Accuracy (Top-1) | Top-3 Accuracy | Thời gian dự đoán (Latency) |
| :--- | :---: | :---: | :---: |
| **Naive Bayes (MultinomialNB - $\alpha=1.0$)** | **93.66%** | **98.84%** | **0.000 ms (Siêu tốc)** |
| **Naive Bayes (BernoulliNB)** | 92.36% | 97.91% | 0.001 ms |
| **Decision Tree** | 97.51% | 98.90% | 0.001 ms |
| **KNN ($k=5$, Cosine)** | 94.37% | 98.84% | 0.497 ms |
| **Logistic Regression** | 96.83% | 99.77% | 0.002 ms |

> 🌟 **Nhận xét khoa học:**
> - Naive Bayes đạt độ chính xác thực nghiệm ấn tượng **93.66%**, cao hơn nhiều so với con số ước lượng 87% trên slide báo cáo.
> - **Top-3 Accuracy đạt tới 98.84%**, chứng minh mô hình hầu như luôn chứa nguyên nhân gốc chính xác trong 3 đề xuất đầu tiên.
> - **Độ trễ suy luận $\approx 0$ ms** (nhờ tính toán dựa trên vector log-likelihood), vượt trội hoàn toàn về tốc độ so với KNN hay Deep Learning.

### Bảng Kết Quả Chi Tiết 7 Nhóm Sự Cố Của Naive Bayes (Slide 9 Thực Nghiệm):
| Nhóm Sự Cố | Precision (%) | Recall (%) | F1-Score (%) | Số Mẫu Test Kiểm Thử |
| :--- | :---: | :---: | :---: | :---: |
| **Nguồn** | 89.41% | 91.79% | **90.58%** | 414 mẫu |
| **Màn hình** | 92.14% | 94.18% | **93.15%** | 704 mẫu |
| **Quá nhiệt** | 88.33% | 76.81% | **82.17%** | 69 mẫu |
| **Ổ cứng** | 98.44% | 97.42% | **97.93%** | 388 mẫu |
| **RAM** | 96.97% | 83.12% | **89.51%** | 77 mẫu |
| **Mạng** | 99.16% | 98.60% | **98.88%** | 358 mẫu |
| **Phần mềm** | 92.59% | 94.16% | **93.37%** | 1,525 mẫu |
| **Trung bình toàn bộ (Weighted Avg)** | **93.71%** | **93.66%** | **93.67%** | **3,535 mẫu** |

---

## 5. Hướng Dẫn Cài Đặt & Chạy Demo

### Yêu cầu môi trường:
- Hệ điều hành: Windows 10/11
- Python 3.11+
- Các thư viện: `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `numpy`, `joblib`, `requests`

### Khởi chạy hệ thống:
```powershell
# Di chuyển vào thư mục dự án
cd "c:\AI Demo App"

# Khởi động Web Server
.venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8000
```

Mở trình duyệt web và truy cập: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 6. Các Tính Năng Nổi Bật Của Giao Diện Demo

1. **Bảng Điều Khiển Chẩn Đoán (Diagnostic Console):**
   - Hỗ trợ nhập triệu chứng tiếng Việt tự do hoặc tick chọn các triệu chứng thường gặp.
   - Nút kịch bản mẫu thử nhanh (Quick Scenarios) theo đúng slide 11 (Tiếng bíp, Màn hình xanh, Quá nhiệt, Ổ cứng 100% disk...).
   - Hiển thị Top-3 nguyên nhân trực quan kèm thanh tiến trình động, phân tách các nguyên nhân con cụ thể.
   - Hướng dẫn an toàn điện và các bước kiểm tra chi tiết.
2. **Báo Cáo Thực Nghiệm Live (Benchmark Dashboard):**
   - Biểu đồ cột động Chart.js cho Precision / Recall / F1 trên 7 nhóm sự cố.
   - Bảng so sánh 5 mô hình máy học (Naive Bayes, Decision Tree, KNN, Logistic Regression).
   - Biểu đồ đường cong học tập (Learning Curve) theo quy mô tập huấn luyện.
   - **Ma trận nhầm lẫn 7x7 (Confusion Matrix)** với cường độ màu heatmap trực quan.
3. **Khám Phá Dữ Liệu Thực (Dataset Explorer - 17,671 hồ sơ):**
   - Phân trang, tìm kiếm từ khóa, lọc theo nguồn (Open Repair Alliance vs Hugging Face) và theo từng nhóm linh kiện.
4. **Cơ Sở Lý Thuyết & Kiến Trúc (Theory & Architecture):**
   - Giải thích công thức toán, Laplace smoothing, và sơ đồ quy trình 5 bước.
