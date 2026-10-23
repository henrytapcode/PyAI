Một đồng nghiệp báo cáo: "`last_n` đôi khi trả về quá nhiều." Hàm này phải trả về `n` phần tử cuối của một list, nhưng có một input cho đáp án sai. Hãy làm hai bước, như một lần sửa bug thật.

1. **Tái hiện.** Tìm lời gọi nhỏ nhất làm lộ bug. Cho `reproduce()` trả về nó dưới dạng tuple `(items, n)`. Hãy thử bằng tay trước (ví dụ với **Visualize** hoặc `print`).
2. **Sửa.** Đổi `last_n` để mọi trường hợp trong bảng đều đúng.

**Ví dụ**

| lời gọi | kết quả |
|---|---|
| `last_n([1, 2, 3, 4], 2)` | `[3, 4]` |
| `last_n([1, 2, 3], 10)` | `[1, 2, 3]` |
| `last_n([1, 2, 3, 4], 0)` | `[]` |
| `last_n([1, 2, 3], -1)` | ném `ValueError` |

**Quy tắc**
- Viết code bên trong hai hàm. `reproduce` phải trả về một list và một số.
- Input sai nhỏ nhất có đúng một phần tử.
- Đừng thay đổi list bạn nhận được.
