import math

def num_BTC(b):
    c = float(0)
    start_btc = float(50)
    n_cycle = int(b/210000)
    n_left = b % 210000
    multiply = 2 * (1 - pow(0.5, n_cycle))
    end_btc = start_btc * pow(0.5, n_cycle)
    c = 10500000 * multiply + end_btc * n_left
    return c




