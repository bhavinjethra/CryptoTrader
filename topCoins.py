from typing import Dict, List

from dateutil import parser

import crypto_api
from customLogger import logger
from db import session
from models import CryptoCoins
from trade import trade_coin


def get_top_coins() -> List[Dict]:
    """
    Gets the top coins by calling the API endpoint.
    Stores only the top 3, discarding the other coins, and trimming off only key features
    namely: id, symbol, name, current price, last updated.
    :return: list_of_top_coins: A dictionary containing a list of dictionary of top coins.
    """
    coins = crypto_api.get_coins()

    dict_coin = {}
    list_of_top_coins = []
    for coin_iterator in coins[:3]:
        dict_coin['id'] = coin_iterator['id']
        dict_coin['symbol'] = coin_iterator['symbol']
        dict_coin['name'] = coin_iterator['name']
        dict_coin['current_price'] = coin_iterator['current_price']
        dict_coin['last_updated'] = coin_iterator['last_updated']
        list_of_top_coins.append(dict_coin.copy())
    return list_of_top_coins


def buy_coin(coin_buy) -> bool:
    """
    This function calls a mock function to place an order.
    :param coin_buy: The coin to buy
    :return: Boolean: If the placed order was fulfilled
    """
    placed_at_bid_price = crypto_api.submit_order(coin_buy['id'], 1, coin_buy['current_price'])
    if placed_at_bid_price:
        return True
    return False


def decide_to_buy(coin_to_consider) -> bool:
    """
    This function defines whether or not to buy a coin. It averages the list of prices
    observed for the past 10 days.
    :param coin_to_consider: The top coin
    :return: Boolean: To buy or not to buy the coin
    """
    average_price_list = crypto_api.get_coin_price_history(coin_to_consider['id'])
    if average_price_list:
        # Zip the list of prices, and take average of prices which is the 2nd column accessed by [1].
        average_price_value = [sum(sub_list) / len(sub_list) for sub_list in zip(*average_price_list)][1]
        if coin_to_consider['current_price'] < average_price_value:
            return True
    return False


def add_to_table(coin):
    """
    This function stores the coins in the Crypto Coins table
    :param coin: The top coin
    :return: None
    """
    try:
        c1 = CryptoCoins(id=coin['id'], name=coin['name'], symbol=coin['symbol'],
                         current_price=coin['current_price'], timestamp=parser.parse(coin['last_updated']))
        session.add(c1)
        session.commit()
    except Exception as e:
        error_msg = f"Exception raised while adding coin details in Crypto Coins table: {e}"
        print(e)
        logger.error(e)
    return


def add_and_buy_coins(top_coins):
    """
    This function iterates through the top coins and decides whether to buy or not
    If it decides to buy, it places a trade and logs the trade details. If it fails
    while trading, it rollbacks.
    :param top_coins:
    :return: None
    """
    for coin_iterator in top_coins:
        add_to_table(coin_iterator)
        if decide_to_buy(coin_iterator):
            if buy_coin(coin_iterator):
                # Update the database tables
                if trade_coin(coin_iterator):
                    log_message = f"Trade Executed: A bid was placed for 1 Quantity of" \
                                  f" {coin_iterator['id']} at {coin_iterator['current_price']}."
                    print(log_message)
                    logger.info(log_message)
                else:
                    session.rollback()
    return
