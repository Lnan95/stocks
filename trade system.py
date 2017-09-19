# simulating stock market system
import pandas as pd
from ntpdatetime import now
import numpy as np

# 时间函数

class stock:
    def __init__(self):
        self.price = 1
        self.order_buy_list = {}
        self.order_sell_list = {}

    def print(self,type=0):
        # 0 打印两个，1打印购买，2打印出售
        if type == 0:
            print("购买挂单",self.order_buy_list)
            print("出售挂单",self.order_sell_list)
        elif type ==1 :
            print("购买挂单", self.order_buy_list)
        else:
            print("出售挂单", self.order_sell_list)
    # 下单
    def order_buy(self,price,number):
        if self.order_buy_list.get(price) == None:
            self.order_buy_list.setdefault(price,number)
            self.print()
            self.married()
        else:
            self.order_buy_list[price] = self.order_buy_list[price] + number
            self.print()
    def order_sell(self,price,number):
        if self.order_sell_list.get(price) == None:
            self.order_sell_list.setdefault(price,number)
            self.print()
            self.married()
        else:
            self.order_sell_list[price] = self.order_sell_list[price] + number
            self.print()
    # 撮合竞价
    def married(self):
        # type交易类型是买还是卖
        if len(self.order_sell_list.keys())==0 or len(self.order_buy_list.keys())==0:
            return
        highest_buy_price = sorted(self.order_buy_list.keys())[-1]
        lowest_sell_price  = sorted(self.order_sell_list.keys())[0]
        # print(highest_buy_price,lowest_sell_price)
        # 买价大于等于卖价有3种情况;买量大于/等于/小于卖量
        if highest_buy_price >= lowest_sell_price:
            if self.order_buy_list[highest_buy_price] < self.order_sell_list[lowest_sell_price]:
                # 补充账户变化
                self.order_sell_list[lowest_sell_price] = self.order_sell_list[lowest_sell_price] - self.order_buy_list[highest_buy_price]
                del self.order_buy_list[highest_buy_price]
                self.print()
                self.married()
                return
            if self.order_buy_list[highest_buy_price] == self.order_sell_list[lowest_sell_price]:
                # 补充账户变化
                del self.order_sell_list[lowest_sell_price]
                del self.order_buy_list[highest_buy_price]
                self.print()
                return
            if self.order_buy_list[highest_buy_price] > self.order_sell_list[lowest_sell_price]:
                self.order_buy_list[highest_buy_price] = self.order_buy_list[highest_buy_price] - self.order_sell_list[lowest_sell_price]
                del self.order_sell_list[lowest_sell_price]
                self.print()
                self.married()
                return

# account
# 后续需要加入交易单号，交易成功后划入账号内
class account:
    def __init__(self):
        self.stocks = {}
        self.wealth = 0
        # 登记录进服务器端
    def buy(self,name,price,number):
        if self.wealth < price*number:
            print("资金不足")
            return
        self.wealth -= price * number
        name.order_buy(price,number)
        # self.stocks.setdefault(name,number)
    def sell(self):
        return
    def history(self):
        return
    def done(self):
        return
# 买单与卖单的撮合
class Serial:
    sell_serial_number = 0
    buy_serial_number = 0
    done_serial_number = 0
    def buy(self):
        self.buy_serial_number += 1
        return self.buy_serial_number-1
    def sell(self):
        self.sell_serial_number += 1
        return self.buy_serial_number-1
    def done(self):
        self.done_serial_number += 1
        return self.done_serial_number - 1
serial_centre = Serial()

class Serial_number():
    def __init__(self,account,type,stock,price,number):
        self.account = account
        self.type = type
        self.stock = stock
        self.number = number
        self.price = price
        self.time = now()[0].strftime('%d-%m-%Y %H:%M:%S')
        if type == 0:
            self.series = serial_centre.sell()
        else:
            self.series = serial_centre.buy()
        self.rival_series = None
        self.done = 0
        self.done_time = None
    def done(self,series_number):
        self.rival_series = series_number
        self.done = 1
        self.done_time = now()[0].strftime('%d-%m-%Y %H:%M:%S')


if __name__ == "__main__":
    # 仲村由理
    if 0:
        zcyl = stock()
        zcyl.order_buy(1,100)
        zcyl.order_sell(1,100)

        zcyl = stock()
        zcyl.order_buy(1, 100)
        zcyl.order_buy(1.1, 100)
        zcyl.order_buy(1.11, 100)
        zcyl.order_sell(1, 200)

        zcyl = stock()
        zcyl.order_buy(1, 100)
        zcyl.order_buy(1.1, 100)
        zcyl.order_buy(1.11, 100)
        zcyl.order_sell(1, 300)

        zcyl = stock()
        zcyl.order_sell(1, 100)
        zcyl.order_sell(1.1, 100)
        zcyl.order_sell(1.11, 100)
        zcyl.order_buy(0.9, 520)
        zcyl.order_buy(1.2, 520)

    lsn = account()
    lrq = account()

    Serial_number('lsn', 0, 'zz', 20, 200)

