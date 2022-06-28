from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from db import Base


class CryptoCoins(Base):
    """
    A class representing the collection of top coins over the previous search
    storing the key fields of id, symbol, current price, and the timestamp.
    """
    __tablename__ = 'CRYPTO_COINS'

    id = Column(String(15), nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    symbol = Column(String(5), nullable=False)
    current_price = Column(Float(6), nullable=False)
    timestamp = Column(DateTime, nullable=False, primary_key=True)


class PortfolioDetails(Base):
    """
    A class representing the current holdings at any time. It lists the quantity held for each coin
    along with the sum invested, and the current market value.
    """
    __tablename__ = 'Portfolio_Details'

    coin_id = Column(String(15), primary_key=True)
    quantity = Column(Integer, nullable=False)
    sum_invested = Column(Float(6), nullable=False)
    market_value = Column(Float(6), nullable=False)


class TradeDetails(Base):
    """
    A class representing each trade that went through. It lists the quantity bought for the coin
    along with the price and time when it was executed. It has a Foreign key to the Portfolio.
    """
    __tablename__ = 'Trade_Details'

    trade_id = Column(Integer, primary_key=True)
    coin_id = Column(String(15), ForeignKey('Portfolio_Details.coin_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sum_invested = Column(Float(6), nullable=False)
    timestamp = Column(DateTime, nullable=False)
