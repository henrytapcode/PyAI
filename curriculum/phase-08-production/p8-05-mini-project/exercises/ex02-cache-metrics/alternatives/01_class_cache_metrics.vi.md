# Tách lớp TTLCache và MetricsTracker riêng biệt

**Cách hoạt động:** Thay vì để trực tiếp dictionary cache và list bản ghi trong closure của `create_app`, cách này giao phần hết hạn cache và tổng hợp metric cho hai lớp riêng (`TTLCache` và `MetricsTracker`) được tạo mới mỗi lần gọi factory.

**Khi nào nên chọn:** Tách riêng giúp unit-test từng thành phần độc lập và dễ thay thế sau này (ví dụ đổi `TTLCache` sang Redis), đổi lại code dài hơn một chút so với biến cục bộ trong closure.
