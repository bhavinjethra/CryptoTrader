"""Crypto API."""

from typing import Dict, List

import requests

# API Documentation - https://www.coingecko.com/en/api#explore-api


def get_coins() -> List[Dict]:
    """
    This function will get the top 10 coins at the current time, sorted by market cap in desc order.
    :return: List of top 10 coins
    """
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=marke'
                            't_cap_desc&per_page=10&page=1&sparkline=false')
    list_of_top_coins = []
    if response.status_code == 200:
        list_of_top_coins = response.json()
    # Important keys
    # - id
    # - symbol
    # - name
    # - current_price
    return list_of_top_coins


def get_coin_price_history(coin_id: str) -> List[Dict]:
    """
    This function will get the historical data of the coin
    :param coin_id: ID of the coin
    :return: List of historical prices
    """
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=9"
                            f"&interval=daily")
    if response.status_code == 200:
        # Returns a list of tuples
        # Item 0 -> Unix Timestamp
        # Item 1 -> price
        return response.json()['prices']
    return []


# utilize this function when submitting an order
def submit_order(coin_id: str, quantity: int, bid: float):
    """
    Mock function to submit an order to an exchange. 
    
    Assume order went through successfully and the return value is the price the order was filled at.
    """
    return bid


