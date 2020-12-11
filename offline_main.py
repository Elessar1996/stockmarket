from Moving_ARIMA import moving_arima_signal_maker
from Past_Derivative import pd_signal_maker
import pandas as pd
import datetime
from Utils import find_positive_idx
from Utils import element_exist
import requests
from Utils import stop_bleeding

stock_symbols = ['AAPL', 'GOOG', 'TSLA']
AAPL = pd.read_csv('/home/elessar/AAPL.csv')
GOOG = pd.read_csv('/home/elessar/GOOG.csv')
TSLA = pd.read_csv('/home/elessar/TSLA.csv')
list_of_dfs = [AAPL, GOOG, TSLA]
delta = datetime.timedelta(days=1)
signal_day = datetime.date(2020, 2, 1)
b_signal_day = signal_day - datetime.timedelta(days=1)
days_ahead = 100
total_property = 0
total_property_list = [1000]
initial_capital = 1000
total_shares = [0, 0, 0]
current = -100
key_error = False

with open('commands.txt', 'a') as file:
    for q in range(days_ahead):
        profits = []
        methods = []
        signals = []
        stock_prices = []
        try:
            a = AAPL.loc[AAPL['Date'] == str(b_signal_day)]
            if not a.empty:
                sp0 = a
                print(f'sp0 is {sp0}')
            elif a.empty:
                pass


        except KeyError:
            pass
        try:
            b = GOOG.loc[GOOG['Date'] == str(b_signal_day)]
            if not b.empty:
                sp1 = b
                print(f'sp1 is {sp1}')
            elif b.empty:
                pass

        except KeyError:
            pass
        try:
            g = TSLA.loc[TSLA['Date'] == str(b_signal_day)]
            if not g.empty:
                sp2 = g
                print(f'sp2 is {sp2}')
            elif g.empty:
                pass

        except KeyError:
            pass
        stock_prices.append(sp0)
        stock_prices.append(sp1)
        stock_prices.append(sp2)


        def buy(stock_idx):
            global initial_capital
            global total_shares
            global total_property
            global total_property_list
            p = stock_prices[stock_idx]['Close'].values * 0.05
            total_shares[stock_idx] = initial_capital / (stock_prices[stock_idx]['Close'].values + p)
            initial_capital = 0
            property_0 = (total_shares[0] > 0) * total_shares[0] * stock_prices[0]['Close'].values
            property_1 = (total_shares[1] > 0) * total_shares[1] * stock_prices[1]['Close'].values
            property_2 = (total_shares[2] > 0) * total_shares[2] * stock_prices[2]['Close'].values
            total_property = (initial_capital > 0) * initial_capital + property_0 + property_1 + property_2
            total_property_list.append(total_property)
            print('buy was executed')
            print(f'initial capital : {initial_capital}')
            print(f'total_shares : {total_shares}')
            print(f'current: {current}')


        def sell(stock_idx):
            global initial_capital
            global total_shares
            global total_property
            global total_property_list
            q = stock_prices[stock_idx]['Close'].values * 0.05
            gained_money = total_shares[stock_idx] * (stock_prices[stock_idx]['Close'].values - q)
            initial_capital += gained_money
            total_shares[stock_idx] = 0
            property_0 = (total_shares[0] > 0) * total_shares[0] * stock_prices[0]['Close'].values
            property_1 = (total_shares[1] > 0) * total_shares[1] * stock_prices[1]['Close'].values
            property_2 = (total_shares[2] > 0) * total_shares[2] * stock_prices[2]['Close'].values
            total_property = (initial_capital > 0) * initial_capital + property_0 + property_1 + property_2
            total_property_list.append(total_property)
            print('sell was executed')
            print(f'initial capital : {initial_capital}')
            print(f'total_shares : {total_shares}')
            print(f'current: {current}')


        def hold():
            global total_property
            global total_property_list
            property_0 = (total_shares[0] > 0) * total_shares[0] * stock_prices[0]['Close'].values
            property_1 = (total_shares[1] > 0) * total_shares[1] * stock_prices[1]['Close'].values
            property_2 = (total_shares[2] > 0) * total_shares[2] * stock_prices[2]['Close'].values
            total_property = (initial_capital > 0) * initial_capital + property_0 + property_1 + property_2
            total_property_list.append(total_property)
            print('hold was executed')
            print(f'initial capital : {initial_capital}')
            print(f'total_shares : {total_shares}')


        for i, j in enumerate(stock_symbols):
            print(j)
            try:
                # arima_signal, arima_profit = moving_arima_signal_maker(j, str(b_signal_day), 500)
                sig_and_prof_arima = moving_arima_signal_maker(j, str(b_signal_day), 500)
                if type(sig_and_prof_arima) != None:
                    arima_signal, arima_profit = sig_and_prof_arima
                else:
                    continue
                # pd_signal, pd_profit = pd_signal_maker(j, str(b_signal_day), 500)
                sig_and_prof_pd = pd_signal_maker(j, str(b_signal_day), 500)
                if type(sig_and_prof_pd) != None:
                    pd_signal, pd_profit = sig_and_prof_pd
                else:
                    continue
            except requests.exceptions.ConnectionError:
                break
            print(f'pd_signal pd_profit: {pd_signal},{pd_profit}')
            print(f'arima signal : {arima_signal}, {arima_profit}')
            profits.append(max(arima_profit, pd_profit))
            if arima_profit > pd_profit:
                methods.append(0)
                signals.append(arima_signal)
            else:
                methods.append(1)
                signals.append(pd_signal)
        print(f'signals: {signals}')
        copy_profits = profits.copy()
        copy_profits.sort()
        most_valuable = profits.index(copy_profits[-1])
        second_most_valuable = profits.index(copy_profits[-2])
        third = profits.index(copy_profits[-3])
        positive_idx = find_positive_idx(signals)
        print(f'positive idxes : {positive_idx}')
        print(f'initial capital before first cond. : {initial_capital}')
        print(f'most valuable: {most_valuable}')
        print(f'second mv: {second_most_valuable}')
        print(f'third : {third}')
        if len(total_property_list) >= 2 and ((total_property_list[-1]-1000)/10)>10 and stop_bleeding(total_property_list[q-2], total_property_list[q-1]):
            sell(current)
            print('You Are So So lucky to have me man! I just saved you from a terrible collapse')
            file.write(f'Date: {b_signal_day + delta} ---- command: EMERGENCY!! sell  {stock_symbols[current]} \n')
        elif initial_capital > 0:
            print(f'app has gone in to ic >0')
            if all(flag > 0 for flag in signals):
                buy(most_valuable)
                current = most_valuable
                file.write(f'Date: {b_signal_day + delta} ---- command: buy {stock_symbols[current]} \n')
                file.write(f'total property: {total_property}\n')
            elif all(flag < 0 for flag in signals):
                hold()
                current = -100
                file.write(f'Date: {b_signal_day + delta} ---- command: hold \n')
                file.write(f'total property: {total_property}\n')
            elif element_exist(positive_idx, most_valuable):
                buy(most_valuable)
                current = most_valuable
                file.write(f'Date: {b_signal_day + delta} ---- command: buy {stock_symbols[current]} \n')
                file.write(f'total property: {total_property}\n')
            elif not element_exist(positive_idx, most_valuable) and element_exist(positive_idx,
                                                                                  second_most_valuable):
                buy(second_most_valuable)
                current = second_most_valuable
                file.write(f'Date: {b_signal_day + delta} ---- command: buy {stock_symbols[current]} \n')
                file.write(f'total property: {total_property}\n')
            elif not element_exist(positive_idx, most_valuable) and not element_exist(positive_idx,
                                                                                      second_most_valuable) and element_exist(
                positive_idx, third):
                buy(third)
                current = third
                file.write(f'Date: {b_signal_day + delta} ---- command: buy {stock_symbols[current]} \n')
                file.write(f'total property: {total_property}\n')
        elif initial_capital == 0:
            print('app has gone into ic ==0')
            if current == most_valuable:
                if element_exist(positive_idx, most_valuable):
                    hold()
                    file.write(f'Date: {b_signal_day + delta} ---- command: hold \n')
                    file.write(f'total property: {total_property}\n')
                elif not element_exist(positive_idx, most_valuable):
                    if element_exist(positive_idx, second_most_valuable):
                        sell(most_valuable)
                        buy(second_most_valuable)
                        current = second_most_valuable
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[most_valuable]} and buy {stock_symbols[second_most_valuable]} \n')
                        file.write(f'total property: {total_property}\n')
                    elif not element_exist(positive_idx, second_most_valuable):
                        if element_exist(positive_idx, third):
                            sell(most_valuable)
                            buy(third)
                            current = third
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[most_valuable]} and buy {stock_symbols[third]} \n')
                            file.write(f'total property: {total_property}\n')
                        elif not element_exist(positive_idx, third):
                            sell(most_valuable)
                            current = -100
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[most_valuable]}  \n')
                            file.write(f'total property: {total_property}\n')
            elif current == second_most_valuable:
                if element_exist(positive_idx, second_most_valuable):
                    if element_exist(positive_idx, most_valuable):
                        sell(second_most_valuable)
                        buy(most_valuable)
                        current = most_valuable
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[second_most_valuable]} and buy {stock_symbols[most_valuable]} \n')
                        file.write(f'total property: {total_property}\n')
                    elif not element_exist(positive_idx, most_valuable):
                        hold()
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: hold \n')
                        file.write(f'total property: {total_property}\n')
                elif not element_exist(positive_idx, second_most_valuable):
                    if element_exist(positive_idx, most_valuable):
                        sell(second_most_valuable)
                        buy(most_valuable)
                        current = most_valuable
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[second_most_valuable]} and buy {stock_symbols[most_valuable]} \n')
                        file.write(f'total property: {total_property}\n')
                    elif not element_exist(positive_idx, most_valuable):
                        if element_exist(positive_idx, third):
                            sell(second_most_valuable)
                            buy(third)
                            current = third
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[second_most_valuable]} and buy {stock_symbols[third]} \n')
                            file.write(f'total property: {total_property}\n')
                        elif not element_exist(positive_idx, third):
                            sell(second_most_valuable)
                            current = -100
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[second_most_valuable]}  \n')
                            file.write(f'total property: {total_property}\n')
            elif current == third:
                if element_exist(positive_idx, third):
                    if element_exist(positive_idx, most_valuable):
                        sell(third)
                        buy(most_valuable)
                        current = most_valuable
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[third]} and buy {stock_symbols[most_valuable]} \n')
                        file.write(f'total property: {total_property}\n')
                    elif not element_exist(positive_idx, most_valuable):
                        if element_exist(positive_idx, second_most_valuable):
                            sell(third)
                            buy(second_most_valuable)
                            current = second_most_valuable
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[third]} and buy {stock_symbols[second_most_valuable]} \n')
                            file.write(f'total property: {total_property}\n')
                        elif not element_exist(positive_idx, second_most_valuable):
                            hold()
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: hold \n')
                            file.write(f'total property:  {total_property} \n')
                elif not element_exist(positive_idx, third):
                    if element_exist(positive_idx, most_valuable):
                        sell(third)
                        buy(most_valuable)
                        current = most_valuable
                        file.write(
                            f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[third]} and buy {stock_symbols[most_valuable]} \n')
                        file.write(f'total property: {total_property}\n')
                    elif not element_exist(positive_idx, most_valuable):
                        if element_exist(positive_idx, second_most_valuable):
                            sell(third)
                            buy(second_most_valuable)
                            current = second_most_valuable
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[third]} and buy {stock_symbols[second_most_valuable]} \n')
                            file.write(f'total property: {total_property} \n')
                        elif not element_exist(positive_idx, second_most_valuable):
                            print('we are there')
                            sell(third)
                            current = -100
                            file.write(
                                f'Date: {b_signal_day + delta} ---- command: sell {stock_symbols[third]} \n')
                            file.write(f'total property: {total_property}\n')
        print(current)
        b_signal_day += delta
