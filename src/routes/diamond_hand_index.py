import sys, math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from wallstreet import Call, Put, Stock
from scipy.stats import norm
from datetime import datetime, timedelta

def get_expiries_bracket(ticker, num_of_days):
    c = Call(ticker)
    expiries = c.expirations
    curr_date = str(datetime.date(datetime.now()))
    longer_expiry = expiries[-1]
    shorter_expiry = expiries[0]
    shorter_day_bound = (datetime.strptime(shorter_expiry,'%d-%m-%Y') - datetime.strptime(curr_date,'%Y-%m-%d')).days
    longer_day_bound = (datetime.strptime(longer_expiry,'%d-%m-%Y') - datetime.strptime(curr_date,'%Y-%m-%d')).days
    for i in expiries:
        days_to_exp = abs(datetime.strptime(i,'%d-%m-%Y') - datetime.strptime(curr_date,'%Y-%m-%d')).days
        if days_to_exp < num_of_days and days_to_exp > shorter_day_bound  :
            shorter_day_bound = days_to_exp
            shorter_expiry = i
            longer_day_bound = days_to_exp
            longer_expiry = i
        elif days_to_exp >= num_of_days:
            longer_day_bound = days_to_exp
            longer_expiry = i
            break;
    shorter_weight = 1;
    if longer_day_bound != shorter_day_bound:
        shorter_weight = (longer_day_bound - num_of_days) / (longer_day_bound - shorter_day_bound)
    return {'shorter_expiry':shorter_expiry,'longer_expiry':longer_expiry,'shorter_day_bound':shorter_day_bound,'longer_day_bound':longer_day_bound, 'shorter_weight':shorter_weight}

def get_strike_bracket(call_object, price_target):
    strikes = call_object.strikes
    higher_strike = strikes[0]
    lower_strike = strikes[0]
    if price_target < strikes[0]:
        return (-1,-1)
    if price_target > strikes[-1]:
        return (-10,-10)
    for i in strikes:
        if i < price_target and i > lower_strike:
            lower_strike = i
            higher_strike = i
        elif i >= price_target:
            higher_strike = i
            break;
    lower_weight = 1
    if higher_strike != lower_strike:
        lower_weight = (higher_strike - price_target)/(higher_strike - lower_strike)
    return {'lower_strike':lower_strike,'higher_strike':higher_strike, 'lower_weight':lower_weight}

def get_atm_ivol(s, ndays=30):
    symbol = s.ticker
    expiry_dict = get_expiries_bracket(symbol, ndays)
    #First Shorter One
    x = expiry_dict['shorter_expiry']
    shorter_call = Call(symbol,d=int(x[0:2]),m=int(x[3:5]),y=int(x[6:10]))
    strike_dict = get_strike_bracket(shorter_call, s.price)
    shorter_call.set_strike(strike_dict['lower_strike'])
    lower_vol = shorter_call.implied_volatility()
    shorter_call.set_strike(strike_dict['higher_strike'])
    higher_vol = shorter_call.implied_volatility()
    shorter_ivol = lower_vol*strike_dict['lower_weight'] + higher_vol*(1-strike_dict['lower_weight'])
    #Now longer One
    x = expiry_dict['longer_expiry']
    longer_call = Call(symbol,d=int(x[0:2]),m=int(x[3:5]),y=int(x[6:10]))
    strike_dict = get_strike_bracket(longer_call, s.price)
    longer_call.set_strike(strike_dict['lower_strike'])
    lower_vol = longer_call.implied_volatility()
    longer_call.set_strike(strike_dict['higher_strike'])
    higher_vol = longer_call.implied_volatility()
    longer_ivol = lower_vol*strike_dict['lower_weight'] + higher_vol*(1-strike_dict['lower_weight'])
    implied_ivol = shorter_ivol*expiry_dict['shorter_weight'] + longer_ivol*(1-expiry_dict['shorter_weight'])
    one_sigma_move_ndays_day = implied_ivol*math.sqrt(ndays/365)
    return (implied_ivol, one_sigma_move_ndays_day)

def generate_svelte_file():
    timestamp = datetime.now().strftime('%b,%d %Y %I:%M:%S %p')
    svelte_file = """
    <style>
    	h1, figure, p {
    		text-align: center;
    		margin: 0 auto;
    	}

    	h1 {
    		font-size: 2.8em;
    		text-transform: uppercase;
    		font-weight: 700;
    		margin: 0 0 0.5em 0;
    	}

    	figure {
    		margin: 0 0 1em 0;
    	}

    	img {
    		width: 100%;
    		max-width: 400px;
    		margin: 0 0 1em 0;
    	}

    	p {
    		margin: 1em auto;
    	}

    	@media (min-width: 480px) {
    		h1 {
    			font-size: 4em;
    		}
    	}
    </style>

    <svelte:head>
    	<title>Diamond Oracle</title>
    </svelte:head>

    <h1>💎 Oracle</h1>
    """
    file_to_append = f"{svelte_file}<p><em>Using <a href='https://finance.yahoo.com/quote/GME/options?p=GME'>Yahoo Finance Options Data</a>; Pulled {timestamp}</em></p>"

    with open("symbols.txt",'r') as f:
        sym_list = f.read().replace(" ", "").replace("\n", "").replace("\t", "").split(',')
        n_days = 5
        try:
            n_days = int(sym_list[0])
            sym_list = sym_list[1:]
        except ValueError:
            print("expected a number. Defaulting to 5")
        td = timedelta(n_days)
        print(sym_list)
        for i in sym_list:
            s = Stock(i)
            my_tuple = get_atm_ivol(s, n_days)
            my_range = my_tuple[1]*1.96*s.price
            file_to_append = f"{file_to_append}<p><strong>{s.ticker}: ${round(s.price - my_range)} - ${round(s.price + my_range)}</strong></p>\n"

        file_to_append = f"""
        {file_to_append}<p>[/🔱 Target Price: {(datetime.now()+td).strftime('%b,%d %Y')}, Odds: 95%]</p>

        <figure>
        	<img alt='Borat' src='great-success.png'>
        	<figcaption>HIGH FIVE!</figcaption>
        </figure>

        <p>Pappe: Who is the Oracle? What is the Matrix? The truth is, we no longer know.</p>
        """

    with open("../routes/index.svelte",'w') as f:
       f.write(file_to_append)


if __name__== "__main__":
    print(len(sys.argv))
    n_days = 30
    if len(sys.argv) == 1:
        generate_svelte_file()
    else:
        if len(sys.argv) == 3:
            n_days = int(sys.argv[2])
        s = Stock(sys.argv[1])
        my_tuple = get_atm_ivol(s, n_days)
        big_loss= 0.9
        sd_move_for_big_loss = big_loss/my_tuple[0]
        prob_of_loss_ndays = 1 - norm.cdf(sd_move_for_big_loss)
        print(f"The Diamond Hand Index of {sys.argv[1]} is {prob_of_loss_ndays*100:.7f} ")
        print(f"{s.ticker} (${s.price}): {n_days} day price range - ${s.price-my_tuple[1]*1.96*s.price:.2f} - ${s.price+my_tuple[1]*1.96*s.price:.2f}")
