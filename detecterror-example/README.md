## Algorithms

-   Step1: Handler images patterns
-   Step2: Handler images detects and compares with images pattern
-   Step3: Show result detects

## API

-   1. Sent image example

```
URL: http://localhost:8080/image-examples
Method: POST
BODY:
{
    "image":"base64"
}
```

-   2. Sent image detects

```
URL: http://localhost:8080/detects
Method: POST
BODY:
{
    "image":"base64"
}
```

## Issues

-   Chưa phát khoanh vùng được vị trí mà bị thiếu lỗ
-   Hiện mới chỉ phát hiện các lỗ có area khác nhau hơn 1000
-   Hiện chưa apply thuật toán trừ background
-   Các vật thể phải đặt ở một góc lệch nhất định để xoay nó về cùng một chiều, chưa hỗ trợ việc nhận diện vật thể xoay ở các góc khác nhau
