# simulating stock market system
import pandas as pd
from ntpdatetime import now
import numpy as np

# 数字转str，逆操作int()
def To_str(series_number,length=10):
    tmp = str(series_number)
    return '0'*(length-len(tmp))+tmp

# 证券类
stock_list = []
class stock:
    def __init__(self,name):
        self.name = name
        self.price = 1
        self.order_buy_list = {}
        self.order_sell_list = {}
        stock_list.append(name)
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
    def order_buy(self,price,quantity):
        if self.order_buy_list.get(price) == None:
            self.order_buy_list.setdefault(price,quantity)
            self.print()
            self.married()
        else:
            self.order_buy_list[price] = self.order_buy_list[price] + quantity
            self.print()
    def order_sell(self,price,quantity):
        if self.order_sell_list.get(price) == None:
            self.order_sell_list.setdefault(price,quantity)
            self.print()
            self.married()
        else:
            self.order_sell_list[price] = self.order_sell_list[price] + quantity
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
user_list = []
class account:
    def __init__(self,name):
        self.stocks = {}
        self.wealth = 0
        self.history = []
        self.name = name
        user_list.append(name)
        # 登记录进服务器端
    def buy(self,stock,price,quantity):
        if self.wealth < price*quantity:
            print("资金不足")
            return
        self.wealth -= price * quantity
        eval(stock).order_buy(price,quantity)
        # self.stocks.setdefault(name,quantity)
    def sell(self):
        return
    def done(self):
        return
# 买单与卖单的撮合
class Serial:
    serial_detail = {}
    serial_number = 0
    done_serial_number = 0
    def trade(self):
        self.serial_number += 1
        return self.serial_number
    def done(self):
        self.done_serial_number += 1
        return self.done_serial_number
serial_centre = Serial()

# done -1取消 0挂单中 1成交
# {'serial_number':['account','type','stock','price','quantity','time','done','rival_series','done_time']}
class Serial_number():
    def __init__(self,account,type,stock,price,quantity):
        serial_number = serial_centre.trade()
        serial_centre.serial_detail[serial_number] = [account, type, stock, price, quantity,
                                                          now()[0].strftime('%d-%m-%Y %H:%M:%S'), 0, None, None]
        eval(account).history.append(serial_number)
    # 交易完成的单号记录
    def done(self,serial_number1,serial_number2):
        tmp = now()[0].strftime('%d-%m-%Y %H:%M:%S')
        serial_centre.serial_detail[serial_number1][7] = serial_number2
        serial_centre.serial_detail[serial_number1][8] = tmp
        serial_centre.serial_detail[serial_number1][6] = 1
        serial_centre.serial_detail[serial_number2][7] = serial_number1
        serial_centre.serial_detail[serial_number2][8] = tmp
        serial_centre.serial_detail[serial_number2][6] = 1
    def married(self,stock):
        # type交易类型是买还是卖
        if len(eval(stock).order_sell_list.keys())==0 or len(eval(stock).order_buy_list.keys())==0:
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
# a['a'] = [zcyl.order_buy_list, zcyl.order_sell_list]

if __name__ == "__main__":
    # 仲村由理
    if 0:
        zcyl = stock('zcyl')
        zcyl.order_buy(1,100)
        zcyl.order_sell(1,100)

        zcyl = stock('zcyl')
        zcyl.order_buy(1, 100)
        zcyl.order_buy(1.1, 100)
        zcyl.order_buy(1.11, 100)
        zcyl.order_sell(1, 200)

        zcyl = stock('zcyl')
        zcyl.order_buy(1, 100)
        zcyl.order_buy(1.1, 100)
        zcyl.order_buy(1.11, 100)
        zcyl.order_sell(1, 300)

        zcyl = stock('zcyl')
        zcyl.order_sell(1, 100)
        zcyl.order_sell(1.1, 100)
        zcyl.order_sell(1.11, 100)
        zcyl.order_buy(0.9, 520)
        zcyl.order_buy(1.2, 520)

    lsn = account('lsn')
    lrq = account('lrq')

    Serial_number('lsn', 0, 'zcyl', 20, 200)

