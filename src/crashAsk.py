import json
import time
import ccxt
from src.config import *
import datetime
from src.inoutargs import parse_args

args = parse_args()

# 定义 API key 和 secret key
apiKey = args.api if args.api is not None else OKAPI
secret = args.secret if args.secret is not None else OKSECRET
passwd = args.passwd if args.passwd is not None else OK_PASSWD
proxy = args.proxy if args.proxy is not None else PROXY

# 定义交易对和交易量
symbol = args.symbol if args.symbol is not None else SYMBOL
amount = args.amount if args.amount is not None else SYMBOL_AMOUNT
sell_price = args.sellprice if args.sellprice is not None else SELL_PRICE
stop_price = args.stopprice if args.stopprice is not None else STOP_PRICE
startTime = args.starttime if args.starttime is not None else StartTime
discount = args.discount if args.discount is not None else DISCOUNT


# 初始化 okex API
#exchange = ccxt.okx
exchange = ccxt.okex({
    'apiKey': apiKey,
    'secret': secret,
    'password': passwd,
    'enableRateLimit': True,  # 启用频率限制'
    'proxies': {
        'http': proxy,
        'https': proxy,
    }
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
    bid_price, ask_price = get_ticker()
    print(f"买一:{bid_price},卖一:{ask_price}")

    # 设置卖单价格
    sell_price = discount*ask_price
    if sell_price < stop_price:
        sell_price = stop_price
        print("卖单价格低于最低卖价，以最低价挂单")

    # 发起市价卖单
    order = exchange.create_order(
        symbol=symbol,
        type='limit',
        side='sell',
        amount=amount,
        price=sell_price,
        #params={'stopPrice': sell_price},
    )
    print("挂了卖单：{},价格：{}".format(order['id'], sell_price))
    return order['id']


# 定义函数，查询订单状态
def check_order_status(order_id):
    order = exchange.fetch_order(order_id, symbol)
    order_status = order['info']['state']

    #print(f"order infor: {order}")
    if order_status == "live":
        print("订单未完全执行，继续等待", end="\r")

    elif order_status == "filled":
        print(f"订单状态:{order['info']['state']}，订单成交价格:{order['info']['fillPx']},"
              f"成交数量:{order['info']['fillSz']},成交金额:{float(order['info']['fillSz'])*float(order['info']['fillPx'])}")

    return order_status



# 定义函数，取消订单
def cancel_order(order_id):
    result = exchange.cancel_order(order_id, symbol)
    return result

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

        dt = datetime.datetime.now() + datetime.timedelta(seconds=last_time)
        delta = dt - datetime.datetime.now()

        format_last_time_string = format_timedelta(delta)
        print("距离开始还差:{}".format(format_last_time_string), end="\r")
        time.sleep(haomiao)
    print("开始抢挂订单")
def Main():

    #开始计时
    countdown()

    #print("symbols", get_ok_symbols())

    #下单
    loop_num = 0
    while True:
        if loop_num%3 == 0:

            order_id = place_sell_order(amount)
        status = check_order_status(order_id)
        if status == 'filled':
            print('市价卖单已成交，订单号：', order_id)
            break
        elif status == "live":
            loop_num += 1
        if loop_num%3 == 0:
            print(f"取消订单{order_id}")
            try:
                cancel_order(order_id)
            except ccxt.base.errors.OrderNotFound as e:
                print(e)
                print("订单在取消前已完成")

            status = check_order_status(order_id)
            print(f"订单状态{status}")
            print(f"已经等待3秒重新挂单", end="\r")

        time.sleep(1)




if __name__ == '__main__':
    Main()
    # main()