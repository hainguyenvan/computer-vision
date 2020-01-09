## List Error Detects
* Mất mát lỗ
* Lỗi bề mặt không quá 15px
* Lỗi viền

## Algorithms
* Step 1: Tách ảnh khỏi nền
* Step 2: Chuyển sang ảnh hsv
* Step 3: Trừ nền
  -> Lấy ảnh thu được từ camera, sau đó trừ nền với ảnh mẫu
* Step 4: Đưa lỗi vào training
* Step 5: Nhận diện
  -> Nhận diện lỗi
  -> Sử dụng tensorflow lite