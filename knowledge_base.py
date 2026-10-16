# Diagnostic knowledge base for computer troubleshooting
# Providing rich sub-causes and detailed safety/resolution steps for the 7 categories

DIAGNOSTIC_KNOWLEDGE = {
    "Nguồn": {
        "icon": "⚡",
        "color": "#f59e0b",
        "description": "Sự cố liên quan đến hệ thống cấp điện, sạc, pin, bộ nguồn PSU hoặc mạch quản lý nguồn (PMIC)",
        "sub_causes": [
            {
                "name": "Bộ sạc / Adapter nguồn hoặc dây cắm bị đứt ngầm / hỏng",
                "prob_factor": 0.40,
                "symptoms": ["Cắm sạc không sáng đèn", "Máy chỉ chạy khi cắm sạc ở góc nhất định", "Adapter quá nóng hoặc kêu rè rè"],
                "action": "Dùng đồng hồ VOM đo điện áp đầu ra adapter (thường 19V-20V đối với laptop). Thử bộ sạc chính hãng khác có cùng công suất (Watt)."
            },
            {
                "name": "Pin laptop bị chai nặng, phồng pin hoặc mạch bảo vệ pin ngắt",
                "prob_factor": 0.35,
                "symptoms": ["Máy sập ngay khi rút sạc", "Pin báo 'Plugged in, not charging'", "Touchpad bị đẩy nhô lên do phồng pin"],
                "action": "Ngắt sạc ngay lập tức. Nếu pin phồng, tháo pin cẩn thận để tránh nguy cơ cháy nổ. Chạy chẩn đoán Battery Report trên Windows (`powercfg /batteryreport`)."
            },
            {
                "name": "Nguồn máy bàn (PSU) bị sụt áp, chết tụ hoặc IC nguồn bo mạch chập",
                "prob_factor": 0.25,
                "symptoms": ["Bấm nút nguồn quạt nhích 1 cái rồi tắt", "Máy tự sập nguồn đột ngột khi tải nặng", "Có mùi khét nhẹ"],
                "action": "Kích nguồn PSU bằng phương pháp chập chân xanh lá (PS_ON) với chân đen (GND) để test quạt nguồn. Kiểm tra tụ điện trên mainboard có bị phù không."
            }
        ],
        "safety_steps": [
            "⚠️ LUÔN ngắt nguồn điện 220V và rút pin trước khi chạm vào linh kiện bên trong.",
            "Xả điện tích dư bằng cách giữ nút nguồn máy tính từ 15-20 giây sau khi ngắt điện.",
            "Không tiếp tục cắm sạc khi phát hiện pin bị phồng hoặc adapter phát tiếng kêu lạ.",
            "Sử dụng ổ cắm có tiếp địa hoặc ổ cắm chống sét lan truyền để bảo vệ thiết bị."
        ],
        "resolution_steps": [
            "Bước 1: Rút toàn bộ thiết bị ngoại vi (USB, chuột, máy in, ổ cứng rời) và thử bật lại.",
            "Bước 2: Kiểm tra ổ cắm điện tường và dây cáp nguồn AC.",
            "Bước 3: Thực hiện Hard Reset (tháo sạc, tháo pin nếu tháo rời được, nhấn giữ nút nguồn 30 giây, cắm sạc trực tiếp và bật thử).",
            "Bước 4: Kiểm tra đèn LED chỉ thị nguồn trên thân máy hoặc cổng Type-C/DC-in.",
            "Bước 5: Nếu máy hoàn toàn im lìm, mang tới trung tâm kỹ thuật kiểm tra IC nguồn / Mosfet trên bo mạch."
        ]
    },
    "Màn hình": {
        "icon": "🖥️",
        "color": "#3b82f6",
        "description": "Sự cố liên quan đến tấm nền LCD/OLED, cáp màn hình (eDP/LVDS), đèn nền (backlight) hoặc chip đồ họa (GPU)",
        "sub_causes": [
            {
                "name": "Cáp màn hình (eDP/LVDS) bị lỏng, gập gãy tại bản lề hoặc đứt ngầm",
                "prob_factor": 0.38,
                "symptoms": ["Màn hình chớp giật khi gập mở góc máy", "Xuất hiện sọc ngang/dọc thay đổi khi ấn nhẹ vào viền", "Màn hình tối đen nhưng rọi đèn pin vẫn thấy mờ mờ"],
                "action": "Tháo nắp viền bezel, kiểm tra chân cắm cáp màn hình phía sau panel và trên mainboard. Gia cố lại băng keo cố định chân cắm."
            },
            {
                "name": "Tấm nền LCD bị hỏng bóng LED đèn nền (Backlight) hoặc nứt vỡ tinh thể lỏng",
                "prob_factor": 0.34,
                "symptoms": ["Màn hình có vệt mực loang", "Một góc màn hình bị tối hẳn", "Chớp tắt liên tục"],
                "action": "Xuất hình ảnh ra màn hình ngoài qua cổng HDMI / Type-C. Nếu màn ngoài hiển thị bình thường 100%, lỗi chắc chắn ở tấm nền LCD cần thay thế."
            },
            {
                "name": "Chip đồ họa (VGA / GPU) bị quá nhiệt hở chân chì, lỗi driver hoặc hỏng VRAM",
                "prob_factor": 0.28,
                "symptoms": ["Xuất hiện rác hình (artifacts), ô cờ caro", "Độ phân giải bị khóa ở 800x600", "Đang xem video thì màn hình nháy đen rồi báo Display driver stopped responding"],
                "action": "Dùng DDU (Display Driver Uninstaller) gỡ sạch driver ở Safe Mode, sau đó cài lại bản driver đồ họa WHQL mới nhất từ website hãng."
            }
        ],
        "safety_steps": [
            "⚠️ Tuyệt đối không ấn mạnh tay vào bề mặt tấm nền LCD khi kiểm tra.",
            "Trước khi tháo/cắm cáp eDP màn hình, BẮT BUỘC phải ngắt pin laptop để tránh chập cầu chì đèn nền trên mainboard.",
            "Tránh gập mở màn hình laptop bằng một tay ở góc viền, luôn mở ở vị trí chính giữa."
        ],
        "resolution_steps": [
            "Bước 1: Kết nối máy tính với màn hình rời hoặc TV qua cổng HDMI / DisplayPort để phân lập lỗi tấm nền hay do GPU.",
            "Bước 2: Nhấn tổ hợp phím [Windows + Ctrl + Shift + B] để reset lại driver đồ họa Windows.",
            "Bước 3: Rọi đèn pin vào màn hình. Nếu thấy hình ảnh mờ mờ, mạch cao áp hoặc đèn nền LED màn hình bị lỗi.",
            "Bước 4: Khởi động vào BIOS (nhấn F2/Del khi bật máy). Nếu trong BIOS màn hình vẫn bị sọc/đen, đây là lỗi phần cứng 100%.",
            "Bước 5: Tháo kiểm tra cáp tín hiệu màn hình hoặc liên hệ thay tấm nền LCD mới."
        ]
    },
    "Quá nhiệt": {
        "icon": "🔥",
        "color": "#ef4444",
        "description": "Hệ thống làm mát không hiệu quả, quạt tản nhiệt kẹt bụi, khô keo tản nhiệt dẫn tới thermal throttling hoặc sập bảo vệ",
        "sub_causes": [
            {
                "name": "Quạt làm mát (Cooling Fan) bị kẹt bụi bẩn, khô dầu hoặc hỏng motor quay",
                "prob_factor": 0.42,
                "symptoms": ["Quạt phát tiếng rít ken két hoặc tiếng gầm rú", "Máy báo lỗi 'Fan Error' lúc khởi động", "Không thấy hơi nóng thổi ra ở khe tản nhiệt"],
                "action": "Dùng bình khí nén vệ sinh quạt và các lá đồng tản nhiệt. Tra dầu bôi trơn chuyên dụng cho trục quạt hoặc thay quạt mới."
            },
            {
                "name": "Keo tản nhiệt (Thermal Paste) CPU/GPU bị khô cứng, mất khả năng dẫn nhiệt",
                "prob_factor": 0.38,
                "symptoms": ["Nhiệt độ CPU vọt lên >90°C chỉ sau 2 phút mở máy", "Bề mặt vỏ máy rất nóng", "Máy bị giảm xung nhịp (thermal throttling) cực giật lag"],
                "action": "Tháo cụm ống đồng tản nhiệt, dùng cồn Isopropyl (IPA) 90%+ lau sạch keo cũ, tra keo tản nhiệt chất lượng cao (như Arctic MX-4, Noctua NT-H1)."
            },
            {
                "name": "Lỗ hút gió / thoát nhiệt bị che chắn hoặc đệm tản nhiệt (Thermal Pad) bị rách/lệch",
                "prob_factor": 0.20,
                "symptoms": ["Nhiệt độ VRM và VRAM tăng cao bất thường", "Máy sập đột ngột khi render đồ họa hoặc chơi game"],
                "action": "Không đặt laptop lên chăn, nệm hay đùi khi làm việc nặng. Sử dụng đế tản nhiệt hoặc kê cao chân đế máy 2-3 cm để lưu thông gió."
            }
        ],
        "safety_steps": [
            "⚠️ Để máy tính nguội hoàn toàn trong ít nhất 15 phút trước khi tháo rời hệ thống làm mát.",
            "Khi xiết ốc tản nhiệt CPU/GPU, phải xiết chéo theo thứ tự số đánh dấu (1-2-3-4) với lực vừa phải để tránh nứt vỡ đế die silicon.",
            "Tuyệt đối không dùng kim loại nhọn cạo keo tản nhiệt trên bề mặt CPU/GPU."
        ],
        "resolution_steps": [
            "Bước 1: Cài đặt phần mềm HWMonitor hoặc Core Temp để theo dõi chính xác nhiệt độ CPU/GPU theo thời gian thực.",
            "Bước 2: Kiểm tra khe tản nhiệt bằng mắt thường xem có mảng bụi bẩn bít kín đường thoát gió không.",
            "Bước 3: Tạm dừng các tác vụ nặng ngầm bằng Task Manager (kiểm tra tiến trình nào đang chiếm >80% CPU).",
            "Bước 4: Thực hiện vệ sinh máy và tra keo tản nhiệt mới định kỳ mỗi 6 - 12 tháng.",
            "Bước 5: Kiểm tra và cập nhật BIOS để tối ưu hóa profile điều khiển tốc độ quạt (Fan Curve)."
        ]
    },
    "Ổ cứng": {
        "icon": "💾",
        "color": "#8b5cf6",
        "description": "Lỗi phần cứng ổ cứng HDD/SSD, phân vùng dữ liệu bị lỗi, bad sector, ổ đĩa đầy hoặc lỗi giao tiếp SATA/NVMe",
        "sub_causes": [
            {
                "name": "Ổ HDD bị Bad Sector hoặc đầu đọc va quẹt bề mặt đĩa (Click of Death)",
                "prob_factor": 0.40,
                "symptoms": ["Ổ cứng phát tiếng lách cách rè rè liên tục", "Task Manager báo 100% Disk dù không chạy ứng dụng gì", "Máy hay bị đơ chuột 5-10 giây rồi chạy tiếp"],
                "action": "Dùng CrystalDiskInfo kiểm tra chỉ số SMART (05 Reallocated Sectors, C5 Current Pending Sector). Sao lưu dữ liệu khẩn cấp ngay lập tức."
            },
            {
                "name": "Ổ SSD bị lỗi Controller, suy thoái chip nhớ NAND hoặc quá nhiệt",
                "prob_factor": 0.32,
                "symptoms": ["Windows bị treo màn hình xanh WHEA_UNCORRECTABLE_ERROR", "Khởi động thẳng vào BIOS và không thấy tên ổ đĩa", "Tốc độ đọc ghi tụt thảm hại"],
                "action": "Kiểm tra khe cắm M.2 NVMe, tháo ra vệ sinh chân tiếp xúc bằng cồn rồi cắm chặt lại. Cập nhật Firmware ổ cứng từ hãng sản xuất."
            },
            {
                "name": "Phân vùng hệ thống NTFS bị hỏng cấu trúc (Corrupted File System) hoặc ổ C bị đầy 100%",
                "prob_factor": 0.28,
                "symptoms": ["Máy khởi động tự chạy 'Scanning and repairing drive (C:)'", "Không thể lưu tệp tin, báo lỗi I/O Device Error"],
                "action": "Mở Command Prompt với quyền Admin, chạy lệnh `chkdsk C: /f /r` và khởi động lại để Windows tự sửa chữa các sector hỏng logic."
            }
        ],
        "safety_steps": [
            "⚠️ SAO LƯU DỮ LIỆU QUAN TRỌNG NGAY LẬP TỨC khi phát hiện ổ cứng có dấu hiệu phát ra tiếng kêu lạ hoặc báo tình trạng Caution/Bad.",
            "Không cố gắng chạy các phần mềm phục hồi dữ liệu nặng nếu ổ đĩa đang phát ra tiếng kêu va đập cơ khí.",
            "Không tháo vỏ bảo vệ ổ cứng HDD trong môi trường phòng thông thường (cần phòng sạch chuẩn Class 100)."
        ],
        "resolution_steps": [
            "Bước 1: Tải công cụ CrystalDiskInfo để kiểm tra sức khỏe SMART của ổ cứng (Good / Caution / Bad).",
            "Bước 2: Mở Command Prompt (Admin), chạy lệnh `sfc /scannow` và `chkdsk C: /f` để quét sửa lỗi hệ thống tệp.",
            "Bước 3: Mở Disk Management (diskmgmt.msc) kiểm tra ổ đĩa có hiển thị đúng dung lượng và định dạng không.",
            "Bước 4: Nâng cấp thay thế ổ HDD cũ bằng ổ SSD SATA/NVMe để tăng tốc độ máy tính lên gấp 5-10 lần.",
            "Bước 5: Nếu ổ cứng không nhận trong BIOS, thử đổi cáp SATA/cổng cắm hoặc gắn vào hộp đọc box USB ngoài để kiểm tra."
        ]
    },
    "RAM": {
        "icon": "🧠",
        "color": "#ec4899",
        "description": "Lỗi bộ nhớ truy xuất ngẫu nhiên (RAM), chân tiếp xúc oxy hóa, khe cắm RAM lỏng, xung đột bus hoặc module RAM bị lỗi cell nhớ",
        "sub_causes": [
            {
                "name": "Chân tiếp xúc RAM bị oxy hóa, bám bụi bẩn hoặc thanh RAM bị lỏng khỏi khe cắm",
                "prob_factor": 0.45,
                "symptoms": ["Bật máy sáng đèn nguồn, quạt quay nhưng không lên màn hình kèm tiếng bíp liên tục (1 bíp dài 2 bíp ngắn)", "Máy nhận thiếu dung lượng RAM (VD cắm 16GB chỉ nhận 8GB)"],
                "action": "Tháo thanh RAM ra, dùng tẩy cao su (gôm học sinh) hoặc cồn IPA lau sạch bóng chân đồng tiếp xúc. Thổi sạch bụi trong khe cắm và ấn chặt chốt khóa 2 đầu."
            },
            {
                "name": "Module chip nhớ (DRAM IC) bị lỗi hỏng cell nhớ (Bad Memory Cell)",
                "prob_factor": 0.35,
                "symptoms": ["Màn hình xanh ngẫu nhiên với mã lỗi MEMORY_MANAGEMENT, PAGE_FAULT_IN_NONPAGED_AREA", "Ứng dụng và trình duyệt Google Chrome tự động crash văng ra"],
                "action": "Chạy công cụ chẩn đoán Windows Memory Diagnostic (`mdsched.exe`) hoặc tạo USB Boot MemTest86 để quét kiểm tra toàn diện từng thanh RAM."
            },
            {
                "name": "Xung đột cấu hình XMP/DOCP, lệch Bus RAM hoặc không tương thích giữa các thanh RAM",
                "prob_factor": 0.20,
                "symptoms": ["Máy không boot được khi cắm 2 thanh khác hãng/khác bus", "Chạy một lúc tự khởi động lại"],
                "action": "Vào BIOS tắt tính năng XMP/DOCP để RAM chạy ở xung nhịp mặc định (JEDEC 2133/2400/2666/3200MHz) hoặc nâng cấp BIOS lên phiên bản mới nhất."
            }
        ],
        "safety_steps": [
            "⚠️ BẮT BUỘC tắt nguồn điện, rút sạc và pin trước khi tháo lắp thanh RAM.",
            "Chạm tay vào bề mặt kim loại không sơn (như khung vỏ case PC) để xả tĩnh điện trước khi chạm vào mạch RAM.",
            "Khi lắp RAM, chú ý đúng chiều rãnh khuyết (notch) ở giữa thanh RAM với khe cắm. Không cố ấn mạnh khi lệch chiều."
        ],
        "resolution_steps": [
            "Bước 1: Rút điện, tháo pin, tháo nắp đáy và lấy các thanh RAM ra khỏi máy.",
            "Bước 2: Dùng cục tẩy học sinh chà nhẹ nhàng làm sạch toàn bộ hàng chân mạ vàng của RAM ở cả 2 mặt.",
            "Bước 3: Nếu máy có 2 thanh RAM, cắm thử TỪNG THANH MỘT vào từng khe cắm để xác định chính xác thanh RAM hay khe cắm nào bị lỗi.",
            "Bước 4: Ấn thanh RAM xuống đều 2 bên cho đến khi 2 ngàm khóa kêu 'tách' và ôm khít thanh RAM.",
            "Bước 5: Khởi động máy, gõ `mdsched.exe` vào hộp thoại Run để Windows quét kiểm tra lỗi bộ nhớ khi khởi động lại."
        ]
    },
    "Mạng": {
        "icon": "🌐",
        "color": "#06b6d4",
        "description": "Lỗi kết nối Wi-Fi, card mạng Ethernet, xung đột địa chỉ IP, lỗi máy chủ DNS hoặc driver điều khiển mạng",
        "sub_causes": [
            {
                "name": "Driver card mạng Wi-Fi / LAN bị lỗi thời, xung đột sau bản cập nhật Windows",
                "prob_factor": 0.40,
                "symptoms": ["Mất biểu tượng Wi-Fi trên thanh taskbar", "Device Manager hiện dấu chấm than vàng tại Network Adapters", "Wi-Fi chập chờn tự ngắt mỗi 10-15 phút"],
                "action": "Mở Device Manager, nhấp chuột phải vào card mạng chọn 'Uninstall device', sau đó khởi động lại máy để Windows tự nhận lại driver gốc hoặc cài driver từ trang chủ hãng."
            },
            {
                "name": "Cấu hình mạng IP / DNS bị lỗi, kẹt bộ nhớ đệm Winsock hoặc máy chủ DHCP router cấp sai",
                "prob_factor": 0.35,
                "symptoms": ["Báo 'Connected, no internet', dấu chấm than vàng", "Vào được mạng Zalo/Skype nhưng không vào được trình duyệt web", "Lỗi DNS_PROBE_FINISHED_NO_INTERNET"],
                "action": "Mở Command Prompt (Admin) chạy chuỗi lệnh reset mạng: `ipconfig /flushdns` -> `ipconfig /release` -> `ipconfig /renew` -> `netsh winsock reset`."
            },
            {
                "name": "Card Wi-Fi vật lý (M.2/PCIe) bị lỏng cáp ăng-ten ngầm hoặc hỏng phần cứng",
                "prob_factor": 0.25,
                "symptoms": ["Bắt sóng Wi-Fi cực yếu (chỉ 1 vạch) dù ngồi cạnh router", "Bật Bluetooth cũng bị ảnh hưởng do chung card", "Không tìm thấy bất kỳ mạng Wi-Fi nào"],
                "action": "Tháo nắp máy kiểm tra 2 đầu dây cáp ăng-ten đen/trắng (Main/Aux) đã gắn chặt vào card Wi-Fi chưa. Thử thay thế bằng USB Wi-Fi cắm ngoài giá rẻ."
            }
        ],
        "safety_steps": [
            "⚠️ Khi tháo đầu bấm cáp ăng-ten card Wi-Fi, dùng nhíp nhựa gắp nhẹ nhàng thẳng đứng, tránh làm bẹp đầu giắc bấm siêu nhỏ u.FL.",
            "Không tải driver mạng từ các trang web lạ không rõ nguồn gốc để phòng tránh mã độc.",
            "Cẩn thận khi thao tác tắt tường lửa (Firewall) trong quá trình test kết nối."
        ],
        "resolution_steps": [
            "Bước 1: Khởi động lại Router / Modem Wi-Fi (rút phích cắm điện, chờ 30 giây rồi cắm lại).",
            "Bước 2: Chạy tính năng Windows Network Troubleshooter (Click phải vào biểu tượng mạng -> Chọn Diagnose / Troubleshoot).",
            "Bước 3: Đổi DNS sang Google DNS (8.8.8.8 / 8.8.4.4) hoặc Cloudflare DNS (1.1.1.1 / 1.0.0.1).",
            "Bước 4: Mở CMD (Admin) chạy `netsh int ip reset` và `netsh winsock reset`, sau đó khởi động lại máy tính.",
            "Bước 5: Vào Settings -> Network & Internet -> Advanced network settings -> Chọn 'Network reset' để khôi phục toàn bộ cài đặt mạng về mặc định."
        ]
    },
    "Phần mềm": {
        "icon": "💻",
        "color": "#10b981",
        "description": "Lỗi hệ điều hành Windows, mã độc/virus, xung đột driver hệ thống, lỗi tập tin boot hoặc ứng dụng bị crash",
        "sub_causes": [
            {
                "name": "Hệ điều hành Windows bị lỗi file hệ thống, xung đột cập nhật (Windows Update) hoặc boot loop",
                "prob_factor": 0.42,
                "symptoms": ["Máy khởi động bị treo ở logo 'Automatic Repair'", "Bị màn hình xanh BSOD sau khi cập nhật Windows", "Không vào được màn hình Desktop"],
                "action": "Khởi động vào chế độ Safe Mode hoặc Windows Recovery Environment (WinRE). Chọn 'Uninstall latest quality update' hoặc chạy lệnh `DISM /Online /Cleanup-Image /RestoreHealth`."
            },
            {
                "name": "Máy tính bị nhiễm mã độc, Virus đào coin, Spyware hoặc phần mềm quảng cáo độc hại",
                "prob_factor": 0.32,
                "symptoms": ["CPU và GPU luôn chạy ở mức 90-100% dù máy đang để không", "Trình duyệt tự nhảy sang các trang web quảng cáo lạ", "Các tệp tin bị đổi đuôi lạ và đòi tiền chuộc"],
                "action": "Tải công cụ quét mã độc chuyên sâu như Malwarebytes Free hoặc Windows Defender Offline Scan để quét và diệt triệt để ở môi trường độc lập."
            },
            {
                "name": "Xung đột ứng dụng chạy ngầm, thiếu thư viện Runtime (Visual C++, .NET) hoặc lỗi Registry",
                "prob_factor": 0.26,
                "symptoms": ["Mở ứng dụng báo lỗi 0xc000007b hoặc thiếu file .dll", "Máy bị đóng băng (Freeze) khi mở nhiều tác vụ", "Thông báo 'Application has stopped working'"],
                "action": "Cài đặt gói All-in-One Visual C++ Redistributable Runtimes. Tắt các ứng dụng khởi động cùng Windows không cần thiết trong thẻ Startup của Task Manager."
            }
        ],
        "safety_steps": [
            "⚠️ Luôn bật tính năng System Restore (Điểm khôi phục hệ thống) trước khi cài đặt phần mềm lạ hoặc can thiệp Registry.",
            "Không tắt ngang máy tính (bằng cách giữ nút nguồn hoặc rút phích) khi Windows đang trong quá trình cập nhật 'Working on updates'.",
            "Cảnh giác với các đường link lạ hoặc tệp tin đính kèm có đuôi .exe, .scr, .vbs trong email."
        ],
        "resolution_steps": [
            "Bước 1: Mở Command Prompt bằng quyền Administrator, chạy lệnh `sfc /scannow` để quét và tự động sửa các tệp tin Windows bị hỏng.",
            "Bước 2: Chạy lệnh `DISM /Online /Cleanup-Image /RestoreHealth` để tải và phục hồi các thành phần hệ thống gốc từ máy chủ Microsoft.",
            "Bước 3: Mở Task Manager (Ctrl + Shift + Esc) kiểm tra xem tiến trình nào đang ngốn tài nguyên bất thường và tắt nó đi.",
            "Bước 4: Sử dụng công cụ System Restore để quay lại thời điểm máy tính còn hoạt động ổn định trước đó.",
            "Bước 5: Nếu hệ thống bị hư hại nặng, sử dụng tính năng 'Reset this PC' (chọn Keep my files để giữ lại tài liệu cá nhân) để cài đặt lại Windows sạch sẽ."
        ]
    }
}
