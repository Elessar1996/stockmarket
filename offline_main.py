from Moving_ARIMA import moving_arima_signal_maker
from Past_Derivative import pd_signal_maker
import pandas as pd
import numpy as np
import datetime
import pandas_datareader as web
from Utils import find_positive_idx
from Utils import element_exist
import requests
from Utils import stop_bleeding
from LSTM import lstm_funcs

stock_symbols = ['MSFT', 'AMZN', 'FB']
list_of_dfs = []
list_lstm_models = []
for i in stock_symbols:
    df = web.DataReader(i, data_source='yahoo', start='2020-01-01', end='2020-11-5')
    df.to_csv(f'{i}.csv')
    df = pd.read_csv(f'{i}.csv')
    x_lstm, y_lstm = lstm_funcs.build_dataset(df['Close'])
    x_lstm = np.reshape(x_lstm, (x_lstm.shape[0], x_lstm.shape[1], 1))
    y_lstm = np.reshape(y_lstm, (y_lstm.shape[0], 1))
    print(x_lstm.shape)
    print(y_lstm.shape)
    lstm_model = lstm_funcs.build_lstm()
    lstm_model.compile(optimizer='adam', loss='mean_squared_error')
    lstm_model.fit(x_lstm, y_lstm, epochs = 1, batch_size = 1)
    list_lstm_models.append(lstm_model)
    list_of_dfs.append(df)


delta = datetime.timedelta(days=1)
signal_day = datetime.date(2020, 2, 5)
b_signal_day = signal_day - datetime.timedelta(days=1)
days_ahead = 180
total_property = 0
total_property_list = [1000]
initial_capital = 1000
total_shares = [0, 0, 0]
current = -100
key_error = False

with open('commands.txt', 'a') as file:
    for q in range(days_ahead):
        print(f'b_signal_weekday is {b_signal_day.weekday()}')

        if b_signal_day.weekday() == 5 or b_signal_day.weekday() == 6:
            b_signal_day += delta
            continue

        profits = []
        methods = []
        signals = []
        stock_prices = []
        lstm_pred = []

        try:
            a_prime = list_of_dfs[0]
            a_zgond = list_lstm_models[0]
            a = a_prime.loc[a_prime['Date'] == str(b_signal_day)]
            day_index_0 = a_prime.index[a_prime['Date'] == str(b_signal_day)].tolist()[0]
            a_prime_prime = a_prime['Close'].values
            # inp_lstm_0 = a_prime_prime[day_index_0-60:day_index_0]
            # print(inp_lstm_0)
            # inp_lstm_0 = np.array(inp_lstm_0, dtype = 'float32')
            # print(inp_lstm_0.shape)
            # inp_lstm_0 = np.reshape(inp_lstm_0, (1,60,1))
            # tom_price_0 = a_zgond.predict(inp_lstm_0)
            if not a.empty:
                sp0 = a
                print(f'a is {a}')
                print(f'sp0 is {sp0}')
            elif a.empty:
                pass



        except (KeyError, requests.exceptions.ConnectionError):

            print(f'There is a serious problem with your Internet Connection')
        try:
            b_prime = list_of_dfs[1]
            b_zgond = list_lstm_models[1]
            b = b_prime.loc[b_prime['Date'] == str(b_signal_day)]
            day_index_1 = b_prime.index[b_prime['Date'] == str(b_signal_day)].tolist()[0]
            b_prime_prime = b_prime['Close'].values
            # inp_lstm_1 = b_prime_prime[day_index_1 - 60:day_index_1]
            # inp_lstm_1 = np.array(inp_lstm_1, dtype='float32')
            # inp_lstm_1 = np.reshape(inp_lstm_1, (1,60, 1))
            # tom_price_1 = b_zgond.predict(inp_lstm_1)
            if not b.empty:
                print(f'b is {b}')
                sp1 = b
                print(f'sp1 is {sp1}')
            elif b.empty:
                pass

        except (KeyError, requests.exceptions.ConnectionError):
            print(f'There is a serious problem with your Internet Connection')
            pass
        try:
            g_prime = list_of_dfs[2]
            g_zgond = list_lstm_models[2]
            g = g_prime.loc[g_prime['Date'] == str(b_signal_day)]
            day_index_2 = g_prime.index[g_prime['Date'] == str(b_signal_day)].tolist()[0]
            g_prime_prime = g_prime['Close'].values
            # inp_lstm_2 = g_prime_prime[day_index_2 - 60:day_index_2]
            # inp_lstm_2 = np.array(inp_lstm_2, dtype='float32')
            # inp_lstm_2 = np.reshape(inp_lstm_2, (1,60,1))
            # tom_price_2 = g_zgond.predict(inp_lstm_2)
            if not g.empty:
                print(f'g is {g}')
                sp2 = g
                print(f'sp2 is {sp2}')
            elif g.empty:
                pass


        except (KeyError, requests.exceptions.ConnectionError):

            print(f'There is a serious problem with your Internet Connection')
        stock_prices.append(sp0)
        stock_prices.append(sp1)
        stock_prices.append(sp2)

        # lstm_pred.append(tom_price_0)
        # lstm_pred.append(tom_price_1)
        # lstm_pred.append(tom_price_2)


        def buy(stock_idx):
            global initial_capital
            global total_shares
            global total_property
            global total_property_list
            # p = stock_prices[stock_idx]['Open'].values * 0.15
            total_shares[stock_idx] = initial_capital / (stock_prices[stock_idx]['Close'])
            initial_capital = 0
            property_0 = (total_shares[0] > 0) * total_shares[0] * stock_prices[0]['Open'].values
            property_1 = (total_shares[1] > 0) * total_shares[1] * stock_prices[1]['Open'].values
            property_2 = (total_shares[2] > 0) * total_shares[2] * stock_prices[2]['Open'].values
            total_property = (initial_capital > 0) * initial_capital + property_0 + property_1 + property_2
            total_property_list.append(total_property)
            print('buy was executed')
            print(f'initial capital : {initial_capital}')
            print(f'total_shares : {total_shares}')
            print(f'current: {current}')
            print(f'Total Property is: {total_property}')


        def sell(stock_idx):
            global initial_capital
            global total_shares
            global total_property
            global total_property_list
            # q = stock_prices[stock_idx]['Open'].values * 0.15
            gained_money = total_shares[stock_idx] * (stock_prices[stock_idx]['Close'])
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
            print(f'Total Property is: {total_property}')


        def hold():
            global total_property
            global total_property_list
            property_0 = (total_shares[0] > 0) * total_shares[0] * stock_prices[0]['Open'].values
            property_1 = (total_shares[1] > 0) * total_shares[1] * stock_prices[1]['Open'].values
            property_2 = (total_shares[2] > 0) * total_shares[2] * stock_prices[2]['Open'].values
            total_property = (initial_capital > 0) * initial_capital + property_0 + property_1 + property_2
            total_property_list.append(total_property)
            print('hold was executed')
            print(f'initial capital : {initial_capital}')
            print(f'total_shares : {total_shares}')
            print(f'Total Property is: {total_property}')


        for i, j in enumerate(stock_symbols):
            print(j)
            try:
                # arima_signal, arima_profit = moving_arima_signal_maker(j, str(b_signal_day), 500)
                sig_and_prof_arima = moving_arima_signal_maker(j, str(b_signal_day), 100, list_lstm_models[i])
                if sig_and_prof_arima is not None:
                    arima_signal, arima_profit_open = sig_and_prof_arima
                else:
                    print("ARIMA CRASHED!!!!!!!!")
                    arima_profit_open = 0
                    # arima_profit_close = 0
                    arima_signal = -1
                    # continue
                # pd_signal, pd_profit = pd_signal_maker(j, str(b_signal_day), 500)
                sig_and_prof_pd = pd_signal_maker(j, str(b_signal_day), 100, list_lstm_models[i])
                if sig_and_prof_pd is not None:
                    pd_signal, pd_profit_open = sig_and_prof_pd
                else:
                    print("PD CRASHED!!!")
                    pd_profit_open = 0
                    # pd_profit_open = 0
                    pd_signal = -1
                    # continue
            except requests.exceptions.ConnectionError:
                print("The internet Connection ruined everything")
                break
            print(f'pd_signal pd_profit: {pd_signal},{pd_profit_open}')
            print(f'arima signal : {arima_signal}, {arima_profit_open}')
            profits.append(max(arima_profit_open, pd_profit_open))
            if arima_profit_open > pd_profit_open:
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
        # if len(total_property_list) >= 2 and initial_capital == 0 and stop_bleeding(
        #         total_property_list[q - 2], total_property_list[q - 1]):
        #     sell(current)
        #     print('You Are So So lucky to have me man! I just saved you from a terrible collapse')
        #     file.write(f'Date: {b_signal_day + delta} ---- command: EMERGENCY!! sell  {stock_symbols[current]} \n')
        if initial_capital > 0:
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
