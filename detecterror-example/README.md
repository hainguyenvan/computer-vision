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
