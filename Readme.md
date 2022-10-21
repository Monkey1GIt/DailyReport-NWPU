# Daily Report of NWPU

## Introduction

The project aims to submit daily report of epidemic situation of NWPU automatically. Although you can submit on APP simply, but sometimes you will forget. You can run the code on your PC、raspberry pi、VPS regularly.

![](https://i.loli.net/2021/08/05/8zg19ul25qocf6k.png)

## Installtion

### Environment

1. python3
2. [Selenium](https://selenium-python.readthedocs.io/installation.html)

In `Raspberry Pi` you can use `sudo apt install chromium-chromedriver` to install selenium.

### Package of Python

1. requests
2. selenium

```bash
cd DailyReport-NWPU && python main.py your_username your_password
```

If it succeeded, the console will print:

> NWPU每日疫情填报: OK: 

and 

1. if your fill in the form manually, the script will not fill again and print `NWPU每日疫情填报: OK: Have Signed!  `
2. the srcpit will keep the last value of form and automatically submit
