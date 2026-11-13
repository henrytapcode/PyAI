Viết hai hàm để tổng hợp và vẽ biểu đồ báo cáo sử dụng API theo từng model từ một `DataFrame` **đã được làm sạch**. Hãy viết code bên trong `model_report` và `plot_report` rồi `return` kết quả tương ứng.

**Ví dụ**

`df` đầu vào (đã sạch):

```text
  request_id   model  tokens  latency_ms status  rating
0        r01  gpt-4o    1200       850.0     ok     5.0
1        r02  gpt-4o     800         NaN  error     NaN
2        r03    mini     300       200.0     ok     4.0
```

`model_report(df)` trả về:

```text
    model  requests  total_tokens  error_rate  avg_latency  avg_rating
0  gpt-4o         2          2000         0.5        850.0         5.0
1    mini         1           300         0.0        200.0         4.0
```

Và `plot_report(report)` vẽ biểu đồ cột gồm `"gpt-4o"` (`2000`) rồi `"mini"` (`300`), trả về `(fig, ax)`.

**Quy tắc**

- `model_report(df)`:
  - Đưa `df` vào database SQLite trong RAM (`sqlite3.connect(":memory:")`) bằng `df.to_sql(...)`, chạy **một** câu truy vấn `GROUP BY model` qua `pd.read_sql_query(...)`, rồi đóng kết nối trước khi trả về.
  - Trả về đúng thứ tự cột: `["model", "requests", "total_tokens", "error_rate", "avg_latency", "avg_rating"]`.
  - Làm tròn `error_rate` tới `3` chữ số, `avg_latency` tới `1` chữ số và `avg_rating` tới `2` chữ số (nếu một model thiếu toàn bộ rating thì `avg_rating` là `NaN`).
  - Sắp xếp theo `total_tokens` giảm dần, hòa thì xếp `model` tăng dần, index `0..n-1`.
  - Không làm thay đổi `df` đầu vào.
- `plot_report(report)`:
  - Vẽ biểu đồ cột `total_tokens` theo `model` giữ nguyên thứ tự của `report`.
  - Đặt tiêu đề `"Tokens by model"` và nhãn trục y `"tokens"`.
  - Trả về `(fig, ax)`, không gọi `plt.show()` và không sửa `report`.
