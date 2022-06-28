from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime

Base = declarative_base()


class CryptoCoins(Base):
    __tablename__ = 'CRYPTO_COINS'

    id = Column(String(15), nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    symbol = Column(String(5), nullable=False)
    current_price = Column(Float(6), nullable=False)
    timestamp = Column(DateTime, nullable=False)


class PortfolioDetails(Base):
    __tablename__ = 'Portfolio_Details'
    coinId = Column(String(15), primary_key=True)
    quantity = Column(Integer, nullable=False)
    sum_invested = Column(Float(6), nullable=False)
    market_value = Column(Float(6), nullable=False)


class TradeDetails(Base):
    __tablename__ = 'Trade_Details'
    tradeId = Column(Integer, primary_key=True)
    coin_id = Column(String(15), ForeignKey('Trade_Details.coin_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    sum_invested = Column(Float(6), nullable=False)
    timestamp = Column(DateTime, nullable=False)