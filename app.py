"""Crypto Interview Assessment Module."""
from portfolio import check_portfolio
from topCoins import add_and_buy_coins, get_top_coins


def initiate_app():
    """
    This function invokes the business logic to get the top coins every hour,
    and then calls a function to add it to database, and determine if the coin
    should be purchased. Then it invokes another function to log the portfolio
    details in a log file stored at storage/logs/app.log.
    :return:
    """
    top_coins = get_top_coins()
    add_and_buy_coins(top_coins)
    check_portfolio()