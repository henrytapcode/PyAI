# F-string và một biến đếm

Cách này đếm số chuỗi bị bỏ qua trong `skipped` và tính số điểm hợp lệ bằng phép trừ. Nó cũng tạo thông điệp bằng f-string. Kết quả giống nhau nên test vẫn pass, nhưng mỗi f-string đều được tạo ra kể cả khi mức log sẽ bỏ thông điệp đi (§5). Hãy ưu tiên đối số `%s` trong code ghi log bên trong vòng lặp bận rộn. Biến đếm là ý hay khi bạn cần số dòng bị bỏ qua cho một báo cáo, khi đó bạn dùng lại được `skipped`.
