from collections import deque

import pandas as pd
import datetime as dt
import numpy as np

BUY_REVERSE = 1
SELL_REVERSE = -1
BUY_TREND = 2
SELL_TREND = -2
NONE = 0

def remove_spread(df):
    for a in ["ask", "bid"]:
        for b in ["o", "h", "l", "c"]:
            c = f"{a}_{b}"
            df[c] = df[f"mid_{b}"]


# Inicializando as constantes para os sinais
SIGNAL_HIGH = 1
SIGNAL_87 = 2
SIGNAL_75 = 3
SIGNAL_62 = 4
SIGNAL_MID = 5
SIGNAL_37 = 6
SIGNAL_25 = 7
SIGNAL_12 = 8
SIGNAL_LOW = 9

# Função para detectar os sinais de cruzamentos
def detect_signals(df):

    # Inicializando vetores para manter o controle dos últimos cruzamentos
    last_band_cross_up = 0
    last_band_cross_down = 0
    
    # Vetores de preços e bandas para simplificar o código
    ema_short = df['EMA_short'].values
    donchian_87 = df['donchian_87'].values
    donchian_75 = df['donchian_75'].values
    donchian_62 = df['donchian_62'].values
    donchian_mid = df['donchian_mid'].values
    donchian_37 = df['donchian_37'].values
    donchian_25 = df['donchian_25'].values
    donchian_12 = df['donchian_12'].values
    donchian_high = df['donchian_high'].values
    donchian_low = df['donchian_low'].values
    
    spread = df['SPREAD'].values

    # Loop sobre o DataFrame para calcular os sinais
    for i in range(1, len(df)):
        if spread[i] < 50:
            # Verifica cruzamentos de alta
            if ema_short[i-1] <= donchian_87[i-1] and ema_short[i] > donchian_87[i]:
                if last_band_cross_up != '87':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_87
                    last_band_cross_up = '87'
                    
            if ema_short[i-1] <= donchian_75[i-1] and ema_short[i] > donchian_75[i]:
                if last_band_cross_up != '75':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_75
                    last_band_cross_up = '75'

            if ema_short[i-1] <= donchian_62[i-1] and ema_short[i] > donchian_62[i]:
                if last_band_cross_up != '62':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_62
                    last_band_cross_up = '62'
            
            if ema_short[i-1] <= donchian_mid[i-1] and ema_short[i] > donchian_mid[i]:
                if last_band_cross_up != 'mid':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_MID
                    last_band_cross_up = 'mid'
            
            if ema_short[i-1] <= donchian_37[i-1] and ema_short[i] > donchian_37[i]:
                if last_band_cross_up != '37':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_37
                    last_band_cross_up = '37'
            
            if ema_short[i-1] <= donchian_25[i-1] and ema_short[i] > donchian_25[i]:
                if last_band_cross_up != '25':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_25
                    last_band_cross_up = '25'
            
            if ema_short[i-1] <= donchian_12[i-1] and ema_short[i] > donchian_12[i]:
                if last_band_cross_up != '12':
                    df.at[i, 'SIGNAL_UP'] = SIGNAL_12
                    last_band_cross_up = '12'
            
            # Caso especial para donchian_high
            if ema_short[i-1] <= donchian_high[i-100] and ema_short[i] > donchian_high[i-100]:
                df.at[i, 'SIGNAL_UP'] = SIGNAL_HIGH
                last_band_cross_up = 'high'
            
            # Verifica cruzamentos de baixa        
            if ema_short[i-1] >= donchian_87[i-1] and ema_short[i] < donchian_87[i]:
                if last_band_cross_down != '87':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_87
                    last_band_cross_down = '87'

            if ema_short[i-1] >= donchian_75[i-1] and ema_short[i] < donchian_75[i]:
                if last_band_cross_down != '75':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_75
                    last_band_cross_down = '75'
            
            if ema_short[i-1] >= donchian_62[i-1] and ema_short[i] < donchian_62[i]:
                if last_band_cross_down != '62':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_62
                    last_band_cross_down = '62'

            if ema_short[i-1] >= donchian_mid[i-1] and ema_short[i] < donchian_mid[i]:
                if last_band_cross_down != 'mid':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_MID
                    last_band_cross_down = 'mid'

            if ema_short[i-1] >= donchian_37[i-1] and ema_short[i] < donchian_37[i]:
                if last_band_cross_down != '37':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_37
                    last_band_cross_down = '37'
            
            if ema_short[i-1] >= donchian_25[i-1] and ema_short[i] < donchian_25[i]:
                if last_band_cross_down != '25':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_25
                    last_band_cross_down = '25'
            
            if ema_short[i-1] >= donchian_12[i-1] and ema_short[i] < donchian_12[i]:
                if last_band_cross_down != '12':
                    df.at[i, 'SIGNAL_DOWN'] = SIGNAL_12
                    last_band_cross_down = '12'
            
            # Caso especial para donchian_low
            if ema_short[i-1] >= donchian_low[i-100] and ema_short[i] < donchian_low[i-100]:
                df.at[i, 'SIGNAL_DOWN'] = SIGNAL_LOW
                last_band_cross_down = 'low'

    return df

INDEX_bid_c = 0
INDEX_ask_c = 1
INDEX_SIGNAL_UP = 2
INDEX_SIGNAL_DOWN = 3
INDEX_time = 4
INDEX_bid_h = 5
INDEX_bid_l = 6
INDEX_ask_h = 7
INDEX_ask_l = 8
INDEX_name = 9
INDEX_ema_short = 10
INDEX_donchian_87 = 11
INDEX_donchian_75 = 12
INDEX_donchian_62 = 13
INDEX_donchian_mid = 14
INDEX_donchian_37 = 15
INDEX_donchian_25 = 16
INDEX_donchian_12 = 17
INDEX_donchian_high = 18
INDEX_donchian_low = 19

class Trade:
    def __init__(self, list_values, index, profit_factor, loss_factor, pip_value,trans_cost,neg_multiplier):
        self.running = True
        self.start_index_m5 = list_values[INDEX_name][index]
        self.profit_factor = profit_factor
        self.loss_factor = loss_factor
        self.pip_value = pip_value
        self.count = 0
        self.neg_multiplier = neg_multiplier
        self.trans_cost = trans_cost
        self.trigger_type = NONE

        if list_values[INDEX_SIGNAL_UP][index] in [1,2,3,4,5,6,7,8,9]:
            self.start_price = list_values[INDEX_bid_c][index]
            self.trigger_price = list_values[INDEX_bid_c][index]
            
        if list_values[INDEX_SIGNAL_DOWN][index] in [1,2,3,4,5,6,7,8,9]:
            self.start_price = list_values[INDEX_ask_c][index]
            self.trigger_price = list_values[INDEX_ask_c][index]
            
        self.SIGNAL_UP = list_values[INDEX_SIGNAL_UP][index]
        self.SIGNAL_DOWN = list_values[INDEX_SIGNAL_DOWN][index]
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

        if min_acumulated_loss > 0.0:
            if result >= self.neg_multiplier*min_acumulated_loss:
                if len(acumulated_loss) > 0:
                    acumulated_loss = acumulated_loss[1:]

        return acumulated_loss

    def update(self, list_values, index, acumulated_loss):

        min_acumulated_loss = acumulated_loss[0] if len(acumulated_loss) > 0 else 0.0
        value_loss_trans_cost = (self.neg_multiplier*min_acumulated_loss) + self.trans_cost
        self.count += 1
        close_op = False
      
        # AQUI APENAS COMPRAS
        if self.SIGNAL_UP == SIGNAL_HIGH:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_HIGH
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_HIGH:
                    self.trigger_type = SIGNAL_HIGH
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_75:
                    self.trigger_type = SIGNAL_HIGH
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_87:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_87
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_HIGH:
                    self.trigger_type = SIGNAL_87
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_62:
                    self.trigger_type = SIGNAL_87
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_75:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_75
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_87:
                    self.trigger_type = SIGNAL_75
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_MID:
                    self.trigger_type = SIGNAL_75
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_62:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_62
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_75:
                    self.trigger_type = SIGNAL_62
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_37:
                    self.trigger_type = SIGNAL_62
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_MID:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_MID
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_62:
                    self.trigger_type = SIGNAL_MID
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_25:
                    self.trigger_type = SIGNAL_MID
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_37:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_37
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_MID:
                    self.trigger_type = SIGNAL_37
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_12:
                    self.trigger_type = SIGNAL_37
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_25:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_25
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_37:
                    self.trigger_type = SIGNAL_25
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_LOW:
                    self.trigger_type = SIGNAL_25
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_UP == SIGNAL_12:
            if min_acumulated_loss > 0.0:
                result = (list_values[INDEX_bid_h][index] - self.start_price) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_12
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_bid_h][index]
                    acumulated_loss = self.close_trade(list_values, index, result, trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_UP][index] == SIGNAL_37:
                    self.trigger_type = SIGNAL_12
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_LOW:
                    self.trigger_type = SIGNAL_12
                    result = (list_values[INDEX_bid_c][index] - self.start_price) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  

        # AQUI APENAS VENDAS
        if self.SIGNAL_DOWN == SIGNAL_87:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_87
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_75:
                    self.trigger_type = SIGNAL_87
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_HIGH:
                    self.trigger_type = SIGNAL_87
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_75:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_75
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_62:
                    self.trigger_type = SIGNAL_75
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_HIGH:
                    self.trigger_type = SIGNAL_75
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_62:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_62
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_MID:
                    self.trigger_type = SIGNAL_62
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_87:
                    self.trigger_type = SIGNAL_62
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_MID:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_MID
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_37:
                    self.trigger_type = SIGNAL_MID
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_75:
                    self.trigger_type = SIGNAL_MID
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_37:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_37
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_25:
                    self.trigger_type = SIGNAL_37
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_62:
                    self.trigger_type = SIGNAL_37
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_25:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_25
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_12:
                    self.trigger_type = SIGNAL_25
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_MID:
                    self.trigger_type = SIGNAL_25
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_12:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_12
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_LOW:
                    self.trigger_type = SIGNAL_12
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_37:
                    self.trigger_type = SIGNAL_12
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  
        elif self.SIGNAL_DOWN == SIGNAL_LOW:
            if min_acumulated_loss > 0.0:
                result = (self.start_price - list_values[INDEX_ask_l][index]) / self.pip_value
                if result >= value_loss_trans_cost:
                    self.trigger_type = SIGNAL_LOW
                    result = value_loss_trans_cost
                    trigger_price = list_values[INDEX_ask_l][index]
                    acumulated_loss = self.close_trade(list_values, index, result,trigger_price, acumulated_loss)
                    close_op = True
            if close_op == False:
                if list_values[INDEX_SIGNAL_DOWN][index] == SIGNAL_LOW:
                    self.trigger_type = SIGNAL_LOW
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)
                elif list_values[INDEX_SIGNAL_UP][index] == SIGNAL_25:
                    self.trigger_type = SIGNAL_LOW
                    result = (self.start_price - list_values[INDEX_ask_c][index]) / self.pip_value
                    acumulated_loss = self.close_trade(list_values, index, result, list_values[INDEX_bid_c][index], acumulated_loss)  

        return acumulated_loss
    


    # def update(self, list_values, index, acumulated_loss):
    #     min_acumulated_loss = acumulated_loss[0] if len(acumulated_loss) > 0 else 0.0
    #     value_loss_trans_cost = (self.neg_multiplier * min_acumulated_loss) + self.trans_cost
    #     self.count += 1
    #     close_op = False

    #     def close_trade(result, trigger_price):
    #         """Encapsula o fechamento de trade"""
    #         return self.close_trade(list_values, index, result, trigger_price, acumulated_loss)

    #     def process_trade(signal_type, result_calc, signal_level_up, signal_level_down):
    #         nonlocal close_op, acumulated_loss
    #         if min_acumulated_loss > 0.0:
    #             result = result_calc(list_values, index) / self.pip_value
    #             if result >= value_loss_trans_cost:
    #                 self.trigger_type = TRIGGER_TYPE_MIN_LOSS_BUY if signal_type == 'buy' else TRIGGER_TYPE_MIN_LOSS_SELL
    #                 acumulated_loss = close_trade(value_loss_trans_cost, list_values[INDEX_bid_h][index] if signal_type == 'buy' else list_values[INDEX_ask_l][index])
    #                 close_op = True
    #         if not close_op:
    #             if list_values[INDEX_SIGNAL_UP][index] == signal_level_up:
    #                 self.trigger_type = signal_level_up
    #                 result = result_calc(list_values, index) / self.pip_value
    #                 acumulated_loss = close_trade(result, list_values[INDEX_bid_c][index])
    #             elif list_values[INDEX_SIGNAL_DOWN][index] == signal_level_down:
    #                 self.trigger_type = signal_level_up
    #                 result = result_calc(list_values, index) / self.pip_value
    #                 acumulated_loss = close_trade(result, list_values[INDEX_bid_c][index])

    #     # Cálculos de resultados de compra e venda
    #     def calc_result_buy(lv, idx):
    #         return lv[INDEX_bid_h][idx] - self.start_price

    #     def calc_result_sell(lv, idx):
    #         return self.start_price - lv[INDEX_ask_l][idx]

    #     # Verificação dos sinais de COMPRA
    #     if self.SIGNAL_UP == SIGNAL_HIGH:
    #         process_trade('buy', calc_result_buy, SIGNAL_HIGH, SIGNAL_75)
    #     elif self.SIGNAL_UP == SIGNAL_87:
    #         process_trade('buy', calc_result_buy, SIGNAL_HIGH, SIGNAL_62)
    #     elif self.SIGNAL_UP == SIGNAL_75:
    #         process_trade('buy', calc_result_buy, SIGNAL_87, SIGNAL_MID)
    #     elif self.SIGNAL_UP == SIGNAL_62:
    #         process_trade('buy', calc_result_buy, SIGNAL_75, SIGNAL_37)
    #     elif self.SIGNAL_UP == SIGNAL_MID:
    #         process_trade('buy', calc_result_buy, SIGNAL_62, SIGNAL_25)
    #     elif self.SIGNAL_UP == SIGNAL_37:
    #         process_trade('buy', calc_result_buy, SIGNAL_MID, SIGNAL_12)
    #     elif self.SIGNAL_UP == SIGNAL_25:
    #         process_trade('buy', calc_result_buy, SIGNAL_37, SIGNAL_LOW)
    #     elif self.SIGNAL_UP == SIGNAL_12:
    #         process_trade('buy', calc_result_buy, SIGNAL_37, SIGNAL_LOW)

    #     # Verificação dos sinais de VENDA
    #     if self.SIGNAL_DOWN == SIGNAL_87:
    #         process_trade('sell', calc_result_sell, SIGNAL_75, SIGNAL_HIGH)
    #     elif self.SIGNAL_DOWN == SIGNAL_75:
    #         process_trade('sell', calc_result_sell, SIGNAL_62, SIGNAL_HIGH)
    #     elif self.SIGNAL_DOWN == SIGNAL_62:
    #         process_trade('sell', calc_result_sell, SIGNAL_MID, SIGNAL_87)
    #     elif self.SIGNAL_DOWN == SIGNAL_MID:
    #         process_trade('sell', calc_result_sell, SIGNAL_37, SIGNAL_75)
    #     elif self.SIGNAL_DOWN == SIGNAL_37:
    #         process_trade('sell', calc_result_sell, SIGNAL_25, SIGNAL_62)
    #     elif self.SIGNAL_DOWN == SIGNAL_25:
    #         process_trade('sell', calc_result_sell, SIGNAL_12, SIGNAL_MID)
    #     elif self.SIGNAL_DOWN == SIGNAL_12:
    #         process_trade('sell', calc_result_sell, SIGNAL_LOW, SIGNAL_37)
    #     elif self.SIGNAL_DOWN == SIGNAL_LOW:
    #         process_trade('sell', calc_result_sell, SIGNAL_LOW, SIGNAL_25)

    #     return acumulated_loss
    


class DonchianMultiTemporal6Tester:
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
        self.df = df
        self.LOSS_FACTOR = LOSS_FACTOR
        self.PROFIT_FACTOR = PROFIT_FACTOR
        self.pip_value = pip_value
        self.fixed_tp_sl = fixed_tp_sl
        self.acumulated_loss = []
        self.trans_cost = trans_cost
        self.neg_multiplier = neg_multiplier
        self.rev = rev
        self.spread_limit = spread_limit
        self.len_close = 0
        self.len_open = 0
        
        self.prepare_data()
        
    def prepare_data(self):
        
        # print("prepare_data...")

        if self.use_spread == False:
            remove_spread(self.df)

        # Inicializando as novas colunas com zeros
        self.df['SIGNAL_UP'] = 0
        self.df['SIGNAL_DOWN'] = 0

        # Aplicar a função para detectar sinais
        detect_signals(self.df)
 
    def run_test(self):
        # print("run_test...")
        open_trades_m5 = deque()
        closed_trades_m5 = deque()

        list_value_refs = [
            self.df.bid_c.values,
            self.df.ask_c.values,
            self.df.SIGNAL_UP.values,
            self.df.SIGNAL_DOWN.values,
            self.df.time.values,
            self.df.bid_h.values,
            self.df.bid_l.values,
            self.df.ask_h.values,
            self.df.ask_l.values,
            self.df.index.values,
            self.df.EMA_short.values,
            self.df.donchian_87.values,
            self.df.donchian_75.values,
            self.df.donchian_62.values,
            self.df.donchian_mid.values,
            self.df.donchian_37.values,
            self.df.donchian_25.values,
            self.df.donchian_12.values,
            self.df.donchian_high.values,
            self.df.donchian_low.values,
        ]

        for index in range(self.df.shape[0]):
            
            for ind, ot in enumerate(open_trades_m5):
                self.acumulated_loss = ot.update(list_value_refs, index, sorted(self.acumulated_loss,reverse=self.rev))
                if ot.running == False:
                    closed_trades_m5.append(ot)
            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]

            if list_value_refs[INDEX_SIGNAL_UP][index] in [1,2,3,4]:
                open_trades_m5.append(Trade(list_value_refs, index, self.PROFIT_FACTOR, 
                                            self.LOSS_FACTOR, self.pip_value, self.trans_cost, self.neg_multiplier))  
                # print(len(open_trades_m5),len(closed_trades_m5))
            elif list_value_refs[INDEX_SIGNAL_DOWN][index] in [6,7,8,9]:
                open_trades_m5.append(Trade(list_value_refs, index, self.PROFIT_FACTOR, 
                                            self.LOSS_FACTOR, self.pip_value, self.trans_cost, self.neg_multiplier))  
                # print(len(open_trades_m5),len(closed_trades_m5))

        self.len_close = len(closed_trades_m5)
        self.len_open = len(open_trades_m5)
        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5]) 
        res_pos = self.df_results[self.df_results['result'] > 0]
        res_neg = self.df_results[self.df_results['result'] < 0]
        sum_neg = res_neg.result.sum() * -1
        sum_pos = res_pos.result.sum()
        
        print("")
        print("Result:", self.df_results.result.sum())
        print("Len loss: ", len(self.acumulated_loss))
        print("Len Open:" , len(open_trades_m5))
        print("Len Close:" , len(closed_trades_m5))
        print("Len Pos", len(res_pos))
        print("Len Neg", len(res_neg))
        print("Res pos", sum_pos)
        print("Res neg", sum_neg)
        print("Rel len pos neg", len(res_pos)/(len(res_pos)+ len(res_neg)))
        print("Rel len neg pos", len(res_neg)/(len(res_pos)+ len(res_neg)))
        print("Rel pos neg", sum_pos/(sum_pos+ sum_neg))
        print("Rel neg pos", sum_neg/(sum_pos+ sum_neg))
        print("")
