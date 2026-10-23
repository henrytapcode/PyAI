# Sao chép trước, rồi sắp xếp tại chỗ

`scores[:]` là một slice không giới hạn, nên nó sao chép cả list. Sau đó `copy.sort(reverse=True)` sắp xếp bản sao đó ngay tại chỗ, nên list gốc không bị động tới. Kết quả giống `sorted(scores, reverse=True)`, vốn sao chép và sắp xếp trong một bước. Dùng `sorted()` khi bạn cần một list mới, và chỉ dùng `.sort()` khi bạn sẵn sàng thay đổi chính list đó.
