"""Crypto Interview Assessment Module."""

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

import crypto_api
from db import engine, session
from models import Base, CryptoCoins, PortfolioDetails

logger = logging.getLogger(__name__)


def setup_logger():
    """
    Setting a 7-day logger for the transactions
    :return: None
    """
    global logger
    logger.handlers.clear()
    # create handler
    handler = TimedRotatingFileHandler(filename='storage/logs/app.log', when='midnight', interval=1, backupCount=7,
                                       encoding='utf-8',
                                       delay=False)
    # Create formatter and add to handler
    formatter = Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handler to named logger
    logger.addHandker(handler)
    # set the logging level
    logger.setLevel(logging.INFO)


Base.metadata.create_all(engine)


def get_top_coins():
    coins = crypto_api.get_coins()

    dict_coin = {}
    list_of_top_coins = []
    for coin in coins[:3]:
        dict_coin['id'] = coin['id']
        dict_coin['symbol'] = coin['symbol']
        dict_coin['name'] = coin['name']
        dict_coin['current_price'] = coin['current_price']
        list_of_top_coins.append(dict_coin.copy())
    return list_of_top_coins


def add_to_table(coin):
    c1 = CryptoCoins(id=coin['id'], name=coin['name'], symbol=coin['symbol'],
                     current_price=coin['current_price'])
    session.add(c1)
    session.commit()


def trade_coin(coin_purchased):
    return


def update_portfolio(coin_purchased):
    exists = session.query(PortfolioDetails.coinId).filter_by(coinId=coin_purchased['id']).scalar() is not None
    if exists:
        x = session.query(PortfolioDetails).get(coin_purchased['id'])
        x.quantity += 1
        x.sum_invested += coin_purchased['current_price']
        x.market_value = coin_purchased['current_price']
        session.commit()
    else:
        p1 = PortfolioDetails(coinId=coin_purchased['id'], quantity=1, sum_invested=coin_purchased['current_price'],
                              market_value=coin_purchased['current_price'])
        session.add(p1)
        session.commit()


def check_portfolio():
    portfolio_list = session.query(PortfolioDetails).all()
    for coin_detail in portfolio_list:
        quantity = coin_detail.quantity
        current_market_value = coin_detail.market_value
        total_market_value = quantity * current_market_value
        profit_loss_pcnt = round(((total_market_value - coin_detail.sum_invested)
                                  / coin_detail.sum_invested) * 100, 2)
        portfolio_message = f"You hold {quantity} units of {coin_detail.coinId} " \
                            f"at a total return of {profit_loss_pcnt}%"
        print(portfolio_message)
        logger.info(portfolio_message)


setup_logger()
top_coins = get_top_coins()
for coin in top_coins:
    add_to_table(coin)
    average_price_list = crypto_api.get_coin_price_history(coin['id'])
    if average_price_list:
        # Zip the list of prices, and take average.
        average_price_value = [sum(sub_list) / len(sub_list) for sub_list in zip(*average_price_list)][1]
        if coin['current_price'] > average_price_value:
            placed_at_bid_price = crypto_api.submit_order(coin['id'], 1, coin['current_price'])
            if placed_at_bid_price:
                trade_coin(coin)
                update_portfolio(coin)
                log_message = f"Trade Executed: A bid was placed for 1 Quantity of {coin['id']} at {placed_at_bid_price}."
                print(log_message)
                logger.info(log_message)
check_portfolio()
