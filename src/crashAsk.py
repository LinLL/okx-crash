import json
import time
import ccxt
import config
import datetime
from inoutargs import parse_args

args = parse_args()

# 定义 API key 和 secret key
apiKey = args.api if args.api is not None else config.OKAPI
secret = args.secret if args.secret is not None else config.OKSECRET
passwd = args.passwd if args.passwd is not None else config.OK_PASSWD

# 定义交易对和交易量
symbol = args.symbol if args.symbol is not None else config.SYMBOL
amount = args.amount if args.amount is not None else config.SYMBOL_AMOUNT
sell_price = args.sellprice if args.sellprice is not None else config.SELL_PRICE

startTime = args.starttime if args.starttime is not None else config.StartTime

# 初始化 okex API
#exchange = ccxt.okx
exchange = ccxt.okex({
    'apiKey': apiKey,
    'secret': secret,
    'password': passwd,
    'enableRateLimit': True,  # 启用频率限制
})
exchange.set_sandbox_mode(True)
#exchange.verbose = True


# 定义函数，获取市场价格信息
def get_ticker():
    ticker = exchange.fetch_ticker(symbol)
    return ticker['bid'], ticker['ask']


# 定义函数，发起市价卖单
def place_sell_order(amount):
    # 获取市场价格
    #bid_price, ask_price = get_ticker()

    # 设置卖单价格
    #sell_price = bid_price + 0.01

    # 发起市价卖单
    order = exchange.create_order(
        symbol=symbol,
        type='limit',
        side='sell',
        amount=amount,
        price=sell_price,
        #params={'stopPrice': sell_price},
    )
    print(order)
    return order['id']


# 定义函数，查询订单状态
def check_order_status(order_id):
    order = exchange.fetch_order(order_id, symbol)
    return order['status']


# 定义函数，取消订单
def cancel_order(order_id):
    exchange.cancel_order(order_id, symbol)

def get_ok_symbols():
    return exchange.symbols


def human_to_unixtime(datestr, format='%Y/%m/%d %H:%M:%S'):
    """将人类时间字符串转换为 Unix 时间戳"""
    dt = datetime.datetime.strptime(datestr, format)
    return dt.timestamp()

def compare_time(target_time):
    """比较指定时间和当前时间的先后顺序，如果当前时间等于或晚于指定时间，返回 True，否则返回 False"""
    current_time = datetime.datetime.now()
    current_time = current_time.timestamp()
    if current_time >= int(target_time):
        return True
    else:
        return False

def format_timedelta(td):
    """格式化 timedelta 为字符串"""
    days, seconds = td.days, td.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"

def countdown():
    targetTime = human_to_unixtime(startTime)
    while not compare_time(targetTime):
        #print("等待时间未到达...")
        # print(targetTime, time.time())
        last_time = targetTime - float(time.time())
        haomiao = last_time - int(last_time)
        # print(haomiao)
        dt = datetime.datetime.now() + datetime.timedelta(seconds=last_time)
        delta = dt - datetime.datetime.now()

        format_last_time_string = format_timedelta(delta)
        print("距离开始还差:{}".format(format_last_time_string), end="\r")
        time.sleep(haomiao)
    print("开始抢挂订单")
def testMain():
    # print('testMain')
    # #bid_price, ask_price = get_ticker()
    # #print('bid_price', bid_price)
    # #print('ask_price', ask_price)
    print("test countdown")
    countdown()

    #print("symbols", get_ok_symbols())

    #测试下单
    order_id = place_sell_order(amount)
    print('order_id', order_id)
    status = check_order_status(order_id)
    print('status', status)
    # cancel_order(order_id)
    # print('cancel_order', order_id)

# 主程序
def main():
    while True:
        # 获取市场价格
        bid_price, ask_price = get_ticker()

        # 如果市场价格超过预期价格，发起市价卖单
        if ask_price > 2500:
            print('市场价格超过2500，发起抢卖...')
            order_id = place_sell_order(amount)
            print('已发起市价卖单，订单号：', order_id)

            # 等待订单成交
            while True:
                status = check_order_status(order_id)
                if status == 'closed':
                    print('市价卖单已成交，订单号：', order_id)
                    break
                else:
                    time.sleep(1)
                    print('订单状态：', status)

            # 取消未成交的订单
            if status != 'closed':
                print('市价卖单未成交，取消订单：', order_id)
                cancel_order(order_id)

        # 每隔一段时间检查一次市场价格
        time.sleep(10)

if __name__ == '__main__':
    testMain()
    # main()