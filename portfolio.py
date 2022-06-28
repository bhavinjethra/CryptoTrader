from customLogger import logger
from db import session
from models import PortfolioDetails


def update_portfolio(coin_purchased) -> bool:
    """
    Updating the portfolio as per the following logic:
    If a new coin is purchased, quantity is 1, market value and sum invested is same as current price
    If a coin exists, then increment the quantity by 1, and the sum invested by current price,
    Market value is updated as quantity*current price.
    Do not commit for maintaining atomicity with the transactions.
    When the transactions are deleted, then make sure to reflect the decreased quantities and sum invested.
    It can go down to 0 which will denote transactions were deleted.
    :param coin_purchased:
    :return: Boolean: If true, then the transaction will be made.
    """
    try:
        # Check if the coin already exists in the Portfolio
        coin_exists = session.query(PortfolioDetails.coin_id).filter_by(
            coin_id=coin_purchased['id']).scalar() is not None
    except Exception as e:
        error_msg = f"Exception raised while checking coin existence in Portfolio table: {e}"
        print(e)
        logger.error(e)
        return False
    if coin_exists:
        try:
            portfolio_fetch = session.query(PortfolioDetails).get(coin_purchased['id'])
        except Exception as e:
            error_msg = f"Exception raised while fetching coin from Portfolio table: {e}"
            print(e)
            logger.error(e)
            return False
        portfolio_fetch.quantity += 1
        portfolio_fetch.sum_invested += coin_purchased['current_price']
        portfolio_fetch.market_value = portfolio_fetch.quantity * coin_purchased['current_price']
        # Hold off on commit till trade is executed
        return True
    else:
        try:
            p1 = PortfolioDetails(coin_id=coin_purchased['id'], quantity=1,
                                  sum_invested=coin_purchased['current_price'],
                                  market_value=coin_purchased['current_price'])
            session.add(p1)
        except Exception as e:
            error_msg = f"Exception raised while adding a coin in Portfolio table: {e}"
            print(e)
            logger.error(e)
            return False
        return True
        # Hold off on commit till trade is executed


def check_portfolio() -> bool:
    """
    Iterate through the portfolio coins and calculate the percentage gain or loss as follows:
    ((market value - sum invested)/sum invested)*100
    :return: None
    """
    try:
        portfolio_list = session.query(PortfolioDetails).all()
    except Exception as e:
        error_msg = f"Exception raised while querying Portfolio table: {e}"
        print(e)
        logger.error(e)
        return

    for coin_detail in portfolio_list:
        quantity = coin_detail.quantity
        current_market_value = coin_detail.market_value
        profit_loss_pcnt = 0
        # Ensuring division by 0 is taken care of
        if coin_detail.sum_invested != 0:
            profit_loss_pcnt = round(((current_market_value - coin_detail.sum_invested)
                                      / coin_detail.sum_invested) * 100, 2)
        portfolio_message = f"You hold {quantity} units of {coin_detail.coin_id} " \
                            f"at a total return of {profit_loss_pcnt}%"
        print(portfolio_message)
        logger.info(portfolio_message)
    return
