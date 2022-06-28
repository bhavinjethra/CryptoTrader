from sqlalchemy import func

from customLogger import logger
from db import session
from models import TradeDetails
from portfolio import update_portfolio


def trade_coin(coin_purchased):
    """
    Adding and committing a transaction for every coin to purchase only
    if the updating the portfolio is successful.
    As the transaction table has a foreign key dependency on portfolio.
    If the transaction needs to be deleted, then you should also update the portfolio table
    to decrease the quantities.
    :param coin_purchased:
    :return:
    """
    if update_portfolio(coin_purchased):
        try:
            trade_instance = TradeDetails(coin_id=coin_purchased['id'], quantity=1,
                                          sum_invested=coin_purchased['current_price'], timestamp=func.now())
            session.add(trade_instance)
            session.commit()
            return True
        except Exception as e:
            error_msg = f"Exception raised while trading coin: {e}"
            print(e)
            logger.error(e)
            return False
    else:
        return False
