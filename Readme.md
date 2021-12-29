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

## Config

There are `.json` files in folder `User`, you should fill your information in fields.

### Userinfo.json

|   key    |             value             |   sample   |
| :------: | :---------------------------: | :--------: |
| USERNAME |          Student ID           | 2019123456 |
| PASSWORD | Your password of ecampus.nwpu |  nwpu0001  |

### Context.json

In school

|     key     |      value      |    sample    |
| :---------: | :-------------: | :----------: |
| userLoginId |   Student ID    |  2019123456  |
|  userName   |    Your name    |     张三     |
|    xymc     | Name of college | 电子信息学院 |


In home

|   key    |             value             |       sample       |
| :------: | :---------------------------: | :----------------: |
|  szcsbm  | The zip code of your location |       710100       |
|  szcsmc  |         Your location         | 陕西省西安市长安区 |
| userName |           Your name           |        张三        |

## Usage

```bash
cd DailyReport-NWPU && python main.py
```

If it succeeded, the console will print:

> {'DailyReportNWPU': 'OK'}

If you fill multiple information in `context.json`, the scirpt will execution batchly.

