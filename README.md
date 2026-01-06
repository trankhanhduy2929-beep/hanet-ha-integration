Hanet AI Camera Bridge Pro cho Home Assistant

Integration này giúp kết nối dữ liệu từ Hanet AI Camera vào Home Assistant thông qua Add-on trung gian "Hanet Bridge Pro".

✨ Tính năng

📸 Camera Snapshot: Hiển thị ảnh khuôn mặt người vừa nhận diện được ngay lập tức (Image Entity).

👤 Tên người (Name): Sensor hiển thị tên người được nhận diện.

🏷️ Loại người (Type): Sensor phân loại: Người nhà, Người quen (ACQ), hoặc Người lạ.

🕒 Thời gian (Time): Sensor hiển thị thời điểm nhận diện cuối cùng.

🏃 Cảm biến chuyển động (Motion): Binary Sensor tự động bật khi có nhận diện và tắt sau 10 giây (dùng để kích hoạt automation).

🚀 Realtime: Cập nhật dữ liệu tức thì (Polling 1s) từ Local Add-on, không độ trễ.

🛠️ Không cần YAML: Cài đặt và cấu hình hoàn toàn qua giao diện UI.

⚠️ Yêu cầu bắt buộc

Integration này cần phải hoạt động song song với Add-on Hanet Bridge Pro.
Bạn phải cài đặt và chạy Add-on trước khi cài Integration này.

Link Add-on: [Link đến repo Add-on của bạn nếu có]

📥 Cài đặt

Cách 1: Qua HACS (Khuyên dùng)

Mở HACS > Integrations.

Bấm vào dấu 3 chấm góc trên bên phải > Custom repositories.

Dán đường dẫn GitHub của repo này vào ô Repository.

Chọn Category là Integration.

Bấm Add, sau đó tìm kiếm "Hanet AI Camera Bridge" và bấm Download.

Khởi động lại Home Assistant.

Cách 2: Cài thủ công

Tải toàn bộ code về máy.

Copy thư mục custom_components/hanet_cloud_pro vào thư mục custom_components trong Home Assistant của bạn.

Khởi động lại Home Assistant.

⚙️ Cấu hình

Sau khi khởi động lại Home Assistant:

Vào Settings (Cài đặt) > Devices & Services (Thiết bị & Dịch vụ).

Bấm nút + ADD INTEGRATION góc dưới bên phải.

Tìm kiếm "Hanet AI Camera Bridge".

Nhập địa chỉ URL của Add-on.

Mặc định nếu chạy Add-on trên cùng máy HA: http://local-hanet-bridge-pro:2900

Nếu Add-on chạy trên máy khác, nhập IP của máy đó (ví dụ: http://192.168.1.100:2900).

Bấm Submit. Hệ thống sẽ tự động quét và thêm tất cả các Camera đã được Add-on nhận diện.

📊 Các thực thể (Entities)

Với mỗi Camera (ví dụ: Device ID: 12345), Integration sẽ tạo ra 1 thiết bị (Device) chứa các thực thể sau:

Tên thực thể

Entity ID

Mô tả

Snapshot

image.camera_12345_snapshot

Ảnh crop khuôn mặt người vừa đi qua.

Tên người

sensor.camera_12345_ten_nguoi

Tên người (hoặc "Unknown").

Loại người

sensor.camera_12345_loai_nguoi

Gia đình / Người quen / Người lạ.

Thời gian

sensor.camera_12345_thoi_gian

Thời gian nhận diện (HH:MM:SS DD/MM).

Motion

binary_sensor.camera_12345_motion

Bật (On) trong 10s khi có người.

🤖 Ví dụ Automation

Kịch bản: Khi phát hiện người lạ, gửi thông báo kèm ảnh chụp nhanh về điện thoại.

alias: Canh bao nguoi la Hanet
description: ""
trigger:
  - platform: state
    entity_id:
      - binary_sensor.cong_chinh_motion  # Thay bằng ID sensor motion của bạn
    to: "on"
condition:
  - condition: state
    entity_id: sensor.cong_chinh_loai_nguoi
    state: "Người lạ"
action:
  - service: notify.mobile_app_iphone
    data:
      message: "Có người lạ tại cổng chính!"
      data:
        image: "/api/image_proxy/image.cong_chinh_snapshot" # Đường dẫn ảnh snapshot
mode: single


❓ Câu hỏi thường gặp (FAQ)

Q: Tại sao ảnh Snapshot hiện dấu chấm hỏi/không tải được?
A: Kiểm tra xem Add-on có đang chạy không. Thử truy cập trực tiếp link Add-on trên trình duyệt để đảm bảo kết nối mạng nội bộ ổn định.

Q: Làm sao để thêm Camera mới?
A: Bạn không cần làm gì cả. Khi Camera mới gửi dữ liệu về Add-on, Integration sẽ tự động phát hiện và tạo entities mới sau vài giây (hoặc bạn có thể Reload lại Integration).

Q: Dữ liệu có bị trễ không?
A: Integration sử dụng cơ chế Local Polling 1 giây/lần cực nhẹ, đảm bảo dữ liệu gần như tức thời (Realtime).

❤️ Credits

Phát triển bởi [trankhanhduy2929-beep]
Dựa trên nền tảng Home Assistant và Hanet AI Camera.
