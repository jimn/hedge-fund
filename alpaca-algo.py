# alpaca.py - never break even!  That's our motto.
import config 
from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
from datetime import datetime, timedelta
import time
import random
BASE_URL = "https://paper-api.alpaca.markets"  # Changed back to paper trading URL without /v2
KEY_ID = "PK9U1RJGMLB48FZABD9J"
SECRET_KEY = "qhaLVhnkRDecpa4QlQXDcxw3zxzb3vw29OY87gDl"
SYMBOL_BARS = "BTC/USD"  # Format for crypto bars
SYMBOL_POSITION = "BTCUSD"  # Format for positions
NOTIONAL = 0
VERBOSITY = 2 # possible range of 0-3 with 0 being silent and 3 being verbose

api = REST(key_id=KEY_ID,secret_key=SECRET_KEY,base_url=BASE_URL)

def transact(symbol_bars, symbol_position, notional, side):
    """
    buy or sell something on Alpaca.

    Args:
        symbol_bars (str): The symbol to use for the order.
        symbol_position (str): The symbol to use for the position, e.g. 'BTCUSD'
        notional (float): The notional amount to use for the order, in USD.
        side (str): The side of the order to use for the order. example: 'buy' or 'sell'
    """
    try:
        # Submit a market order for crypto
        order_buy = api.submit_order(
            symbol=symbol_bars,  # Use BTC/USD for orders
            notional=notional,  
            side=side,
            type='market',
            time_in_force='gtc'
        )
        if VERBOSITY > 1:
            print(f"Order submitted successfully: {order_buy.id}")
        
        # Wait longer for the order to process and position to be updated
        if VERBOSITY > 1:
            print("Waiting for order to settle...")
            time.sleep(5)
        
        # Check the order status
        order_status = api.get_order(order_buy.id)
        if VERBOSITY > 1:
            print(f"Order status: {order_status.status}")
            if hasattr(order_status, 'filled_qty'):
                print(f"Filled quantity: {order_status.filled_qty}")
        
    except Exception as e:
        print(f"Error occurred during buy: {str(e)}")

def get_market_data(symbol, timeframe=TimeFrame.Minute, days=1):
    """
    Get market data for a given symbol.
    
    Args:
        symbol (str): Trading symbol (e.g., 'BTC/USD')
        timeframe (TimeFrame): Time interval for bars (default: TimeFrame.Minute)
        days (int): Number of days of historical data to fetch (default: 1)
    
    Returns:
        pandas.DataFrame: DataFrame containing market data with columns:
            - timestamp (index)
            - open, high, low, close (price data)
            - volume (trading volume)
            - trade_count (number of trades)
            - vwap (volume weighted average price)
    """
    try:
        end = datetime.now()
        start = end - timedelta(days=days)
        
        # Convert to string format required by API
        end = end.strftime('%Y-%m-%d')
        start = start.strftime('%Y-%m-%d')
        
        bars = api.get_crypto_bars(
            symbol,
            timeframe,
            start=start,
            end=end
        ).df
        
        return bars
    
    except Exception as e:
        print(f"Error getting market data for {symbol}: {str(e)}")
        return None

def trade_logically(bars):
    """
    Implement your trading logic here.
    """
    gods_say_buy = random.choice([True, False])
    if gods_say_buy:
        if VERBOSITY > 1:
            print("\nAttempting to buy Bitcoin...")
        notional = random.randint(1, 100)
        transact(SYMBOL_BARS, SYMBOL_POSITION, notional, 'buy')
        if VERBOSITY > 1:
            print(f"Bought {notional} of {SYMBOL_BARS}")
    else:
        if VERBOSITY > 1:
            print("\nAttempting to sell Bitcoin...")
        notional = random.randint(1, 100) 
        transact(SYMBOL_BARS, SYMBOL_POSITION, notional, 'sell')
        if VERBOSITY > 1:
            print(f"Sold {notional} of {SYMBOL_BARS}")


bars = get_market_data(SYMBOL_BARS)



# transact(SYMBOL_BARS, SYMBOL_POSITION, NOTIONAL, 'buy')
trade_logically(bars)

account = api.get_account()
if VERBOSITY > 0:
    print(f"\nAccount Status:")
    print(f"Cash available: ${account.cash}")
    print(f"Portfolio value: ${account.portfolio_value}")
    print(f"Buying power: ${account.buying_power}")


if VERBOSITY > 0:
    print("-------------------------------- (: --------------------------------")