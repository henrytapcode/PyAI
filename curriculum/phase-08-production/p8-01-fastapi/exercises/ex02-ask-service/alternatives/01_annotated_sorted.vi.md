# Dùng kiểu Annotated tái sử dụng cùng comprehension và sorted()

Cách làm thay thế này (giới thiệu trước `typing.Annotated` của Python) gắn ràng buộc `Field(...)` vào các tên kiểu dùng lại được (`QuestionText`, `TopK`) và tính `ranked` bằng comprehension kết hợp `sorted(..., key=...)` thay vì dùng vòng lặp `for` thêm từng phần tử. Hãy chọn `Annotated` khi nhiều model Pydantic dùng chung một ràng buộc, còn giữ `= Field(...)` trực tiếp cùng vòng lặp `for` khi schema chỉ dùng một lần hoặc cần dễ đọc từng bước khi debug.
