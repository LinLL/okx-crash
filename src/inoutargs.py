import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="OKX 抢卖程序")
    parser.add_argument('-a', '--api', type=str, help='OKAPI 的 API')
    parser.add_argument("-s", "--secret", type=str, help="OKAPI 的 SECRET")
    parser.add_argument("-p", "--passwd", type=str, help="OKAPI 的 PASSWD")
    parser.add_argument("-t", "--starttime", type=str, help="开始时间, 例如\"2023/5/01 15:44:00\"", default="2023/5/03 14:00:00")
    parser.add_argument("-m", "--symbol", type=str, help="交易对, 例如\"OKB/USDT\"", default="SUI/USDT")
    parser.add_argument("-n", "--amount", type=str, help="交易量, 例如\"1\"", default=1500)
    parser.add_argument("-r", "--sellprice", type=float, help="卖出价格,在这个版本中没有用, 例如\"46.3\"", default=3)
    parser.add_argument("-o", "--stopprice", type=float, help="最低卖价,低于此价格不会挂单 例如\"1\"", default=1)
    parser.add_argument("-d", "--discount", type=float, help="卖一折扣卖价, 例如\"0.8\"", default=0.8)
    parser.add_argument("-x", "--proxy", type=str, help="代理, 例如\"http://127.0.0.1:7890", default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if args.api:
        print(f"OKAPI 的 API 为 {args.api}")
    if args.starttime:
        print(f"开始时间为 {args.starttime}")
    print(args)
