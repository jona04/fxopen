import pandas as pd
import datetime as dt
import numpy as np

BUY_REVERSE = 1
SELL_REVERSE = -1
BUY_TREND = 2
SELL_TREND = -2
NONE = 0

TRIGGER_TYPE_TP = 1
TRIGGER_TYPE_SL = 2
TRIGGER_TYPE_ACUMULATED_LOSS = 3
TRIGGER_TYPE_REVERSED_CROSS = 4

def remove_spread(df):
    for a in ["ask", "bid"]:
        for b in ["o", "h", "l", "c"]:
            c = f"{a}_{b}"
            df[c] = df[f"mid_{b}"]

def apply_signals(df,sig, spread_limit):
    df["SIGNAL"] = df.apply(sig, spread=spread_limit, axis=1)

def apply_final_signals(df):
    df['FINAL_SIGNAL'] = 0

    delta_ema = df.DELTA_EMA
    delta_ema_prev = df.DELTA_EMA_PREV
    signal = df.SIGNAL
    signal_trend = df.SIGNAL_TREND
    final_signal = df.FINAL_SIGNAL

    for ind in range(df.shape[0]):
        if signal[ind] == SELL_REVERSE:
            for sub_ind in range(ind, df.shape[0]):
                if delta_ema[sub_ind] < 0 and delta_ema_prev[sub_ind] >= 0:
                    final_signal[sub_ind] = SELL_REVERSE
                    break
        elif signal[ind] == BUY_REVERSE:
            for sub_ind in range(ind, df.shape[0]):
                if delta_ema[sub_ind] > 0 and delta_ema_prev[sub_ind] <= 0:
                    final_signal[sub_ind] = BUY_REVERSE
                    break
    
    df["FINAL_SIGNAL"] = final_signal

    i = 0
    while i < len(df):
        if signal_trend[i] == BUY_TREND:
            # Percorre um loop interno a partir do índice i+1
            for j in range(i+1, len(df)):
                # Condição para satisfazer
                if final_signal[j] == SELL_REVERSE:
                    final_signal[i] = BUY_TREND
                    i = j  # Atualiza o índice 'i' para o valor de 'j'
                    break  # Encerra o loop interno
            else:
                i += 1 
        elif signal_trend[i] == SELL_TREND:
            # Percorre um loop interno a partir do índice i+1
            for j in range(i+1, len(df)):
                # Condição para satisfazer
                if final_signal[j] == BUY_REVERSE:
                    final_signal[i] = SELL_TREND
                    i = j  # Atualiza o índice 'i' para o valor de 'j'
                    break  # Encerra o loop interno
            else:
                i += 1 
        else:
            i += 1  # Incrementa 'i' se a condição SIGNAL == 1 não for atendida
            
    df["FINAL_SIGNAL"] = final_signal

def apply_short_signals(df,sig):
    df["SIGNAL_TREND"] = df.apply(sig, axis=1)

INDEX_bid_c = 0
INDEX_ask_c = 1
INDEX_FINAL_SIGNAL = 2
INDEX_time = 3
INDEX_bid_h = 4
INDEX_bid_l = 5
INDEX_ask_h = 6
INDEX_ask_l = 7
INDEX_name = 8
INDEX_SIGNAL = 9
INDEX_delta_ema_mid = 10
INDEX_delta_ema_mid_prev = 11
INDEX_delta_ema_high = 12
INDEX_delta_ema_high_prev = 13
INDEX_delta_ema_low = 14
INDEX_delta_ema_low_prev = 15


class Trade:
    def __init__(self, list_values, index, profit_factor, loss_factor, pip_value,trans_cost,neg_multiplier):
        self.running = True
        self.start_index_m5 = list_values[INDEX_name][index]
        self.profit_factor = profit_factor
        self.loss_factor = loss_factor
        self.pip_value = pip_value
        # self.SL_value = list_values[INDEX_SL_VALUE][index]
        self.count = 0
        self.neg_multiplier = neg_multiplier
        self.trans_cost = trans_cost
        self.trigger_type = NONE

        if list_values[INDEX_FINAL_SIGNAL][index] in [BUY_REVERSE, BUY_TREND]:
            self.start_price = list_values[INDEX_bid_c][index]
            self.trigger_price = list_values[INDEX_bid_c][index]
            
        if list_values[INDEX_FINAL_SIGNAL][index] in [SELL_REVERSE, SELL_TREND]:
            self.start_price = list_values[INDEX_ask_c][index]
            self.trigger_price = list_values[INDEX_ask_c][index]
            
        self.SIGNAL = list_values[INDEX_SIGNAL][index]
        self.FINAL_SIGNAL = list_values[INDEX_FINAL_SIGNAL][index]
        self.result = 0.0
        self.end_time = list_values[INDEX_time][index]
        self.start_time = list_values[INDEX_time][index]
    
    def close_trade(self, list_values, index, result, trigger_price, acumulated_loss):
        self.running = False
        self.result = result - self.trans_cost
        self.end_time = list_values[INDEX_time][index]
        self.trigger_price = trigger_price

        min_acumulated_loss = acumulated_loss[0] if len(acumulated_loss) > 0 else 0.0

        if result < 0.0:
            acumulated_loss.append(abs(result))
        #     self.result = result
        # else:
        #     self.result = result

        if min_acumulated_loss > 0.0:
            if result >= self.neg_multiplier*min_acumulated_loss:
                if len(acumulated_loss) > 0:
                    acumulated_loss = acumulated_loss[1:]
                # print("zerou agora",len(acumulated_loss))

        return acumulated_loss

    def update(self, list_values, index, acumulated_loss):
        # self.acumulated_sum_loss = acumulated_loss

        min_acumulated_loss = acumulated_loss[0] if len(acumulated_loss) > 0 else 0.0
        value_loss_trans_cost = (self.neg_multiplier*min_acumulated_loss) + self.trans_cost
        self.count += 1
        close_op = False
        if self.FINAL_SIGNAL == BUY_REVERSE:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = TRIGGER_TYPE_ACUMULATED_LOSS
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_delta_ema_mid][index] < 0 and list_values[INDEX_delta_ema_mid_prev][index] >= 0 :
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == BUY_REVERSE:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == SELL_REVERSE:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
            
        if self.FINAL_SIGNAL == SELL_REVERSE:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = TRIGGER_TYPE_ACUMULATED_LOSS
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_delta_ema_mid][index] > 0 and list_values[INDEX_delta_ema_mid_prev][index] <= 0 :
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == SELL_REVERSE:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == BUY_REVERSE:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)



        if self.FINAL_SIGNAL == BUY_TREND:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = TRIGGER_TYPE_ACUMULATED_LOSS
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_delta_ema_low][index] < 0 and list_values[INDEX_delta_ema_mid_prev][index] >= 0 :
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                # if list_values[INDEX_FINAL_SIGNAL][index] == SELL_REVERSE:
                #     self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                #     result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                #     acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == BUY_TREND:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
            
        if self.FINAL_SIGNAL == SELL_TREND:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = TRIGGER_TYPE_ACUMULATED_LOSS
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_delta_ema_high][index] > 0 and list_values[INDEX_delta_ema_high_prev][index] <= 0 :
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)
                # if list_values[INDEX_FINAL_SIGNAL][index] == BUY_REVERSE:
                #     self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                #     result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                #     acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)
                elif list_values[INDEX_FINAL_SIGNAL][index] == SELL_TREND:
                    self.trigger_type = TRIGGER_TYPE_REVERSED_CROSS
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result,list_values[INDEX_ask_c][index], acumulated_loss)

            

        return acumulated_loss
    

class DonchianMultiTemporal5Tester:
    def __init__(self, df,
                    apply_signal,
                    apply_short_signal,
                    pip_value,
                    use_spread=True,
                    LOSS_FACTOR = 1000,
                    PROFIT_FACTOR = 200,
                    fixed_tp_sl=True,
                    trans_cost=8,
                    neg_multiplier=1,
                    rev=False,
                    spread_limit=50
                    ):
        self.use_spread = use_spread
        self.apply_signal = apply_signal
        self.apply_short_signal = apply_short_signal
        self.df = df.copy()
        self.LOSS_FACTOR = LOSS_FACTOR
        self.PROFIT_FACTOR = PROFIT_FACTOR
        self.pip_value = pip_value
        self.fixed_tp_sl = fixed_tp_sl
        self.acumulated_loss = []
        self.trans_cost = trans_cost
        self.neg_multiplier = neg_multiplier
        self.rev = rev
        self.spread_limit = spread_limit

        self.prepare_data()
        
    def prepare_data(self):
        
        print("prepare_data...")

        if self.use_spread == False:
            remove_spread(self.df)

        apply_signals(self.df, self.apply_signal, self.spread_limit)
        self.df.SIGNAL = self.df.SIGNAL.astype(int)

        if self.apply_short_signal != None:
            apply_short_signals(self.df, self.apply_short_signal)
            self.df.SIGNAL_TREND = self.df.SIGNAL_TREND.astype(int)

        apply_final_signals(self.df)

        
    def run_test(self):
        print("run_test...")
        open_trades_m5 = []
        closed_trades_m5 = []

        list_value_refs = [
            self.df.bid_c.array,
            self.df.ask_c.array,
            self.df.FINAL_SIGNAL.array,
            self.df.time.array,
            self.df.bid_h.array,
            self.df.bid_l.array,
            self.df.ask_h.array,
            self.df.ask_l.array,
            self.df.index.array,
            self.df.SIGNAL.array,
            self.df.DELTA_EMA_MID.array,
            self.df.DELTA_EMA_MID_PREV.array,
            self.df.DELTA_EMA_HIGH.array,
            self.df.DELTA_EMA_HIGH_PREV.array,
            self.df.DELTA_EMA_LOW.array,
            self.df.DELTA_EMA_LOW_PREV.array,
        ]

        for index in range(self.df.shape[0]):
            
            for ind, ot in enumerate(open_trades_m5):
                self.acumulated_loss = ot.update(list_value_refs, index, sorted(self.acumulated_loss,reverse=self.rev))
                if ot.running == False:
                    closed_trades_m5.append(ot)
            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]

            if list_value_refs[INDEX_FINAL_SIGNAL][index] in [-2,2]:
                open_trades_m5.append(Trade(list_value_refs, index, self.PROFIT_FACTOR, 
                                            self.LOSS_FACTOR, self.pip_value, self.trans_cost, self.neg_multiplier))  
            
        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5]) 
        print("Result:", self.df_results.result.sum())
        print("Len loss: ", len(self.acumulated_loss))
        print("Len Open:" , len(open_trades_m5))
        print("Len Close:" , len(closed_trades_m5))
