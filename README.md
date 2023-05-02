# okx-crash
OKX平台的挂单抢卖小程序

usage: main.py [-h] [-a API] [-s SECRET] [-p PASSWD] [-t STARTTIME] [-m SYMBOL] [-n AMOUNT] [-r SELLPRICE] [-o STOPPRICE] [-d DISCOUNT] [-x PROXY]

OKX 抢卖程序

optional arguments:
  -h, --help            show this help message and exit
  -a API, --api API     OKAPI 的 API
  -s SECRET, --secret SECRET
                        OKAPI 的 SECRET
  -p PASSWD, --passwd PASSWD
                        OKAPI 的 PASSWD
  -t STARTTIME, --starttime STARTTIME
                        开始时间, 例如"2023/5/01 15:44:00"
  -m SYMBOL, --symbol SYMBOL
                        交易对, 例如"OKB/USDT"
  -n AMOUNT, --amount AMOUNT
                        交易量, 例如"1"
  -r SELLPRICE, --sellprice SELLPRICE
                        卖出价格,在这个版本中没有用, 例如"46.3"
  -o STOPPRICE, --stopprice STOPPRICE
                        最低卖价,低于此价格不会挂单 例如"1"
  -d DISCOUNT, --discount DISCOUNT
                        卖一折扣卖价, 例如"0.8"
  -x PROXY, --proxy PROXY
                        代理, 例如"http://127.0.0.1:7890
