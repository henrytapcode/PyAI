# Vòng lặp dừng khi đủ n

Thay vì dùng slice, cách này đi qua list đã sắp xếp, thêm từng điểm vào một list mới, và dùng `break` để dừng ngay khi list mới đủ `n` phần tử. Cách này dài hơn nhưng mọi bước đều nhìn thấy được, nên rất dễ theo dõi bằng **Visualize**. Slice `ordered[:n]` làm cùng việc trong một dòng, nên hãy ưu tiên nó khi bạn đã quen với slicing.
