import json
import time
import ccxt
import config
import datetime

# 定义 API key 和 secret key
apiKey = config.OKAPI
secret = config.OKSECRET

# 定义交易对和交易量
symbol = 'SUI/USDT'
amount = 0.1

# 初始化 okex API
exchange = ccxt.okex({
    'apiKey': apiKey,
    'secret': secret,
    'enableRateLimit': True,  # 启用频率限制
})


# 定义函数，获取市场价格信息
def get_ticker():
    ticker = exchange.fetch_ticker(symbol)
    return ticker['bid'], ticker['ask']


# 定义函数，发起市价卖单
def place_sell_order(amount):
    # 获取市场价格
    bid_price, ask_price = get_ticker()

    # 设置卖单价格
    sell_price = bid_price + 0.01

    # 发起市价卖单
    order = exchange.create_order(
        symbol=symbol,
        type='market',
        side='sell',
        amount=amount,
        params={'stopPrice': sell_price},
    )

    return order['info']['order_id']


# 定义函数，查询订单状态
def check_order_status(order_id):
    order = exchange.fetch_order(order_id, symbol)
    return order['status']


# 定义函数，取消订单
def cancel_order(order_id):
    exchange.cancel_order(order_id, symbol)

def get_ok_symbols():
    return exchange.symbols


def human_to_unixtime(datestr, format='%Y/%m/%d %H:%M'):
    """将人类时间字符串转换为 Unix 时间戳"""
    dt = datetime.datetime.strptime(datestr, format)
    return int(time.mktime(dt.timetuple()))

def compare_time(target_time):
    """比较指定时间和当前时间的先后顺序，如果当前时间等于或晚于指定时间，返回 True，否则返回 False"""
    current_time = datetime.datetime.now()
    if current_time >= target_time:
        return True
    else:
        return False


def testMain():
    print('testMain')
    bid_price, ask_price = get_ticker()
    print('bid_price', bid_price)
    print('ask_price', ask_price)
    print("test ok symbols")
    #print("symbols", get_ok_symbols())
    # order_id = place_sell_order(amount)
    # print('order_id', order_id)
    # status = check_order_status(order_id)
    # print('status', status)
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