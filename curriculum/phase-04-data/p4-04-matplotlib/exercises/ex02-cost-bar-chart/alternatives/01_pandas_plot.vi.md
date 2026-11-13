# Vẽ trực tiếp từ pandas Series

Thay vì tách `totals.index.tolist()` và `totals.tolist()` để truyền vào `ax.bar(...)`, cách này gọi thẳng `totals.plot(kind="bar", ax=ax)` trên `Series` vừa tổng hợp. Cách viết này gọn hơn khi khám phá dữ liệu nhanh và tự động đặt nhãn trục x theo tên cột nhóm (`"model"`), trong khi gọi `ax.bar(...)` trực tiếp giúp bạn kiểm soát kiểu dáng cột rõ ràng hơn và giữ nhãn trục x nằm ngang theo mặc định.
